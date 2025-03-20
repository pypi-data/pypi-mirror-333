/* Copyright (c) 2006-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include <simgrid/kernel/routing/NetPoint.hpp>
#include <simgrid/kernel/routing/NetZoneImpl.hpp>
#include <simgrid/s4u/Engine.hpp>
#include <simgrid/s4u/Host.hpp>
#include <simgrid/s4u/VirtualMachine.hpp>

#include "src/kernel/EngineImpl.hpp"
#include "src/kernel/resource/CpuImpl.hpp"
#include "src/kernel/resource/DiskImpl.hpp"
#include "src/kernel/resource/HostImpl.hpp"
#include "src/kernel/resource/NetworkModel.hpp"
#include "src/kernel/resource/SplitDuplexLinkImpl.hpp"
#include "src/kernel/resource/StandardLinkImpl.hpp"
#include "src/kernel/resource/VirtualMachineImpl.hpp"
#include "src/simgrid/module.hpp"
#include "src/simgrid/sg_config.hpp"
#include "xbt/asserts.hpp"
#include "xbt/log.h"

XBT_LOG_NEW_DEFAULT_SUBCATEGORY(ker_platform, kernel, "Kernel platform-related information");

namespace simgrid {

template class xbt::Extendable<kernel::routing::NetZoneImpl>;

namespace kernel::routing {

xbt::signal<void(bool symmetrical, kernel::routing::NetPoint* src, kernel::routing::NetPoint* dst,
                 kernel::routing::NetPoint* gw_src, kernel::routing::NetPoint* gw_dst,
                 std::vector<kernel::resource::StandardLinkImpl*> const& link_list)>
    NetZoneImpl::on_route_creation;

NetZoneImpl::NetZoneImpl(const std::string& name) : piface_(this), name_(name)
{
  auto* engine = s4u::Engine::get_instance();

  xbt_enforce(nullptr == engine->netpoint_by_name_or_null(get_name()),
             "Refusing to create a second NetZone called '%s'.", get_cname());
  netpoint_ = new NetPoint(name_, NetPoint::Type::NetZone);
  XBT_DEBUG("NetZone '%s' created with the id '%lu'", get_cname(), netpoint_->id());
  simgrid::s4u::NetZone::on_creation(piface_); // notify the signal
}

NetZoneImpl::~NetZoneImpl()
{
  for (auto const& nz : children_)
    delete nz;

  /* Since hosts_ and links_ are a std::map, the hosts are destroyed in the lexicographic order, which ensures that the
   * output is reproducible.
   */
  for (auto const& [_, host] : hosts_) {
    host->destroy();
  }
  hosts_.clear();
  for (auto const& [_, link] : links_) {
    link->destroy();
  }
  links_.clear();

  for (auto const& [_, route] : bypass_routes_)
    delete route;

  s4u::Engine::get_instance()->netpoint_unregister(netpoint_);
}

xbt_node_t NetZoneImpl::new_xbt_graph_node(const s_xbt_graph_t* graph, const char* name,
                                           std::map<std::string, xbt_node_t, std::less<>>* nodes)
{
  auto [elm, inserted] = nodes->try_emplace(name);
  if (inserted)
    elm->second = xbt_graph_new_node(graph, xbt_strdup(name));
  return elm->second;
}

xbt_edge_t NetZoneImpl::new_xbt_graph_edge(const s_xbt_graph_t* graph, xbt_node_t src, xbt_node_t dst,
                                           std::map<std::string, xbt_edge_t, std::less<>>* edges)
{
  const auto* src_name = static_cast<const char*>(xbt_graph_node_get_data(src));
  const auto* dst_name = static_cast<const char*>(xbt_graph_node_get_data(dst));

  auto elm = edges->find(std::string(src_name) + dst_name);
  if (elm == edges->end()) {
    bool inserted;
    std::tie(elm, inserted) = edges->try_emplace(std::string(dst_name) + src_name);
    if (inserted)
      elm->second = xbt_graph_new_edge(graph, src, dst, nullptr);
  }

  return elm->second;
}

