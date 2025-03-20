/* Copyright (c) 2019-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#ifndef DISK_IMPL_HPP_
#define DISK_IMPL_HPP_

#include "simgrid/kernel/resource/Action.hpp"
#include "simgrid/kernel/resource/Model.hpp"
#include "simgrid/s4u/Disk.hpp"
#include "simgrid/s4u/Io.hpp"
#include "src/kernel/resource/Resource.hpp"
#include "xbt/PropertyHolder.hpp"

#include <map>

namespace simgrid::kernel::resource {
/***********
 * Classes *
 ***********/

class DiskAction;

/*********
 * Model *
 *********/
class DiskModel : public Model {
public:
  using Model::Model;

  virtual DiskImpl* create_disk(const std::string& name, double read_bandwidth, double write_bandwidth) = 0;
};

/************
 * Resource *
 ************/
class DiskImpl : public Resource_T<DiskImpl>, public xbt::PropertyHolder {
  s4u::Disk piface_;
  s4u::Host* host_                   = nullptr;
  lmm::Constraint* constraint_write_ = nullptr; /* Constraint for maximum write bandwidth*/
  lmm::Constraint* constraint_read_  = nullptr; /* Constraint for maximum read bandwidth*/
  std::unordered_map<s4u::Disk::Operation, s4u::Disk::SharingPolicy> sharing_policy_ = {
      {s4u::Disk::Operation::READ, s4u::Disk::SharingPolicy::LINEAR},
      {s4u::Disk::Operation::WRITE, s4u::Disk::SharingPolicy::LINEAR},
      {s4u::Disk::Operation::READWRITE, s4u::Disk::SharingPolicy::LINEAR}};
  std::unordered_map<s4u::Disk::Operation, s4u::NonLinearResourceCb> sharing_policy_cb_ = {};
  std::function<s4u::Disk::IoFactorCb> factor_cb_                                       = {};

  Metric read_bw_      = {0.0, 0, nullptr};
  Metric write_bw_     = {0.0, 0, nullptr};
  double readwrite_bw_ = -1; /* readwrite constraint bound, usually max(read, write) */
  std::atomic_int_fast32_t refcount_{0};

  void apply_sharing_policy_cfg();

protected:
  ~DiskImpl() override = default; // Disallow direct deletion. Call destroy() instead.

public:
  explicit DiskImpl(const std::string& name, double read_bandwidth, double write_bandwidth);
  DiskImpl(const DiskImpl&) = delete;
  DiskImpl& operator=(const DiskImpl&) = delete;
  friend void intrusive_ptr_add_ref(DiskImpl* disk)
  {
    disk->refcount_.fetch_add(1, std::memory_order_acq_rel);
  }
  friend void intrusive_ptr_release(DiskImpl* disk)
  {
    if (disk->refcount_.fetch_sub(1, std::memory_order_release) == 1) {
      std::atomic_thread_fence(std::memory_order_acquire);
      delete disk;
    }
  }

  /** @brief Public interface */
  const s4u::Disk* get_iface() const { return &piface_; }
  s4u::Disk* get_iface() { return &piface_; }
  DiskImpl* set_host(s4u::Host* host);
  s4u::Host* get_host() const { return host_; }

  void set_read_bandwidth(double value);
  double get_read_bandwidth() const { return read_bw_.peak * read_bw_.scale; }

  void set_write_bandwidth(double value);
  double get_write_bandwidth() const { return write_bw_.peak * write_bw_.scale; }

  void set_readwrite_bandwidth(double value);
  double get_readwrite_bandwidth() const { return readwrite_bw_; }

  DiskImpl* set_read_constraint(lmm::Constraint* constraint_read);
  lmm::Constraint* get_read_constraint() const { return constraint_read_; }

  DiskImpl* set_write_constraint(lmm::Constraint* constraint_write);
  lmm::Constraint* get_write_constraint() const { return constraint_write_; }

  profile::Event* get_read_event() const { return read_bw_.event; }
  void unref_read_event() { tmgr_trace_event_unref(&read_bw_.event); }

  profile::Event* get_write_event() const { return write_bw_.event; }
  void unref_write_event() { tmgr_trace_event_unref(&write_bw_.event); }

  DiskImpl* set_read_bandwidth_profile(profile::Profile* profile);
  DiskImpl* set_write_bandwidth_profile(profile::Profile* profile);

  void set_sharing_policy(s4u::Disk::Operation op, s4u::Disk::SharingPolicy policy, const s4u::NonLinearResourceCb& cb);
  s4u::Disk::SharingPolicy get_sharing_policy(s4u::Disk::Operation op) const;

  void set_factor_cb(const std::function<s4u::Disk::IoFactorCb>& cb);
  const std::function<s4u::Disk::IoFactorCb>& get_factor_cb() const { return factor_cb_; }

  void turn_on() override;
  void turn_off() override;

  void on_read_bandwidth_change() const;
  void on_write_bandwidth_change() const;

  void seal() override;
  void destroy(); // Must be called instead of the destructor

  virtual DiskAction* io_start(sg_size_t size, s4u::Io::OpType type) = 0;
};

/**********
 * Action *
 **********/

class DiskAction : public Action {
public:
  static xbt::signal<void(DiskAction const&, Action::State, Action::State)> on_state_change;

  using Action::Action;
  void set_state(simgrid::kernel::resource::Action::State state) override;
  void update_remains_lazy(double now) override;
};

} // namespace simgrid::kernel::resource
#endif /* DISK_IMPL_HPP_ */
