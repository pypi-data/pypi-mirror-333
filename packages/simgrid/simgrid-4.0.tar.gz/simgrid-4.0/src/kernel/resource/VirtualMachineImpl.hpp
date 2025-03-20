/* Copyright (c) 2004-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include <simgrid/s4u/VirtualMachine.hpp>

#include "src/kernel/resource/HostImpl.hpp"

#ifndef VM_INTERFACE_HPP_
#define VM_INTERFACE_HPP_

namespace simgrid {

extern template class XBT_PUBLIC xbt::Extendable<kernel::resource::VirtualMachineImpl>;

namespace kernel::resource {

/************
 * Resource *
 ************/

class XBT_PUBLIC VirtualMachineImpl : public HostImpl, public xbt::Extendable<VirtualMachineImpl> {
#ifndef DOXYGEN
  friend s4u::VirtualMachine;
#endif

public:
  static std::deque<s4u::VirtualMachine*> allVms_;

  explicit VirtualMachineImpl(const std::string& name, s4u::VirtualMachine* piface, s4u::Host* host, int core_amount,
                              size_t ramsize);
  explicit VirtualMachineImpl(const std::string& name, simgrid::s4u::Host* host_PM, int core_amount, size_t ramsize);
  void set_piface(s4u::VirtualMachine* piface);

  void start();
  void suspend(const actor::ActorImpl* issuer);
  void resume();
  void shutdown(kernel::actor::ActorImpl* issuer);
  void vm_destroy();

  /** @brief Change the physical host on which the given VM is running */
  void set_physical_host(s4u::Host* dest);
  /** @brief Get the physical host on which the given VM is running */
  s4u::Host* get_physical_host() const { return physical_host_; }

  size_t get_ramsize() const { return ramsize_; }
  void set_ramsize(size_t ramsize) { ramsize_ = ramsize; }

  s4u::VirtualMachine::State get_state() const { return vm_state_; }
  void set_state(s4u::VirtualMachine::State state) { vm_state_ = state; }

  unsigned int get_core_amount() const { return core_amount_; }
  Action* get_action() const { return action_; }

  const s4u::VirtualMachine* get_iface() const override { return piface_; }
  s4u::VirtualMachine* get_iface() override { return piface_; }

  void set_bound(double bound);

  void update_action_weight();

  void add_active_exec() { active_execs_++; }
  void remove_active_exec() { active_execs_--; }

  void start_migration();
  void end_migration();
  bool is_migrating() const { return is_migrating_; }
  void seal() override;

private:
  s4u::VirtualMachine* piface_ = nullptr;
  Action* action_            = nullptr;
  unsigned int active_execs_ = 0;
  s4u::Host* physical_host_;
  unsigned int core_amount_;
  double user_bound_                   = std::numeric_limits<double>::max();
  size_t ramsize_                      = 0;
  s4u::VirtualMachine::State vm_state_ = s4u::VirtualMachine::State::CREATED;
  bool is_migrating_                   = false;
};

/*********
 * Model *
 *********/
/** @ingroup Model_vm_interface
 * @brief VM model interface class
 * @details A model is an object which handle the interactions between its Resources and its Actions
 */
class XBT_PRIVATE VMModel : public HostModel {
public:
  explicit VMModel(const std::string& name);

  double next_occurring_event(double now) override;
  void update_actions_state(double /*now*/, double /*delta*/) override{};
  Action* execute_thread(const s4u::Host* host, double flops_amount, int thread_count) override;
  Action* execute_parallel(const std::vector<s4u::Host*>& host_list, const double* flops_amount,
                           const double* bytes_amount, double rate) override
  {
    return nullptr;
  };
};
} // namespace kernel::resource
} // namespace simgrid

#endif /* VM_INTERFACE_HPP_ */