void NetZoneImpl::add_child(NetZoneImpl* new_zone)
{
  xbt_enforce(not sealed_, "Cannot add a new child to the sealed zone %s", get_cname());
  /* set the parent behavior */
  hierarchy_ = RoutingMode::recursive;
  children_.push_back(new_zone);
}

/** @brief Returns the list of the hosts found in this NetZone (not recursively)
 *
 * Only the hosts that are directly contained in this NetZone are retrieved,
 * not the ones contained in sub-netzones.
 */
std::vector<s4u::Host*> NetZoneImpl::get_all_hosts() const
{
  return s4u::Engine::get_instance()->get_filtered_hosts(
      [this](const s4u::Host* host) { return host->get_impl()->get_englobing_zone() == this; });
}
size_t NetZoneImpl::get_host_count() const
{
  return get_all_hosts().size();
}

std::vector<s4u::Link*> NetZoneImpl::get_filtered_links(const std::function<bool(s4u::Link*)>& filter) const
{
  std::vector<s4u::Link*> filtered_list;
  for (auto const& [_, link] : links_) {
    s4u::Link* l = link->get_iface();
    if (filter(l))
      filtered_list.push_back(l);
  }

  for (const auto* child : children_) {
    auto child_links = child->get_filtered_links(filter);
    filtered_list.insert(filtered_list.end(), std::make_move_iterator(child_links.begin()),
                         std::make_move_iterator(child_links.end()));
  }
  return filtered_list;
}

std::vector<s4u::Link*> NetZoneImpl::get_all_links() const
{
  return get_filtered_links([](const s4u::Link*) { return true; });
}

size_t NetZoneImpl::get_link_count() const
{
  size_t total = links_.size();
  for (const auto* child : children_) {
    total += child->get_link_count();
  }
  return total;
}

s4u::Host* NetZoneImpl::add_host(const std::string& name, const std::vector<double>& speed_per_pstate)
{
  xbt_enforce(cpu_model_pm_,
             "Impossible to create host: %s. Invalid CPU model: nullptr. Have you set the parent of this NetZone: %s?",
             name.c_str(), get_cname());
  xbt_enforce(not sealed_, "Impossible to create host: %s. NetZone %s already sealed", name.c_str(), get_cname());
  auto* host   = (new resource::HostImpl(name))->set_englobing_zone(this);
  hosts_[name] = host;
  host->get_iface()->set_netpoint((new NetPoint(name, NetPoint::Type::Host))->set_englobing_zone(this));

  cpu_model_pm_->create_cpu(host->get_iface(), speed_per_pstate);

  return host->get_iface();
}

resource::StandardLinkImpl* NetZoneImpl::do_create_link(const std::string& name, const std::vector<double>& bandwidths)
{
  return network_model_->create_link(name, bandwidths);
}

s4u::Link* NetZoneImpl::add_link(const std::string& name, const std::vector<double>& bandwidths)
{
  xbt_enforce(
      network_model_,
      "Impossible to create link: %s. Invalid network model: nullptr. Have you set the parent of this NetZone: %s?",
      name.c_str(), get_cname());
  xbt_enforce(not sealed_, "Impossible to create link: %s. NetZone %s already sealed", name.c_str(), get_cname());
  links_[name] = do_create_link(name, bandwidths)->set_englobing_zone(this);
  return links_[name]->get_iface();
}

s4u::SplitDuplexLink* NetZoneImpl::add_split_duplex_link(const std::string& name, const std::vector<double>& bw_up,
                                                            const std::vector<double>& bw_down)
{
  xbt_enforce(
      network_model_,
      "Impossible to create link: %s. Invalid network model: nullptr. Have you set the parent of this NetZone: %s?",
      name.c_str(), get_cname());
  xbt_enforce(not sealed_, "Impossible to create link: %s. NetZone %s already sealed", name.c_str(), get_cname());

  auto* link_up             = add_link(name + "_UP", bw_up)->get_impl()->set_englobing_zone(this);
  auto* link_down           = add_link(name + "_DOWN", bw_down)->get_impl()->set_englobing_zone(this);
  split_duplex_links_[name] = std::make_unique<resource::SplitDuplexLinkImpl>(name, link_up, link_down);
  return split_duplex_links_[name]->get_iface();
}

