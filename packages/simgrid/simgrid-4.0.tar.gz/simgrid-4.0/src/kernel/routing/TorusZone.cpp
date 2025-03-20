/* Copyright (c) 2014-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "simgrid/kernel/routing/TorusZone.hpp"
#include "simgrid/kernel/routing/NetPoint.hpp"
#include "simgrid/s4u/Host.hpp"
#include "src/kernel/resource/NetworkModel.hpp"
#include "xbt/parse_units.hpp"

#include <numeric>
#include <string>
#include <vector>

XBT_LOG_NEW_DEFAULT_SUBCATEGORY(ker_routing_torus, ker_platform, "Kernel Torus Routing");

namespace simgrid {
namespace kernel::routing {

void TorusZone::create_torus_links(unsigned long id, int rank, unsigned long position)
{
  /* Create all links that exist in the torus. Each rank creates @a dimensions-1 links */
  unsigned long dim_product = 1; // Needed to calculate the next neighbor_id

  for (unsigned long j = 0; j < dimensions_.size(); j++) {
    unsigned long current_dimension =
        dimensions_[j]; // which dimension are we currently in?
                        // we need to iterate over all dimensions and create all links there
    // The other node the link connects
    unsigned long neighbor_rank_id = ((rank / dim_product) % current_dimension == current_dimension - 1)
                                         ? rank - (current_dimension - 1) * dim_product
                                         : rank + dim_product;
    // name of neighbor is not right for non contiguous cluster radicals (as id != rank in this case)
    std::string link_id = get_name() + "_link_from_" + std::to_string(id) + "_to_" + std::to_string(neighbor_rank_id);
    const s4u::Link* linkup;
    const s4u::Link* linkdown;
    if (get_link_sharing_policy() == s4u::Link::SharingPolicy::SPLITDUPLEX) {
      linkup   = add_link(link_id + "_UP", {get_link_bandwidth()})->set_latency(get_link_latency())->seal();
      linkdown = add_link(link_id + "_DOWN", {get_link_bandwidth()})->set_latency(get_link_latency())->seal();

    } else {
      linkup   = add_link(link_id, {get_link_bandwidth()})->set_latency(get_link_latency())->seal();
      linkdown = linkup;
    }
    /*
     * Add the link to its appropriate position.
     * Note that position rankId*(xbt_dynar_length(dimensions)+has_loopback?+has_limiter?)
     * holds the link "rankId->rankId"
     */
    add_private_link_at(position + j, {linkup->get_impl(), linkdown->get_impl()});
    dim_product *= current_dimension;
  }
}

void TorusZone::set_topology(const std::vector<unsigned long>& dimensions)
{
  xbt_assert(not dimensions.empty(), "Torus dimensions cannot be empty");
  dimensions_ = dimensions;
  set_tot_elements(std::accumulate(dimensions.begin(), dimensions.end(), 1, std::multiplies<>()));
  set_cluster_dimensions(dimensions);
  set_num_links_per_node(dimensions_.size());
}

