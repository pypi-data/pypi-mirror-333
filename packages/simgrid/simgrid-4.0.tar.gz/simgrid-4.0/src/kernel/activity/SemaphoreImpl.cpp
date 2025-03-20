/* Copyright (c) 2019-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include <simgrid/Exception.hpp>
#include <simgrid/s4u/Host.hpp>

#include "src/kernel/activity/SemaphoreImpl.hpp"
#include "src/kernel/actor/SynchroObserver.hpp"
#include "src/kernel/resource/CpuImpl.hpp"

#include <cmath> // std::isfinite
#include <string>

XBT_LOG_NEW_DEFAULT_SUBCATEGORY(ker_semaphore, ker_synchro, "Semaphore kernel-space implementation");

namespace simgrid::kernel::activity {

/* -------- Acquisition -------- */
SemAcquisitionImpl::SemAcquisitionImpl(actor::ActorImpl* issuer, SemaphoreImpl* sem) : issuer_(issuer), semaphore_(sem)
{
  set_name(std::string("on semaphore ") + std::to_string(sem->get_id()));
}

void SemAcquisitionImpl::wait_for(actor::ActorImpl* issuer, double timeout)
{
  xbt_assert(std::isfinite(timeout), "timeout is not finite!");
  xbt_assert(issuer == issuer_, "Cannot wait on acquisitions created by another actor (id %ld)", issuer_->get_pid());

  XBT_DEBUG("Wait semaphore %u (timeout:%f)", semaphore_->get_id(), timeout);

  this->register_simcall(&issuer_->simcall_); // Block on that acquisition

  if (granted_) {
    finish();
  } else if (timeout > 0) {
    model_action_ = get_issuer()->get_host()->get_cpu()->sleep(timeout);
    model_action_->set_activity(this);
  }

  // Already in the queue
}
void SemAcquisitionImpl::finish()
{
  if (model_action_ != nullptr) {                                          // A timeout was declared
    if (model_action_->get_state() == resource::Action::State::FINISHED) { // The timeout elapsed
      if (granted_) { // but we got the semaphore, just in time!
        set_state(State::DONE);

      } else { // we have to report that timeout
        cancel(); // Unregister the acquisition from the semaphore

        /* Return to the englobing simcall that the wait_for timeouted */
        auto* observer = dynamic_cast<kernel::actor::SemaphoreAcquisitionObserver*>(get_issuer()->simcall_.observer_);
        xbt_assert(observer != nullptr);
        observer->set_result(true);
      }
    }
    model_action_->unref();
    model_action_ = nullptr;
  }

  xbt_assert(simcalls_.size() == 1, "Unexpected number of simcalls waiting: %zu", simcalls_.size());
  auto issuer = unregister_first_simcall();
  if (issuer != nullptr) /* don't answer exiting and dying actors */
    issuer->simcall_answer();
}
void SemAcquisitionImpl::cancel()
{
  /* Remove myself from the list of interested parties */
  const auto* issuer = get_issuer();
  auto it     = std::find_if(semaphore_->ongoing_acquisitions_.begin(), semaphore_->ongoing_acquisitions_.end(),
                             [issuer](SemAcquisitionImplPtr acqui) { return acqui->get_issuer() == issuer; });
  xbt_assert(it != semaphore_->ongoing_acquisitions_.end(),
             "Cannot find myself in the waiting queue that I have to leave");
  semaphore_->ongoing_acquisitions_.erase(it);
  get_issuer()->activities_.erase(this); // The actor does not need to cancel the activity when it dies
}

/* -------- Semaphore -------- */
unsigned SemaphoreImpl::next_id_ = 0;

SemAcquisitionImplPtr SemaphoreImpl::acquire_async(actor::ActorImpl* issuer)
{
  auto res = SemAcquisitionImplPtr(new kernel::activity::SemAcquisitionImpl(issuer, this), true);

  if (value_ > 0) {
    value_--;
    res->granted_ = true;
  } else {
    /* No free token in the semaphore; register the acquisition */
    ongoing_acquisitions_.push_back(res);
  }
  return res;
}
void SemaphoreImpl::release()
{
  XBT_DEBUG("Sem release semaphore %u", get_id());

  if (not ongoing_acquisitions_.empty()) {
    /* Release the first waiting actor */

    auto acqui = ongoing_acquisitions_.front();
    ongoing_acquisitions_.pop_front();

    acqui->granted_ = true;

    // Finish the acquisition if the owner is already blocked on its completion
    auto& synchros = acqui->get_issuer()->waiting_synchros_;
    if (std::find(synchros.begin(), synchros.end(), acqui) != synchros.end())
      acqui->finish();
    // else, the issuer is not blocked on this acquisition so no need to release it

  } else {
    // nobody's waiting here
    value_++;
  }
}

} // namespace simgrid::kernel::activity