s4u::Disk* NetZoneImpl::add_disk(const std::string& name, double read_bandwidth, double write_bandwidth)
{
  xbt_enforce(disk_model_,
             "Impossible to create disk: %s. Invalid disk model: nullptr. Have you set the parent of this NetZone: %s?",
             name.c_str(), get_cname());
  xbt_enforce(not sealed_, "Impossible to create disk: %s. NetZone %s already sealed", name.c_str(), get_cname());
  auto* l = disk_model_->create_disk(name, read_bandwidth, write_bandwidth);

  return l->get_iface();
}

NetPoint* NetZoneImpl::add_router(const std::string& name)
{
  xbt_enforce(nullptr == s4u::Engine::get_instance()->netpoint_by_name_or_null(name),
             "Refusing to create a router named '%s': this name already describes a node.", name.c_str());
  xbt_enforce(not sealed_, "Impossible to create router: %s. NetZone %s already sealed", name.c_str(), get_cname());

  return (new NetPoint(name, NetPoint::Type::Router))->set_englobing_zone(this);
}

unsigned long NetZoneImpl::add_component(NetPoint* elm)
{
  vertices_.push_back(elm);
  return vertices_.size() - 1; // The rank of the newly created object
}

std::vector<resource::StandardLinkImpl*> NetZoneImpl::get_link_list_impl(const std::vector<s4u::LinkInRoute>& link_list,
                                                                         bool backroute) const
{
  std::vector<resource::StandardLinkImpl*> links;

  for (const auto& link : link_list) {
    if (link.get_link()->get_sharing_policy() != s4u::Link::SharingPolicy::SPLITDUPLEX) {
      links.push_back(link.get_link()->get_impl());
      continue;
    }
    // split-duplex links
    const auto* sd_link = dynamic_cast<const s4u::SplitDuplexLink*>(link.get_link());
    xbt_enforce(sd_link,
               "Add_route: cast to SpliDuplexLink impossible. This should not happen, please contact SimGrid team");
    resource::StandardLinkImpl* link_impl;
    switch (link.get_direction()) {
      case s4u::LinkInRoute::Direction::UP:
        if (backroute)
          link_impl = sd_link->get_link_down()->get_impl();
        else
          link_impl = sd_link->get_link_up()->get_impl();
        break;
      case s4u::LinkInRoute::Direction::DOWN:
        if (backroute)
          link_impl = sd_link->get_link_up()->get_impl();
        else
          link_impl = sd_link->get_link_down()->get_impl();
        break;
      default:
        throw std::invalid_argument("Invalid add_route. Split-Duplex link without a direction: " +
                                    link.get_link()->get_name());
    }
    links.push_back(link_impl);
  }
  return links;
}

resource::StandardLinkImpl* NetZoneImpl::get_link_by_name_or_null(const std::string& name) const
{
  if (auto link_it = links_.find(name); link_it != links_.end())
    return link_it->second;

  for (const auto* child : children_) {
    if (auto* link = child->get_link_by_name_or_null(name))
      return link;
  }

  return nullptr;
}

resource::SplitDuplexLinkImpl* NetZoneImpl::get_split_duplex_link_by_name_or_null(const std::string& name) const
{
  if (auto link_it = split_duplex_links_.find(name); link_it != split_duplex_links_.end())
    return link_it->second.get();

  for (const auto* child : children_) {
    if (auto* link = child->get_split_duplex_link_by_name_or_null(name))
      return link;
  }

  return nullptr;
}

resource::HostImpl* NetZoneImpl::get_host_by_name_or_null(const std::string& name) const
{
  if (auto host_it = hosts_.find(name); host_it != hosts_.end())
    return host_it->second;

  for (const auto* child : children_) {
    if (auto* host = child->get_host_by_name_or_null(name))
      return host;
  }

  return nullptr;
}

