/* Copyright (c) 2004-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#ifndef SIMGRID_KERNEL_PROFILE_EVENT_HPP
#define SIMGRID_KERNEL_PROFILE_EVENT_HPP

#include "simgrid/forward.h"

namespace simgrid::kernel::profile {

class Event {
public:
  Profile* profile;
  unsigned int idx;
  resource::Resource* resource;
  bool free_me;
};
} // namespace simgrid::kernel::profile
/**
 * @brief Free a trace event structure
 *
 * This function frees a trace_event if it can be freed, ie, if it has the free_me flag set to 1.
 * This flag indicates whether the structure is still used somewhere or not.
 * When the structure is freed, the argument is set to nullptr
 */
XBT_PUBLIC void tmgr_trace_event_unref(simgrid::kernel::profile::Event** trace_event);

#endif // SIMGRID_KERNEL_PROFILE_EVENT_HPP
