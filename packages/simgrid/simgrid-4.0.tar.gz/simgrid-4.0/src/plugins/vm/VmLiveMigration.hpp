/* Copyright (c) 2004-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "simgrid/s4u/Engine.hpp"
#include "simgrid/s4u/Mailbox.hpp"
#include "simgrid/s4u/VirtualMachine.hpp"

#ifndef VM_LIVE_MIGRATION_HPP_
#define VM_LIVE_MIGRATION_HPP_

namespace simgrid::plugin::vm {
class VmMigrationExt {
public:
  s4u::ActorPtr issuer_ = nullptr;
  s4u::ActorPtr tx_     = nullptr;
  s4u::ActorPtr rx_     = nullptr;
  static xbt::Extension<s4u::Host, VmMigrationExt> EXTENSION_ID;
  explicit VmMigrationExt(s4u::ActorPtr issuer, s4u::ActorPtr rx, s4u::ActorPtr tx) : issuer_(issuer), tx_(tx), rx_(rx)
  {
  }
  static void ensureVmMigrationExtInstalled();
};

class MigrationRx {
  /* The migration_rx process uses mbox_ctl to let the caller of do_migration()  know the completion of the migration.
   */
  s4u::Mailbox* mbox_ctl;
  /* The migration_rx and migration_tx processes use mbox to transfer migration data. */
  s4u::Mailbox* mbox;
  s4u::VirtualMachine* vm_;
  s4u::Host* src_pm_ = nullptr;
  s4u::Host* dst_pm_ = nullptr;

public:
  explicit MigrationRx(s4u::VirtualMachine* vm, s4u::Host* dst_pm) : vm_(vm), dst_pm_(dst_pm)
  {
    src_pm_ = vm_->get_pm();

    mbox_ctl = s4u::Mailbox::by_name("__mbox_mig_ctl:" + vm_->get_name() + "(" + src_pm_->get_name() + "-" +
                                     dst_pm_->get_name() + ")");
    mbox     = s4u::Mailbox::by_name("__mbox_mig_src_dst:" + vm_->get_name() + "(" + src_pm_->get_name() + "-" +
                                 dst_pm_->get_name() + ")");
  }
  void operator()();
};

class MigrationTx {
  /* The migration_rx and migration_tx processes use mbox to transfer migration data. */
  s4u::Mailbox* mbox;
  s4u::VirtualMachine* vm_;
  s4u::Host* src_pm_ = nullptr;
  s4u::Host* dst_pm_ = nullptr;

public:
  explicit MigrationTx(s4u::VirtualMachine* vm, s4u::Host* dst_pm) : vm_(vm), dst_pm_(dst_pm)
  {
    src_pm_ = vm_->get_pm();
    mbox    = s4u::Mailbox::by_name("__mbox_mig_src_dst:" + vm_->get_name() + "(" + src_pm_->get_name() + "-" +
                                 dst_pm_->get_name() + ")");
  }
  void operator()();
  sg_size_t sendMigrationData(sg_size_t size, int stage, int stage2_round, double mig_speed, double timeout);
};
} // namespace simgrid::plugin::vm
#endif