std::vector<s4u::Host*> NetZoneImpl::get_filtered_hosts(const std::function<bool(s4u::Host*)>& filter) const
{
  std::vector<s4u::Host*> filtered_list;
  for (auto const& [_, host] : hosts_) {
    s4u::Host* h = host->get_iface();
    if (filter(h))
      filtered_list.push_back(h);
    /* Engine::get_hosts returns the VMs too */
    for (auto* vm : h->get_impl()->get_vms()) {
      if (filter(vm))
        filtered_list.push_back(vm);
    }
  }

  for (const auto* child : children_) {
    auto child_links = child->get_filtered_hosts(filter);
    filtered_list.insert(filtered_list.end(), std::make_move_iterator(child_links.begin()),
                         std::make_move_iterator(child_links.end()));
  }
  return filtered_list;
}

void NetZoneImpl::add_route(NetPoint* /*src*/, NetPoint* /*dst*/, NetPoint* /*gw_src*/, NetPoint* /*gw_dst*/,
                            const std::vector<s4u::LinkInRoute>& /*link_list_*/, bool /*symmetrical*/)
{
  xbt_die("NetZone '%s' does not accept new routes (wrong class).", get_cname());
}

void NetZoneImpl::add_bypass_route(NetPoint* src, NetPoint* dst, NetPoint* gw_src, NetPoint* gw_dst,
                                   const std::vector<s4u::LinkInRoute>& link_list)
{
  /* Argument validity checks */
  if (gw_dst) {
    XBT_DEBUG("Load bypassNetzoneRoute from %s@%s to %s@%s", src->get_cname(), gw_src->get_cname(), dst->get_cname(),
              gw_dst->get_cname());
    xbt_enforce(not link_list.empty(), "Bypass route between %s@%s and %s@%s cannot be empty.", src->get_cname(),
               gw_src->get_cname(), dst->get_cname(), gw_dst->get_cname());
    xbt_enforce(bypass_routes_.find({src, dst}) == bypass_routes_.end(),
               "The bypass route between %s@%s and %s@%s already exists.", src->get_cname(), gw_src->get_cname(),
               dst->get_cname(), gw_dst->get_cname());
  } else {
    XBT_DEBUG("Load bypassRoute from %s to %s", src->get_cname(), dst->get_cname());
    xbt_enforce(not link_list.empty(), "Bypass route between %s and %s cannot be empty.", src->get_cname(),
               dst->get_cname());
    xbt_enforce(bypass_routes_.find({src, dst}) == bypass_routes_.end(),
               "The bypass route between %s and %s already exists.", src->get_cname(), dst->get_cname());
  }

  /* Build a copy that will be stored in the dict */
  auto* newRoute = new BypassRoute(gw_src, gw_dst);
  auto converted_list = get_link_list_impl(link_list, false);
  newRoute->links.insert(newRoute->links.end(), begin(converted_list), end(converted_list));

  /* Store it */
  bypass_routes_.try_emplace({src, dst}, newRoute);
}

/** @brief Get the common ancestor and its first children in each line leading to src and dst
 *
 * In the recursive case, this sets common_ancestor, src_ancestor and dst_ancestor are set as follows.
 * @verbatim
 *         platform root
 *               |
 *              ...                <- possibly long path
 *               |
 *         common_ancestor
 *           /        \
 *          /          \
 *         /            \          <- direct links
 *        /              \
 *       /                \
 *  src_ancestor     dst_ancestor  <- must be different in the recursive case
 *      |                   |
 *     ...                 ...     <-- possibly long paths (one hop or more)
 *      |                   |
 *     src                 dst
 *  @endverbatim
 *
 *  In the base case (when src and dst are in the same netzone), things are as follows:
 *  @verbatim
 *                  platform root
 *                        |
 *                       ...                      <-- possibly long path
 *                        |
 * common_ancestor==src_ancestor==dst_ancestor    <-- all the same value
 *                   /        \
 *                  /          \                  <-- direct links (exactly one hop)
 *                 /            \
 *              src              dst
 *  @endverbatim
 *
 * A specific recursive case occurs when src is the ancestor of dst. In this case,
 * the base case routing should be used so the common_ancestor is specifically set
 * to src_ancestor==dst_ancestor.
 * Naturally, things are completely symmetrical if dst is the ancestor of src.
 * @verbatim
 *            platform root
 *                  |
 *                 ...                <-- possibly long path
 *                  |
 *  src == src_ancestor==dst_ancestor==common_ancestor <-- same value
 *                  |
 *                 ...                <-- possibly long path (one hop or more)
 *                  |
 *                 dst
 *  @endverbatim
 */
