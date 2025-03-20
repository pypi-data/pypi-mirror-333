/* Copyright (c) 2016-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "src/mc/explo/ParallelizedExplorer.hpp"
#include "src/mc/explo/odpor/Execution.hpp"
#include "src/mc/mc_config.hpp"
#include "src/mc/mc_exit.hpp"
#include "src/mc/mc_forward.hpp"
#include "src/mc/mc_private.hpp"
#include "src/mc/mc_record.hpp"
#include "src/mc/remote/mc_protocol.h"
#include "src/mc/transition/Transition.hpp"

#include "src/mc/explo/reduction/BeFSODPOR.hpp"
#include "src/mc/explo/reduction/DPOR.hpp"
#include "src/mc/explo/reduction/NoReduction.hpp"
#include "src/mc/explo/reduction/Reduction.hpp"
#include "src/mc/explo/reduction/SDPOR.hpp"

#include "xbt/asserts.h"
#include "xbt/log.h"

#include <cassert>
#include <cstdio>

#include <algorithm>
#include <exception>
#include <limits>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <unordered_set>
#include <vector>

XBT_LOG_NEW_DEFAULT_SUBCATEGORY(mc_parallel, mc, "Parallel exploration algorithm of the model-checker");

namespace simgrid::mc {

RecordTrace ParallelizedExplorer::get_record_trace() // override
{
  RecordTrace res;

  if (const auto trans = stack_.back()->get_transition_out(); trans != nullptr)
    res.push_back(trans.get());
  for (const auto* state = stack_.back().get(); state != nullptr; state = state->get_parent_state())
    if (state->get_transition_in() != nullptr)
      res.push_front(state->get_transition_in().get());

  return res;
}

void ParallelizedExplorer::restore_stack(StatePtr state)
{
  XBT_DEBUG("Going to restore stack. Current depth is %lu; chosen state is #%ld", stack_.size(), state->get_num());
  stack_.clear();
  execution_seq_     = odpor::Execution();
  auto current_state = state;
  stack_.emplace_front(current_state);
  // condition corresponds to reaching initial state
  while (current_state->get_parent_state() != nullptr) {
    current_state = current_state->get_parent_state();
    stack_.emplace_front(current_state);
  }
  XBT_DEBUG("Replaced stack by %s", get_record_trace().to_string().c_str());
  // NOTE: The outgoing transition for the top-most state of the  stack refers to that which was taken
  // as part of the last trace explored by the algorithm. Thus, only the sequence of transitions leading up to,
  // but not including, the last state must be included when reconstructing the Exploration for SDPOR.
  for (auto iter = std::next(stack_.begin()); iter != stack_.end(); ++iter) {
    execution_seq_.push_transition((*iter)->get_transition_in());
  }
}

void ParallelizedExplorer::log_state() // override
{
  on_log_state_signal(get_remote_app());
  XBT_INFO("BeFS exploration ended. %ld unique states visited; %lu explored traces (%lu transition replays, "
           "%lu states "
           "visited overall)",
           State::get_expanded_states(), explored_traces_, Transition::get_replayed_transitions(),
           visited_states_count_);
  Exploration::log_state();
}

void ParallelizedExplorer::run()
{
  on_exploration_start_signal(get_remote_app());
  /* This function runs the Best First Search algorithm the state space.
   * We do so iteratively instead of recursively, dealing with the call stack manually.
   * This allows one to explore the call stack at will. */
  try {
    Explorer();
  } catch (McError& error) {
    XBT_CRITICAL("Going to kill the reducer");
    reducer.std::thread::~thread();
    throw error;
  }
  log_state();
}

StatePtr ParallelizedExplorer::best_opened_state()
{
  int best_prio = 0; // cache the value for the best priority found so far (initialized to silence gcc)
  auto best     = end(opened_states_);   // iterator to the state to explore having the best priority
  auto valid    = begin(opened_states_); // iterator marking the limit between states still to explore, and already
                                         // explored ones

  // Keep only still non-explored states (aid != -1), and record the one with the best (greater) priority.
  for (auto current = begin(opened_states_); current != end(opened_states_); ++current) {
    aid_t aid;
    int prio;
    if (current->get() == nullptr) {
      aid  = 0;
      prio = std::numeric_limits<int>::max();
    } else {
      aid  = (*current)->next_transition_guided().first;
      prio = (*current)->next_transition_guided().second;
    }
    if (aid == -1)
      continue;
    if (valid != current) {
      *valid = std::move(*current);
    }
    if (best == end(opened_states_) || prio <= best_prio) {
      best_prio = prio;
      best      = valid;
    }
    ++valid;
  }

  StatePtr best_state;
  if (best < valid) {
    // There are non-explored states, and one of them has the best priority.  Remove it from opened_states_ before
    // returning.
    best_state = std::move(*best);
    --valid;
    if (best != valid)
      *best = std::move(*valid);
  }
  opened_states_.erase(valid, end(opened_states_));

  return best_state;
}

