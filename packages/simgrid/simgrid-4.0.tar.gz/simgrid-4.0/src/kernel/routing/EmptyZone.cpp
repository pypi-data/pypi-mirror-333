/* Copyright (c) 2009-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include <xbt/dict.h>
#include <xbt/graph.h>
#include <xbt/log.h>

#include "simgrid/kernel/routing/EmptyZone.hpp"

XBT_LOG_NEW_DEFAULT_SUBCATEGORY(ker_routing_none, ker_platform, "Kernel No Routing");

namespace simgrid {
namespace kernel::routing {

void EmptyZone::get_graph(const s_xbt_graph_t* /*graph*/, std::map<std::string, xbt_node_t, std::less<>>* /*nodes*/,
                          std::map<std::string, xbt_edge_t, std::less<>>* /*edges*/)
{
  xbt_die("No routing no graph");
}
} // namespace kernel::routing

namespace s4u {
NetZone* create_empty_zone(const std::string& name)
{
  return (new kernel::routing::EmptyZone(name))->get_iface();
}
} // namespace s4u

} // namespace simgrid