static void find_common_ancestors(const NetPoint* src, const NetPoint* dst,
                                  /* OUT */ NetZoneImpl** common_ancestor, NetZoneImpl** src_ancestor,
                                  NetZoneImpl** dst_ancestor)
{
  /* Deal with the easy base case */
  if (src->get_englobing_zone() == dst->get_englobing_zone()) {
    *common_ancestor = src->get_englobing_zone();
    *src_ancestor    = *common_ancestor;
    *dst_ancestor    = *common_ancestor;
    return;
  }

  /* engage the full recursive search */

  /* (1) find the path to root of src and dst*/
  const NetZoneImpl* src_as = src->get_englobing_zone();
  const NetZoneImpl* dst_as = dst->get_englobing_zone();

  xbt_enforce(src_as, "Host %s must be in a netzone", src->get_cname());
  xbt_enforce(dst_as, "Host %s must be in a netzone", dst->get_cname());

  /* (2) find the path to the root routing component */
  std::vector<NetZoneImpl*> path_src;
  NetZoneImpl* current = src->get_englobing_zone();
  while (current != nullptr) {
    path_src.push_back(current);
    current = current->get_parent();
  }
  std::vector<NetZoneImpl*> path_dst;
  current = dst->get_englobing_zone();
  while (current != nullptr) {
    path_dst.push_back(current);
    current = current->get_parent();
  }

  /* (3) find the common parent.
   * Before that, index_src and index_dst may be different, they both point to nullptr in path_src/path_dst
   * So we move them down simultaneously as long as they point to the same content.
   *
   * This works because all SimGrid platform have a unique root element (that is the last element of both paths).
   */
  NetZoneImpl* parent = nullptr; // the netzone we dropped on the previous loop iteration
  while (path_src.size() > 1 && path_dst.size() > 1 && path_src.back() == path_dst.back()) {
    parent = path_src.back();
    path_src.pop_back();
    path_dst.pop_back();
  }

  /* (4) we found the difference at least. Finalize the returned values */
  *src_ancestor = path_src.back();                  /* the first different parent of src */
  *dst_ancestor = path_dst.back();                  /* the first different parent of dst */
  if (*src_ancestor == *dst_ancestor) {             // src is the ancestor of dst, or the contrary
    *common_ancestor = *src_ancestor;
  } else {
    xbt_enforce(parent != nullptr);
    *common_ancestor = parent;
  }
}

