/* Copyright (c) 2004-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "src/kernel/resource/profile/Profile.hpp"
#include "src/kernel/resource/profile/Event.hpp"
#include "src/kernel/resource/profile/FutureEvtSet.hpp"
#include "src/kernel/resource/profile/StochasticDatedValue.hpp"
#include "xbt/asserts.h"

#include <boost/algorithm/string.hpp>
#include <fstream>
#include <memory>
#include <ostream>
#include <sstream>
#include <unordered_map>
#include <utility>
#include <vector>
#include <string>

static std::unordered_map<std::string, simgrid::kernel::profile::Profile*> trace_list;

namespace simgrid::kernel::profile {

/** @brief Register this profile for that resource onto that FES,
 * and get an iterator over the integrated trace  */
Event* Profile::schedule(FutureEvtSet* fes, resource::Resource* resource)
{
  auto* event     = new Event();
  event->profile  = this;
  event->idx      = 0;
  event->resource = resource;
  event->free_me  = false;

  fes_ = fes;

  if (get_enough_events(0)) {
    fes_->add_event(event_list[0].date_, event);
  } else {
    event->free_me  = true;
    tmgr_trace_event_unref(&event);
  }
  return event;
}

/** @brief Gets the next event from a profile */
DatedValue Profile::next(Event* event)
{
  double event_date  = fes_->next_date();

  DatedValue dateVal = event_list.at(event->idx);

  event->idx++;

  if (get_enough_events(event->idx)) {
    const DatedValue& nextDateVal = event_list[event->idx];
    xbt_assert(nextDateVal.date_>=0);
    xbt_assert(nextDateVal.value_>=0);
    fes_->add_event(event_date +nextDateVal.date_, event);
  } else {
    event->free_me = true;
  }
  return dateVal;
}

Profile::Profile(const std::string& name, const std::function<ProfileBuilder::UpdateCb>& cb, double repeat_delay)
    : name(name), cb(cb), repeat_delay(repeat_delay)
{
  xbt_assert(trace_list.find(name) == trace_list.end(), "Refusing to define trace %s twice", name.c_str());
  trace_list.try_emplace(name, this);
  get_enough_events(0);
}

} // namespace simgrid::kernel::profile

void tmgr_finalize()
{
  for (auto const& [_, trace] : trace_list)
    delete trace;
  trace_list.clear();
}

void tmgr_trace_event_unref(simgrid::kernel::profile::Event** event)
{
  if ((*event)->free_me) {
    delete *event;
    *event = nullptr;
  }
}