void ParallelizedExplorer::backtrack()
{
  XBT_VERB("Backtracking from %s", get_record_trace().to_string().c_str());
  XBT_DEBUG("%lu alternatives are yet to be explored:", opened_states_.size());

  Exploration::check_deadlock();

  // Take the point with smallest distance
  std::unique_lock<std::mutex> lock_oh(opened_heads_lock_);
  opened_heads_cv_.wait(lock_oh, [&] { return opened_states_.size() > 1; });
  auto backtracking_point = best_opened_state();
  lock_oh.unlock();

  // if no backtracking point, then set the stack_ to empty so we can end the exploration
  if (not backtracking_point) {
    XBT_DEBUG("No more opened point of exploration, the search will end");
    stack_.clear();
    return;
  }
  // We found a backtracking point, let's go to it
  backtrack_to_state(backtracking_point.get());
  this->restore_stack(backtracking_point);
}

void ParallelizedExplorer::Explorer()
{
  while (not stack_.empty()) {
    /* Get current state */
    auto state = stack_.back();

    XBT_DEBUG("**************************************************");
    XBT_DEBUG("Exploration depth=%zu (state:#%ld; %zu interleaves todo; %lu currently opened states)", stack_.size(),
              state->get_num(), state->count_todo(), opened_states_.size());

    // Backtrack if we reached the maximum depth
    if (stack_.size() > (std::size_t)_sg_mc_max_depth) {
      XBT_WARN("/!\\ Max depth of %d reached! THIS WILL PROBABLY BREAK the reduction /!\\", _sg_mc_max_depth.get());
      XBT_WARN("/!\\ Any bug you may find are real, but not finding bug doesn't mean anything /!\\");
      XBT_WARN("/!\\ You should consider changing the depth limit with --cfg=model-check/max-depth /!\\");
      XBT_WARN("/!\\ Asumming you know what you are doing, the programm will now backtrack /!\\");
      this->backtrack();
      continue;
    }

    // Search for the next transition
    // next_transition returns a pair<aid_t, int>
    // in case we want to consider multiple states (eg. during backtrack)
    const aid_t next = reduction_algo_->next_to_explore(execution_seq_, &stack_);

    if (next < 0) {

      // If there is no more transition in the current state (or if ODPOR picked an actor that is not enabled --
      // ReversibleRace is an overapproximation), backtrace
      XBT_VERB("%lu actors remain, but none of them need to be interleaved (depth %zu).", state->get_actor_count(),
               stack_.size() + 1);
      Exploration::check_deadlock();

      if (state->get_actor_count() == 0) {
        // Compute the race when reaching a leaf, and pass them to the Reductor through the dedicated queue
        std::unique_ptr<Reduction::RaceUpdate> todo_updates =
            reduction_algo_->races_computation(execution_seq_, &stack_, &opened_states_);
        std::unique_lock<std::mutex> lock_ru(race_updates_lock_);
        race_updates_.push_back(std::move(todo_updates));
        lock_ru.unlock();
        race_updates_cv_.notify_one();

        explored_traces_++;
        get_remote_app().finalize_app();
        XBT_VERB("Execution came to an end at %s", get_record_trace().to_string().c_str());
        XBT_VERB("(state: %ld, depth: %zu, %lu explored traces)", state->get_num(), stack_.size(), explored_traces_);
        report_correct_execution(state.get());
      }

      this->backtrack();
      continue;
    }

    xbt_assert(state->is_actor_enabled(next));

    // If we use a state containing a sleep state, display it during debug
    if (XBT_LOG_ISENABLED(mc_parallel, xbt_log_priority_verbose) && reduction_mode_ != ReductionMode::none) {
      auto sleep_state = static_cast<SleepSetState*>(state.get());
      if (not sleep_state->get_sleep_set().empty()) {
        XBT_VERB("Sleep set actually containing:");

        for (const auto& [aid, transition] : sleep_state->get_sleep_set())
          XBT_VERB("  <%ld,%s>", aid, transition->to_string().c_str());
      }
    }

    auto todo = state->get_actors_list().at(next).get_transition();
    XBT_DEBUG("wanna execute %ld: %.60s", next, todo->to_string().c_str());

    /* Actually answer the request: let's execute the selected request (MCed does one step) */
    auto executed_transition = state->execute_next(next, get_remote_app());
    on_transition_execute_signal(state->get_transition_out().get(), get_remote_app());

    // If there are processes to interleave and the maximum depth has not been
    // reached then perform one step of the exploration algorithm.
    XBT_VERB("Executed %ld: %.60s (stack depth: %zu, state: %ld, %zu interleaves, %lu opened states)",
             state->get_transition_out()->aid_, state->get_transition_out()->to_string().c_str(), stack_.size(),
             state->get_num(), state->count_todo(), opened_states_.size());

    /* Create the new expanded state (copy the state of MCed into our MCer data) */
    auto next_state = reduction_algo_->state_create(get_remote_app(), state);
    if (_sg_mc_cached_states_interval > 0 && next_state->get_num() % _sg_mc_cached_states_interval == 0) {
      next_state->set_state_factory(get_remote_app().clone_checker_side());
    }
    on_state_creation_signal(next_state.get(), get_remote_app());

    visited_states_count_++;

    reduction_algo_->on_backtrack(state.get());

    // Before leaving that state, if the transition we just took can be taken multiple times, we
    // need to give it to the opened states
    if (stack_.back()->has_more_to_be_explored() > 0) {
      std::unique_lock<std::mutex> lock_oh(opened_heads_lock_);
      opened_states_.emplace_back(state);
      lock_oh.unlock();
    }

    stack_.emplace_back(std::move(next_state));
    execution_seq_.push_transition(std::move(executed_transition));
  }
}