/* PRECONDITION: this is the common ancestor of src and dst */
bool NetZoneImpl::get_bypass_route(const NetPoint* src, const NetPoint* dst,
                                   /* OUT */ std::vector<resource::StandardLinkImpl*>& links, double* latency,
                                   std::unordered_set<NetZoneImpl*>& netzones)
{
  // If never set a bypass route return nullptr without any further computations
  if (bypass_routes_.empty())
    return false;

  /* Base case, no recursion is needed */
  if (dst->get_englobing_zone() == this && src->get_englobing_zone() == this) {
    if (bypass_routes_.find({src, dst}) != bypass_routes_.end()) {
      const BypassRoute* bypassedRoute = bypass_routes_.at({src, dst});
      add_link_latency(links, bypassedRoute->links, latency);
      XBT_DEBUG("Found a bypass route from '%s' to '%s' with %zu links", src->get_cname(), dst->get_cname(),
                bypassedRoute->links.size());
      return true;
    }
    return false;
  }

  /* Engage recursive search */

  /* (1) find the path to the root routing component */
  std::vector<NetZoneImpl*> path_src;
  NetZoneImpl* current = src->get_englobing_zone();
  while (current != nullptr) {
    path_src.push_back(current);
    current = current->parent_;
  }

  std::vector<NetZoneImpl*> path_dst;
  current = dst->get_englobing_zone();
  while (current != nullptr) {
    path_dst.push_back(current);
    current = current->parent_;
  }

  /* (2) find the common parent */
  while (path_src.size() > 1 && path_dst.size() > 1 && path_src.back() == path_dst.back()) {
    path_src.pop_back();
    path_dst.pop_back();
  }

  /* (3) Search for a bypass making the path up to the ancestor useless */
  const BypassRoute* bypassedRoute = nullptr;
  std::pair<kernel::routing::NetPoint*, kernel::routing::NetPoint*> key;
  // Search for a bypass with the given indices. Returns true if found. Initialize variables `bypassedRoute' and `key'.
  auto lookup = [&bypassedRoute, &key, &path_src, &path_dst, this](unsigned src_index, unsigned dst_index) {
    if (src_index < path_src.size() && dst_index < path_dst.size()) {
      key      = {path_src[src_index]->netpoint_, path_dst[dst_index]->netpoint_};
      auto bpr = bypass_routes_.find(key);
      if (bpr != bypass_routes_.end()) {
        bypassedRoute = bpr->second;
        return true;
      }
    }
    return false;
  };

  for (unsigned max = 0, max_index = std::max(path_src.size(), path_dst.size()); max < max_index; max++) {
    for (unsigned i = 0; i < max; i++) {
      if (lookup(i, max) || lookup(max, i))
        break;
    }
    if (bypassedRoute || lookup(max, max))
      break;
  }

  /* (4) If we have the bypass, use it. If not, caller will do the Right Thing. */
  if (bypassedRoute) {
    XBT_DEBUG("Found a bypass route from '%s' to '%s' with %zu links. We may have to complete it with recursive "
              "calls to getRoute",
              src->get_cname(), dst->get_cname(), bypassedRoute->links.size());
    if (src != key.first)
      get_global_route_with_netzones(src, bypassedRoute->gw_src, links, latency, netzones);
    add_link_latency(links, bypassedRoute->links, latency);
    if (dst != key.second)
      get_global_route_with_netzones(bypassedRoute->gw_dst, dst, links, latency, netzones);
    return true;
  }
  XBT_DEBUG("No bypass route from '%s' to '%s'.", src->get_cname(), dst->get_cname());
  return false;
}

void NetZoneImpl::get_global_route(const NetPoint* src, const NetPoint* dst,
                                   /* OUT */ std::vector<resource::StandardLinkImpl*>& links, double* latency)
{
  std::unordered_set<NetZoneImpl*> netzones;
  get_global_route_with_netzones(src, dst, links, latency, netzones);
}

void NetZoneImpl::get_global_route_with_netzones(const NetPoint* src, const NetPoint* dst,
                                                 /* OUT */ std::vector<resource::StandardLinkImpl*>& links,
                                                 double* latency, std::unordered_set<NetZoneImpl*>& netzones)
{
  Route route;

  XBT_DEBUG("Resolve route from '%s' to '%s'", src->get_cname(), dst->get_cname());

  /* Find how src and dst are interconnected */
  NetZoneImpl* common_ancestor;
  NetZoneImpl* src_ancestor;
  NetZoneImpl* dst_ancestor;
  find_common_ancestors(src, dst, &common_ancestor, &src_ancestor, &dst_ancestor);
  XBT_DEBUG("find_common_ancestors: common ancestor '%s' src ancestor '%s' dst ancestor '%s'",
            common_ancestor->get_cname(), src_ancestor->get_cname(), dst_ancestor->get_cname());

  netzones.insert(src->get_englobing_zone());
  netzones.insert(dst->get_englobing_zone());
  netzones.insert(common_ancestor);
  /* Check whether a direct bypass is defined. If so, use it and bail out */
  if (common_ancestor->get_bypass_route(src, dst, links, latency, netzones))
    return;

  /* If src and dst are in the same netzone, life is good */
  if (src_ancestor == dst_ancestor) { /* ROUTING_BASE */
    route.link_list_ = std::move(links);

    xbt_assert(src->get_englobing_zone() == common_ancestor,
               "Source host %s is not part of the zone %s but of zone %s, please report that bug.", src->get_cname(),
               common_ancestor->get_cname(), src->get_englobing_zone()->get_cname());
    xbt_assert(dst->get_englobing_zone() == common_ancestor,
               "Destination host %s is not part of the zone %s but of zone %s, please report that bug.",
               dst->get_cname(), common_ancestor->get_cname(), dst->get_englobing_zone()->get_cname());

    common_ancestor->get_local_route(src, dst, &route, latency);
    links = std::move(route.link_list_);
    return;
  }

  /* Not in the same netzone, no bypass. We'll have to find our path between the netzones recursively */
  common_ancestor->get_local_route(src_ancestor->netpoint_, dst_ancestor->netpoint_, &route, latency);
  xbt_enforce((route.gw_src_ != nullptr) && (route.gw_dst_ != nullptr), "Bad gateways for route from '%s' to '%s'.",
             src->get_cname(), dst->get_cname());

  /* If source gateway is not our source, we have to recursively find our way up to this point */
  if (src != route.gw_src_)
    get_global_route_with_netzones(src, route.gw_src_, links, latency, netzones);
  links.insert(links.end(), begin(route.link_list_), end(route.link_list_));

  /* If dest gateway is not our destination, we have to recursively find our way from this point */
  if (route.gw_dst_ != dst)
    get_global_route_with_netzones(route.gw_dst_, dst, links, latency, netzones);
}

