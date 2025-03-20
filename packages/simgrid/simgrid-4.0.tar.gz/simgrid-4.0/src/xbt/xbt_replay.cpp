/* Copyright (c) 2010-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "simgrid/Exception.hpp"
#include "xbt/log.h"
#include "xbt/replay.hpp"

#include <boost/algorithm/string.hpp>

XBT_LOG_NEW_DEFAULT_SUBCATEGORY(replay,xbt,"Replay trace reader");

namespace simgrid::xbt {

static std::ifstream action_fs;

std::unordered_map<std::string, action_fun> action_funs;
static std::unordered_map<std::string, std::queue<std::unique_ptr<ReplayAction>>> action_queues;

static void read_and_trim_line(std::ifstream& fs, std::string* line)
{
  do {
    std::getline(fs, *line);
    boost::trim(*line);
  } while (not fs.eof() && (line->length() == 0 || line->front() == '#'));
  XBT_DEBUG("got from trace: %s", line->c_str());
}

class ReplayReader {
  std::ifstream fs;
  std::string line;

public:
  explicit ReplayReader(const char* filename) : fs(filename, std::ifstream::in)
  {
    XBT_VERB("Prepare to replay file '%s'", filename);
    xbt_assert(fs.is_open(), "Cannot read replay file '%s'", filename);
  }
  ReplayReader(const ReplayReader&) = delete;
  ReplayReader& operator=(const ReplayReader&) = delete;
  bool get(ReplayAction* action);
};

bool ReplayReader::get(ReplayAction* action)
{
  read_and_trim_line(fs, &line);

  boost::split(*action, line, boost::is_any_of(" \t"), boost::token_compress_on);
  return not fs.eof();
}

static std::unique_ptr<ReplayAction> get_action(const char* name)
{
  if (auto queue_elt = action_queues.find(name); queue_elt != action_queues.end()) {
    if (auto& my_queue = queue_elt->second; not my_queue.empty()) {
      // Get something from my queue and return it
      auto action = std::move(my_queue.front());
      my_queue.pop();
      return action;
    }
  }

  // Nothing stored for me. Read the file further
  // Read lines until I reach something for me (which breaks in loop body) or end of file reached
  while (true) {
    std::string action_line;
    read_and_trim_line(action_fs, &action_line);
    if (action_fs.eof())
      break;
    /* we cannot split in place here because we parse&store several lines for the colleagues... */
    auto action = std::make_unique<ReplayAction>();
    boost::split(*action, action_line, boost::is_any_of(" \t"), boost::token_compress_on);

    // if it's for me, I'm done
    std::string evtname = action->front();
    if (evtname == name)
      return action;

    // else, I have to store it for the relevant colleague
    action_queues[evtname].emplace(std::move(action));
  }
  // end of file reached while searching in vain for more work

  return nullptr;
}

static void handle_action(ReplayAction& action)
{
  XBT_DEBUG("%s replays a %s action", action.at(0).c_str(), action.at(1).c_str());
  action_fun function;
  try {
    function = action_funs.at(action.at(1));
  } catch (const std::out_of_range&) {
    xbt_die("Replay Error: action %s is unknown, please register it properly in the replay engine",  action.at(1).c_str());
  }
  try {
    function(action);
  } catch (const Exception&) {
    action.clear();
    throw;
  }
}

/**
 * @ingroup XBT_replay
 * @brief function used internally to actually run the replay
 */
int replay_runner(const char* actor_name, const char* trace_filename)
{
  std::string actor_name_string(actor_name);
  if (simgrid::xbt::action_fs.is_open()) { // <A unique trace file
    xbt_assert(trace_filename == nullptr,
               "Passing nullptr to replay_runner() means that you want to use a shared trace, but you did not provide "
               "any. Please use xbt_replay_set_tracefile().");
    while (true) {
      auto evt = simgrid::xbt::get_action(actor_name);
      if (not evt)
        break;
      simgrid::xbt::handle_action(*evt);
    }
    action_queues.erase(actor_name_string);
  } else { // Should have got my trace file in argument
    xbt_assert(trace_filename != nullptr,
               "Trace replay cannot mix shared and unshared traces for now. Please don't set a shared tracefile with "
               "xbt_replay_set_tracefile() if you use actor-specific trace files using the second parameter of "
               "replay_runner().");
    simgrid::xbt::ReplayAction evt;
    simgrid::xbt::ReplayReader reader(trace_filename);
    while (reader.get(&evt)) {
      if (evt.front() == actor_name) {
        simgrid::xbt::handle_action(evt);
      } else {
        XBT_WARN("Ignore trace element not for me (target='%s', I am '%s')", evt.front().c_str(), actor_name);
      }
      evt.clear();
    }
  }
  return 0;
}
} // namespace simgrid::xbt

/**
 * @ingroup XBT_replay
 * @brief Registers a function to handle a kind of action
 *
 * Registers a function to handle a kind of action
 * This table is then used by @ref simgrid::xbt::replay_runner
 *
 * The argument of the function is the line describing the action, fields separated by spaces.
 *
 * @param action_name the reference name of the action.
 * @param function prototype given by the type: void...(simgrid::xbt::ReplayAction& action)
 */
void xbt_replay_action_register(const char* action_name, const action_fun& function)
{
  simgrid::xbt::action_funs[action_name] = function;
}

/**
 * @ingroup XBT_replay
 * @brief Get the function that was previously registered to handle a kind of action
 *
 * This can be useful if you want to override and extend an existing action.
 */
action_fun xbt_replay_action_get(const char* action_name)
{
  return simgrid::xbt::action_funs.at(action_name);
}

void xbt_replay_set_tracefile(const std::string& filename)
{
  xbt_assert(not simgrid::xbt::action_fs.is_open(), "Tracefile already set");
  simgrid::xbt::action_fs.open(filename, std::ifstream::in);
  xbt_assert(simgrid::xbt::action_fs.is_open(), "Failed to open file: %s", filename.c_str());
}
