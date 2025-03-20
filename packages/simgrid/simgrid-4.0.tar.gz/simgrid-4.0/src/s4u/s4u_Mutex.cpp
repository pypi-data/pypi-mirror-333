/* Copyright (c) 2006-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include <simgrid/modelchecker.h>
#include <simgrid/mutex.h>
#include <simgrid/s4u/Mutex.hpp>

#include "src/kernel/activity/MutexImpl.hpp"
#include "src/kernel/actor/SynchroObserver.hpp"
#include "src/mc/mc_replay.hpp"

namespace simgrid::s4u {

/** @brief Blocks the calling actor until the mutex can be obtained */
void Mutex::lock()
{
  kernel::actor::ActorImpl* issuer = kernel::actor::ActorImpl::self();

  if (MC_is_active() || MC_record_replay_is_active()) { // Split in 2 simcalls for transition persistency
    kernel::actor::MutexObserver lock_observer{issuer, mc::Transition::Type::MUTEX_ASYNC_LOCK, pimpl_};
    auto acquisition =
        kernel::actor::simcall_answered([issuer, this] { return pimpl_->lock_async(issuer); }, &lock_observer);

    kernel::actor::MutexAcquisitionObserver wait_observer{issuer, mc::Transition::Type::MUTEX_WAIT, acquisition.get(),
                                                          -1};
    kernel::actor::simcall_blocking([issuer, &acquisition] { acquisition->wait_for(issuer, -1); }, &wait_observer);

  } else { // Do it in one simcall only
    // We don't need no observer on this non-MC path, but simcall_blocking() requires it.
    // Use a type clearly indicating it's NO-MC in the hope to get a loud error if it gets used despite our
    // expectations.
    kernel::actor::MutexAcquisitionObserver useless_observer{issuer, mc::Transition::Type::MUTEX_LOCK_NOMC, nullptr,
                                                             -1};
    kernel::actor::simcall_blocking([issuer, this] { pimpl_->lock_async(issuer)->wait_for(issuer, -1); },
                                    &useless_observer);
  }
}

/** @brief Release the ownership of the mutex, unleashing a blocked actor (if any)
 *
 * Will fail if the calling actor does not own the mutex.
 */
void Mutex::unlock()
{
  kernel::actor::ActorImpl* issuer = kernel::actor::ActorImpl::self();
  kernel::actor::MutexObserver observer{issuer, mc::Transition::Type::MUTEX_UNLOCK, pimpl_};
  kernel::actor::simcall_answered([this, issuer] { this->pimpl_->unlock(issuer); }, &observer);
}

/** @brief Acquire the mutex if it's free, and return false (without blocking) if not */
bool Mutex::try_lock()
{
  kernel::actor::ActorImpl* issuer = kernel::actor::ActorImpl::self();
  kernel::actor::MutexObserver observer{issuer, mc::Transition::Type::MUTEX_TRYLOCK, pimpl_};
  return kernel::actor::simcall_answered([&observer] { return observer.get_mutex()->try_lock(observer.get_issuer()); },
                                         &observer);
}

/** @brief Create a new mutex
 *
 * See @ref s4u_raii.
 */
MutexPtr Mutex::create(bool recursive)
{
  auto* mutex = new kernel::activity::MutexImpl(recursive);
  return MutexPtr(&mutex->get_iface(), false);
}

Actor* Mutex::get_owner()
{
  auto* owner = pimpl_->get_owner();
  if (owner == nullptr)
    return nullptr;
  return owner->get_ciface();
}

/* refcounting of the intrusive_ptr is delegated to the implementation object */
void intrusive_ptr_add_ref(const Mutex* mutex)
{
  intrusive_ptr_add_ref(mutex->pimpl_);
}
void intrusive_ptr_release(const Mutex* mutex)
{
  intrusive_ptr_release(mutex->pimpl_);
}

} // namespace simgrid::s4u

/* **************************** Public C interface *************************** */
sg_mutex_t sg_mutex_init()
{
  return simgrid::s4u::Mutex::create().detach();
}

void sg_mutex_lock(sg_mutex_t mutex)
{
  mutex->lock();
}

void sg_mutex_unlock(sg_mutex_t mutex)
{
  mutex->unlock();
}

int sg_mutex_try_lock(sg_mutex_t mutex)
{
  return mutex->try_lock();
}

void sg_mutex_destroy(const_sg_mutex_t mutex)
{
  intrusive_ptr_release(mutex);
}