void NetZoneImpl::get_graph(const s_xbt_graph_t* graph, std::map<std::string, xbt_node_t, std::less<>>* nodes,
                            std::map<std::string, xbt_edge_t, std::less<>>* edges)
{
  std::vector<NetPoint*> vertices = get_vertices();

  for (auto const* my_src : vertices) {
    for (auto const* my_dst : vertices) {
      if (my_src == my_dst)
        continue;

      Route route;

      get_local_route(my_src, my_dst, &route, nullptr);

      XBT_DEBUG("get_route_and_latency %s -> %s", my_src->get_cname(), my_dst->get_cname());

      xbt_node_t current;
      xbt_node_t previous;
      const char* previous_name;
      const char* current_name;

      if (route.gw_src_) {
        previous      = new_xbt_graph_node(graph, route.gw_src_->get_cname(), nodes);
        previous_name = route.gw_src_->get_cname();
      } else {
        previous      = new_xbt_graph_node(graph, my_src->get_cname(), nodes);
        previous_name = my_src->get_cname();
      }

      for (auto const& link : route.link_list_) {
        const char* link_name = link->get_cname();
        current               = new_xbt_graph_node(graph, link_name, nodes);
        current_name          = link_name;
        new_xbt_graph_edge(graph, previous, current, edges);
        XBT_DEBUG("  %s -> %s", previous_name, current_name);
        previous      = current;
        previous_name = current_name;
      }

      if (route.gw_dst_) {
        current      = new_xbt_graph_node(graph, route.gw_dst_->get_cname(), nodes);
        current_name = route.gw_dst_->get_cname();
      } else {
        current      = new_xbt_graph_node(graph, my_dst->get_cname(), nodes);
        current_name = my_dst->get_cname();
      }
      new_xbt_graph_edge(graph, previous, current, edges);
      XBT_DEBUG("  %s -> %s", previous_name, current_name);
    }
  }
}

void NetZoneImpl::set_gateway(const std::string& name, NetPoint* router)
{
  xbt_enforce(not sealed_, "Impossible to create gateway: %s. NetZone %s already sealed", name.c_str(), get_cname());
  if (auto gateway_it = gateways_.find(name); gateway_it != gateways_.end())
    xbt_die("Impossible to create a gateway named %s. It already exists", name.c_str());
  else
    gateways_[name] = router;
}

NetPoint* NetZoneImpl::get_gateway() const
{
  xbt_enforce(not gateways_.empty(), "No default gateway has been defined for NetZone '%s'. Try to seal it first", get_cname());
  xbt_enforce(gateways_.size() < 2, "NetZone '%s' has more than one gateway, please provide a gateway name", get_cname());
  auto gateway_it = gateways_.find("default");
  xbt_enforce(gateway_it != gateways_.end(), "NetZone '%s' hasno default gateway, please define one", get_cname());
  return gateway_it->second;
}

