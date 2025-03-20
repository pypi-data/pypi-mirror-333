/* Copyright (c) 2007-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "src/mc/api/states/SleepSetState.hpp"
#include "src/mc/api/RemoteApp.hpp"
#include "xbt/log.h"

XBT_LOG_NEW_DEFAULT_SUBCATEGORY(mc_sleepset, mc_state, "DFS exploration algorithm of the model-checker");

namespace simgrid::mc {

SleepSetState::SleepSetState(RemoteApp& remote_app) : State(remote_app) {}

SleepSetState::SleepSetState(RemoteApp& remote_app, StatePtr parent_state) : State(remote_app, parent_state)
{
  /* Copy the sleep set and eventually removes things from it: */
  /* For each actor in the previous sleep set, keep it if it is not dependent with current transition.
   * And if we kept it and the actor is enabled in this state, mark the actor as already done, so that
   * it is not explored*/
  for (const auto& [aid, transition] : static_cast<SleepSetState*>(parent_state.get())->get_sleep_set()) {
    if (not get_transition_in()->depends(transition.get()))
      sleep_add_and_mark(transition);
  }

  if (not sleep_set_.empty() and parent_state->has_correct_execution())
    this->register_as_correct(); // FIX ME
  // This is only working if the parent has been fully explored when creating this state
  // In other word, if we are doing any sort of BeFS, there are no good reason for this to work as intented
}

void SleepSetState::sleep_add_and_mark(std::shared_ptr<Transition> transition)
{
  XBT_DEBUG("Adding transition Actor %ld:%s to the sleep set from parent state", transition->aid_,
            transition->to_string().c_str());
  sleep_set_.try_emplace(transition->aid_, transition);
  if (actors_to_run_.count(transition->aid_) != 0) {
    actors_to_run_.at(transition->aid_).mark_done();
  }
}

std::unordered_set<aid_t> SleepSetState::get_sleeping_actors(aid_t) const
{
  std::unordered_set<aid_t> actors;
  for (const auto& [aid, _] : get_sleep_set()) {
    actors.insert(aid);
  }
  return actors;
}
std::vector<aid_t> SleepSetState::get_enabled_minus_sleep() const
{
  std::vector<aid_t> actors;
  for (const auto& [aid, state] : actors_to_run_) {
    if (state.is_enabled() && sleep_set_.count(aid) < 1) {
      actors.insert(actors.begin(), aid);
    }
  }
  return actors;
}

bool SleepSetState::is_actor_sleeping(aid_t actor) const
{
  return std::find_if(sleep_set_.begin(), sleep_set_.end(), [=](const auto& pair) { return pair.first == actor; }) !=
         sleep_set_.end();
}

} // namespace simgrid::mc