void TorusZone::get_local_route(const NetPoint* src, const NetPoint* dst, Route* route, double* lat)
{
  XBT_VERB("torus getLocalRoute from '%s'[%lu] to '%s'[%lu]", src->get_cname(), src->id(), dst->get_cname(), dst->id());

  if (dst->is_router() || src->is_router())
    return;

  if (src->id() == dst->id() && has_loopback()) {
    resource::StandardLinkImpl* uplink = get_uplink_from(node_pos(src->id()));

    add_link_latency(route->link_list_, uplink, lat);
    return;
  }

  /*
   * Dimension based routing routes through each dimension consecutively
   * TODO Change to dynamic assignment
   */

  /*
   * Arrays that hold the coordinates of the current node and the target; comparing the values at the i-th position of
   * both arrays, we can easily assess whether we need to route into this dimension or not.
   */
  const unsigned long dsize = dimensions_.size();
  std::vector<unsigned long> myCoords(dsize);
  std::vector<unsigned long> targetCoords(dsize);
  unsigned int dim_size_product = 1;
  for (unsigned long i = 0; i < dsize; i++) {
    unsigned long cur_dim_size = dimensions_[i];
    myCoords[i]           = (src->id() / dim_size_product) % cur_dim_size;
    targetCoords[i]       = (dst->id() / dim_size_product) % cur_dim_size;
    dim_size_product *= cur_dim_size;
  }

  /*
   * linkOffset describes the offset where the link we want to use is stored(+1 is added because each node has a link
   * from itself to itself, which can only be the case if src->m_id == dst->m_id -- see above for this special case)
   */
  unsigned long linkOffset = (dsize + 1) * src->id();

  bool use_lnk_up = false; // Is this link of the form "cur -> next" or "next -> cur"? false means: next -> cur
  unsigned long current_node = src->id();
  while (current_node != dst->id()) {
    unsigned long next_node   = 0;
    unsigned long dim_product = 1; // First, we will route in x-dimension
    for (unsigned long j = 0; j < dsize; j++) {
      const unsigned long cur_dim = dimensions_[j];
      // current_node/dim_product = position in current dimension
      if ((current_node / dim_product) % cur_dim != (dst->id() / dim_product) % cur_dim) {
        if ((targetCoords[j] > myCoords[j] &&
             targetCoords[j] <= myCoords[j] + cur_dim / 2) // Is the target node on the right, without the wrap-around?
            ||
            (myCoords[j] > cur_dim / 2 && (myCoords[j] + cur_dim / 2) % cur_dim >=
                                              targetCoords[j])) { // Or do we need to use the wrap around to reach it?
          if ((current_node / dim_product) % cur_dim == cur_dim - 1)
            next_node = (current_node + dim_product - dim_product * cur_dim);
          else
            next_node = (current_node + dim_product);

          // HERE: We use *CURRENT* node for calculation (as opposed to next_node)
          linkOffset = node_pos_with_loopback_limiter(current_node) + j;
          use_lnk_up = true;
        } else { // Route to the left
          if ((current_node / dim_product) % cur_dim == 0)
            next_node = (current_node - dim_product + dim_product * cur_dim);
          else
            next_node = (current_node - dim_product);

          // HERE: We use *next* node for calculation (as opposed to current_node!)
          linkOffset = node_pos_with_loopback_limiter(next_node) + j;
          use_lnk_up = false;
        }
        XBT_DEBUG("torus_get_route_and_latency - current_node: %lu, next_node: %lu, linkOffset is %lu", current_node,
                  next_node, linkOffset);
        break;
      }

      dim_product *= cur_dim;
    }

    if (has_limiter()) { // limiter for sender
      route->link_list_.push_back(get_uplink_from(node_pos_with_loopback(current_node)));
    }

    resource::StandardLinkImpl* lnk;
    if (use_lnk_up)
      lnk = get_uplink_from(linkOffset);
    else
      lnk = get_downlink_to(linkOffset);

    add_link_latency(route->link_list_, lnk, lat);

    current_node = next_node;
  }
  if (has_limiter()) { // limiter for receiver/destination
    route->link_list_.push_back(get_downlink_to(node_pos_with_loopback(dst->id())));
  }
  // set gateways (if any)
  route->gw_src_ = get_gateway(src->id());
  route->gw_dst_ = get_gateway(dst->id());
}

void TorusZone::do_seal()
{
  for (int i = 0; i < get_tot_elements(); i++) {
    auto [netpoint, loopback, limiter] = fill_leaf_from_cb(i);
    create_torus_links(netpoint->id(), i, node_pos_with_loopback_limiter(netpoint->id()));
  }
}

} // namespace kernel::routing

namespace s4u {

NetZone* create_torus_zone(const std::string& name, NetZone* parent, const std::vector<unsigned long>& dimensions,
    const ClusterCallbacks& set_callbacks, double bandwidth, double latency,
    Link::SharingPolicy sharing_policy) // XBT_ATTRIB_DEPRECATED_v401
{
  auto* zone = parent->add_netzone_torus(name, dimensions, bandwidth, latency, sharing_policy);

  if (set_callbacks.is_by_netzone())
    zone->set_netzone_cb(set_callbacks.netzone);
  else
    zone->set_host_cb(set_callbacks.host);
  zone->set_loopback_cb(set_callbacks.loopback);
  zone->set_limiter_cb(set_callbacks.limiter);

  return zone;
}

NetZone* NetZone::add_netzone_torus(const std::string& name, const std::vector<unsigned long>& dimensions,
                                    const std::string& bandwidth, const std::string& latency, 
                                    Link::SharingPolicy sharing_policy)
{

  return add_netzone_torus(name, dimensions, xbt_parse_get_bandwidth("", 0, bandwidth, ""), 
                           xbt_parse_get_time("", 0, latency, ""), sharing_policy);
}

NetZone* NetZone::add_netzone_torus(const std::string& name, const std::vector<unsigned long>& dimensions,
                                      double bandwidth, double latency, Link::SharingPolicy sharing_policy)
{
  int tot_elements = std::accumulate(dimensions.begin(), dimensions.end(), 1, std::multiplies<>());
  if (dimensions.empty() || tot_elements <= 0)
    throw std::invalid_argument("TorusZone: incorrect dimensions parameter, each value must be > 0");
  if (bandwidth <= 0)
    throw std::invalid_argument("TorusZone: incorrect bandwidth for internode communication, bw=" +
                                std::to_string(bandwidth));
  if (latency < 0)
    throw std::invalid_argument("TorusZone: incorrect latency for internode communication, lat=" +
                                std::to_string(latency));

  auto* zone = new kernel::routing::TorusZone(name);
  zone->set_topology(dimensions);
  zone->set_parent(get_impl());

  zone->set_link_characteristics(bandwidth, latency, sharing_policy);

  return zone->get_iface();
}
} // namespace s4u

} // namespace simgrid
