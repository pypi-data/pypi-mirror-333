/* Copyright (c) 2014-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#ifndef SIMGRID_MODEL_NETWORK_IB_HPP_
#define SIMGRID_MODEL_NETWORK_IB_HPP_

#include "src/kernel/resource/models/network_cm02.hpp"

#include <map>
#include <vector>

namespace simgrid::kernel::resource {

class XBT_PRIVATE IBNode;

struct XBT_PRIVATE ActiveComm {
  IBNode* destination   = nullptr;
  NetworkAction* action = nullptr;
  double init_rate      = -1;
};

class IBNode {
public:
  int id_;
  // store related links, to ease computation of the penalties
  std::vector<ActiveComm*> active_comms_up_;
  // store the number of comms received from each node
  std::map<IBNode*, int> active_comms_down_;
  // number of comms the node is receiving
  int nb_active_comms_down_ = 0;
  explicit IBNode(int id) : id_(id){};
};

class XBT_PRIVATE NetworkIBModel : public NetworkCm02Model {
  std::unordered_map<std::string, IBNode> active_nodes;
  std::unordered_map<NetworkAction*, std::pair<IBNode*, IBNode*>> active_comms;

  double Bs_;
  double Be_;
  double ys_;
  void update_IB_factors_rec(IBNode* root, std::vector<bool>& updatedlist) const;
  void compute_IB_factors(IBNode* root) const;

public:
  explicit NetworkIBModel(const std::string& name);
  NetworkIBModel(const NetworkIBModel&)            = delete;
  NetworkIBModel& operator=(const NetworkIBModel&) = delete;
  void update_IB_factors(NetworkAction* action, IBNode* from, IBNode* to, bool remove) const;

  static void IB_create_host_callback(s4u::Host const& host);
  static void IB_action_state_changed_callback(NetworkAction& action, Action::State /*previous*/);
  static void IB_comm_start_callback(const s4u::Comm& comm);
};
} // namespace simgrid::kernel::resource
#endif
