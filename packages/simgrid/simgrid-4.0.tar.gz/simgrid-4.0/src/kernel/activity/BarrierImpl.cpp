/* Copyright (c) 2007-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "src/kernel/activity/BarrierImpl.hpp"

XBT_LOG_NEW_DEFAULT_SUBCATEGORY(ker_barrier, ker_synchro, "Barrier kernel-space implementation");

namespace simgrid::kernel::activity {

/* -------- Acquisition -------- */
bool BarrierAcquisitionImpl::test(actor::ActorImpl*)
{
  return granted_;
}
void BarrierAcquisitionImpl::wait_for(actor::ActorImpl* issuer, double timeout)
{
  xbt_assert(issuer == issuer_, "Cannot wait on acquisitions created by another actor (id %ld)", issuer_->get_pid());
  xbt_assert(timeout < 0, "Timeouts on barrier acquisitions are not implemented yet.");

  this->register_simcall(&issuer_->simcall_); // Block on that acquisition

  if (granted_) { // This was unblocked already
    finish();
  } else {
    // Already in the queue
  }
}

void BarrierAcquisitionImpl::finish()
{
  xbt_assert(simcalls_.size() == 1, "Unexpected number of simcalls waiting: %zu", simcalls_.size());
  auto issuer = unregister_first_simcall();
  issuer->simcall_answer();
}
/* -------- Barrier -------- */

unsigned BarrierImpl::next_id_ = 0;

BarrierAcquisitionImplPtr BarrierImpl::acquire_async(actor::ActorImpl* issuer)
{
  auto res = BarrierAcquisitionImplPtr(new kernel::activity::BarrierAcquisitionImpl(issuer, this), true);

  XBT_DEBUG("%s acquires barrier #%u (%zu of %u)", issuer->get_cname(), id_, ongoing_acquisitions_.size(),
            expected_actors_);
  if (ongoing_acquisitions_.size() < expected_actors_ - 1) {
    /* Not everybody arrived yet */
    ongoing_acquisitions_.push_back(res);

  } else {
    for (auto const& acqui : ongoing_acquisitions_) {
      acqui->granted_ = true;
      
      // Finish the acquisition if the owner is already blocked on its completion
      auto& synchros = acqui->get_issuer()->waiting_synchros_;
      if (std::find(synchros.begin(), synchros.end(), acqui) != synchros.end())
        acqui->finish();
      // else, the issuer is not blocked on this acquisition so no need to release it
    }
    ongoing_acquisitions_.clear(); // Rearm the barier for subsequent uses
    res->granted_ = true;
  }
  return res;
}

} // namespace simgrid::kernel::activity