void ParallelizedExplorer::Reducter()
{
  unsigned long possible_remaining_explo = 1;
  while (true) {
    std::unique_lock<std::mutex> lock_ru(race_updates_lock_);
    race_updates_cv_.wait(lock_ru, [&] { return race_updates_.size() > 0; });
    auto update = std::move(race_updates_.back());
    race_updates_.pop_back();
    lock_ru.unlock();

    std::unique_lock<std::mutex> lock_oh(opened_heads_lock_);
    possible_remaining_explo = reduction_algo_->apply_race_update(std::move(update), &opened_states_) - 1;
    if (possible_remaining_explo == 0) {
      opened_states_.emplace_back();
    }
    lock_oh.unlock();
    opened_heads_cv_.notify_one();
  }
}

ParallelizedExplorer::ParallelizedExplorer(const std::vector<char*>& args, ReductionMode mode)
    : Exploration(args), reduction_mode_(mode)
{

  if (reduction_mode_ == ReductionMode::dpor)
    reduction_algo_ = std::make_unique<DPOR>();
  else if (reduction_mode_ == ReductionMode::sdpor)
    reduction_algo_ = std::make_unique<SDPOR>();
  else if (reduction_mode_ == ReductionMode::odpor)
    reduction_algo_ = std::make_unique<BeFSODPOR>();
  else {
    xbt_assert(reduction_mode_ == ReductionMode::none, "Reduction mode %s not supported yet by BeFS explorer",
               to_c_str(reduction_mode_));
    reduction_algo_ = std::make_unique<NoReduction>();
  }

  reducer = std::thread([&] { this->Reducter(); });
  XBT_INFO("Start a parallelized exploration. Reduction is: %s.", to_c_str(reduction_mode_));

  auto initial_state = reduction_algo_->state_create(get_remote_app());

  XBT_DEBUG("**************************************************");

  stack_.emplace_back(std::move(initial_state));
  visited_states_count_++;

  /* Get an enabled actor and insert it in the interleave set of the initial state */
  XBT_DEBUG("Initial state. %lu actors to consider", stack_.back()->get_actor_count());

  opened_states_.emplace_back(stack_.back());
}

Exploration* create_parallelized_exploration(const std::vector<char*>& args, ReductionMode mode)
{
  return new ParallelizedExplorer(args, mode);
}

} // namespace simgrid::mc