void NetZoneImpl::seal()
{
  /* already sealed netzone */
  if (sealed_)
    return;
  do_seal(); // derived class' specific sealing procedure

  // for zone with a single host, this host is its own default gateway
  if (gateways_.empty() && hosts_.size() == 1)
    gateways_["default"] = hosts_.begin()->second->get_iface()->get_netpoint();

  /* seals sub-netzones and hosts */
  for (auto* host : get_all_hosts()) {
    host->seal();
  }

  /* sealing links */
  for (auto const& [_, link] : links_)
    link->get_iface()->seal();

  for (auto* sub_net : get_children()) {
    sub_net->seal();
  }
  sealed_ = true;
  s4u::NetZone::on_seal(piface_);
}

NetZoneImpl* NetZoneImpl::set_parent(NetZoneImpl* parent)
{
  xbt_enforce(not sealed_, "Impossible to set parent to an already sealed NetZone(%s)", this->get_cname());
  parent_ = parent;
  netpoint_->set_englobing_zone(parent_);
  if (parent) {
    /* adding this class as child */
    parent->add_child(this);
    /* copying models from parent host, to be reviewed when we allow multi-models */
    set_network_model(parent->get_network_model());
    set_cpu_pm_model(parent->get_cpu_pm_model());
    set_cpu_vm_model(parent->get_cpu_vm_model());
    set_disk_model(parent->get_disk_model());
    set_host_model(parent->get_host_model());
  }
  return this;
}

void NetZoneImpl::set_network_model(std::shared_ptr<resource::NetworkModel> netmodel)
{
  xbt_enforce(not sealed_, "Impossible to set network model to an already sealed NetZone(%s)", this->get_cname());
  network_model_ = std::move(netmodel);
}

void NetZoneImpl::set_cpu_vm_model(std::shared_ptr<resource::CpuModel> cpu_model)
{
  xbt_enforce(not sealed_, "Impossible to set CPU model to an already sealed NetZone(%s)", this->get_cname());
  cpu_model_vm_ = std::move(cpu_model);
}

void NetZoneImpl::set_cpu_pm_model(std::shared_ptr<resource::CpuModel> cpu_model)
{
  xbt_enforce(not sealed_, "Impossible to set CPU model to an already sealed NetZone(%s)", this->get_cname());
  cpu_model_pm_ = std::move(cpu_model);
}

void NetZoneImpl::set_disk_model(std::shared_ptr<resource::DiskModel> disk_model)
{
  xbt_enforce(not sealed_, "Impossible to set disk model to an already sealed NetZone(%s)", this->get_cname());
  disk_model_ = std::move(disk_model);
}

void NetZoneImpl::set_host_model(std::shared_ptr<resource::HostModel> host_model)
{
  xbt_enforce(not sealed_, "Impossible to set host model to an already sealed NetZone(%s)", this->get_cname());
  host_model_ = std::move(host_model);
}

const NetZoneImpl* NetZoneImpl::get_netzone_recursive(const NetPoint* netpoint) const
{
  xbt_enforce(netpoint && netpoint->is_netzone(), "Netpoint %s must be of the type NetZone",
             netpoint ? netpoint->get_cname() : "nullptr");

  if (netpoint == netpoint_)
    return this;

  for (const auto* children : children_) {
    const NetZoneImpl* netzone = children->get_netzone_recursive(netpoint);
    if (netzone)
      return netzone;
  }
  return nullptr;
}

bool NetZoneImpl::is_component_recursive(const NetPoint* netpoint) const
{
  /* check direct components */
  if (std::any_of(begin(vertices_), end(vertices_), [netpoint](const auto* elem) { return elem == netpoint; }))
    return true;

  /* check childrens */
  return std::any_of(begin(children_), end(children_),
                     [netpoint](const auto* child) { return child->is_component_recursive(netpoint); });
}

} // namespace kernel::routing
} // namespace simgrid
