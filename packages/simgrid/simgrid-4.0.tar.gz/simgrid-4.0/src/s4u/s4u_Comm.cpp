/* Copyright (c) 2006-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include <simgrid/Exception.hpp>
#include <simgrid/comm.h>
#include <simgrid/s4u/ActivitySet.hpp>
#include <simgrid/s4u/Comm.hpp>
#include <simgrid/s4u/Engine.hpp>
#include <simgrid/s4u/Mailbox.hpp>

#include "src/kernel/activity/CommImpl.hpp"
#include "src/kernel/actor/ActorImpl.hpp"
#include "src/kernel/actor/WaitTestObserver.hpp"
#include "src/mc/mc.h"
#include "src/mc/mc_replay.hpp"

#include <boost/core/demangle.hpp>
#include <cmath>

XBT_LOG_NEW_DEFAULT_SUBCATEGORY(s4u_comm, s4u_activity, "S4U asynchronous communications");

namespace simgrid::s4u {
xbt::signal<void(Comm const&)> Comm::on_send;
xbt::signal<void(Comm const&)> Comm::on_recv;

template <> xbt::signal<void(Comm&)> Activity_T<Comm>::on_veto             = xbt::signal<void(Comm&)>();
template <> xbt::signal<void(Comm const&)> Activity_T<Comm>::on_start      = xbt::signal<void(Comm const&)>();
template <> xbt::signal<void(Comm const&)> Activity_T<Comm>::on_completion = xbt::signal<void(Comm const&)>();
template <> xbt::signal<void(Comm const&)> Activity_T<Comm>::on_suspend    = xbt::signal<void(Comm const&)>();
template <> xbt::signal<void(Comm const&)> Activity_T<Comm>::on_resume     = xbt::signal<void(Comm const&)>();
template <> void Activity_T<Comm>::fire_on_start() const
{
  on_start(static_cast<const Comm&>(*this));
}
template <> void Activity_T<Comm>::fire_on_completion() const
{
  on_completion(static_cast<const Comm&>(*this));
}
template <> void Activity_T<Comm>::fire_on_suspend() const
{
  on_suspend(static_cast<const Comm&>(*this));
}
template <> void Activity_T<Comm>::fire_on_resume() const
{
  on_resume(static_cast<const Comm&>(*this));
}
template <> void Activity_T<Comm>::fire_on_veto()
{
  on_veto(static_cast<Comm&>(*this));
}
template <> void Activity_T<Comm>::on_start_cb(const std::function<void(Comm const&)>& cb)
{
  on_start.connect(cb);
}
template <> void Activity_T<Comm>::on_completion_cb(const std::function<void(Comm const&)>& cb)
{
  on_completion.connect(cb);
}
template <> void Activity_T<Comm>::on_suspend_cb(const std::function<void(Comm const&)>& cb)
{
  on_suspend.connect(cb);
}
template <> void Activity_T<Comm>::on_resume_cb(const std::function<void(Comm const&)>& cb)
{
  on_resume.connect(cb);
}
template <> void Activity_T<Comm>::on_veto_cb(const std::function<void(Comm&)>& cb)
{
  on_veto.connect(cb);
}

void Comm::fire_on_completion_for_real() const
{
  Activity_T<Comm>::fire_on_completion();
}
void Comm::fire_on_this_completion_for_real() const
{
  Activity_T<Comm>::fire_on_this_completion();
}

CommPtr Comm::set_copy_data_callback(const std::function<void(kernel::activity::CommImpl*, void*, size_t)>& callback)
{
  copy_data_function_ = callback;
  return this;
}

Comm::~Comm()
{
  if (state_ == State::STARTED && not detached_ &&
      (pimpl_ == nullptr || pimpl_->get_state() == kernel::activity::State::RUNNING)) {
    XBT_INFO("Comm %p freed before its completion. Did you forget to detach it? (state: %s)", this, get_state_str());
    if (pimpl_ != nullptr)
      XBT_INFO("pimpl_->state: %s", pimpl_->get_state_str());
    else
      XBT_INFO("pimpl_ is null");
    xbt_backtrace_display_current();
  }
}

void Comm::send(kernel::actor::ActorImpl* sender, const Mailbox* mbox, double task_size, double rate, void* src_buff,
                size_t src_buff_size,
                const std::function<bool(void*, void*, simgrid::kernel::activity::CommImpl*)>& match_fun,
                const std::function<void(simgrid::kernel::activity::CommImpl*, void*, size_t)>& copy_data_fun,
                void* data, double timeout)
{
  /* checking for infinite values */
  xbt_assert(std::isfinite(task_size), "task_size is not finite!");
  xbt_assert(std::isfinite(rate), "rate is not finite!");
  xbt_assert(std::isfinite(timeout), "timeout is not finite!");

  xbt_assert(mbox, "No rendez-vous point defined for send");

  if (MC_is_active() || MC_record_replay_is_active()) {
    /* the model-checker wants two separate simcalls, and wants comm to be nullptr during the simcall */
    simgrid::kernel::activity::ActivityImplPtr comm = nullptr;

    simgrid::kernel::actor::CommIsendSimcall send_observer{
        sender,        mbox->get_impl(), task_size, rate,          static_cast<unsigned char*>(src_buff),
        src_buff_size, match_fun,        nullptr,   copy_data_fun, data,
        false,         "Isend"};
    comm = simgrid::kernel::actor::simcall_answered(
        [&send_observer] { return simgrid::kernel::activity::CommImpl::isend(&send_observer); }, &send_observer);

    if (simgrid::kernel::actor::ActivityWaitSimcall wait_observer{sender, comm.get(), timeout, "Wait"};
        simgrid::kernel::actor::simcall_blocking(
            [&wait_observer] {
              wait_observer.get_activity()->wait_for(wait_observer.get_issuer(), wait_observer.get_timeout());
            },
            &wait_observer)) {
      throw simgrid::TimeoutException(XBT_THROW_POINT, "Timeouted");
    }
    comm = nullptr;
  } else {
    simgrid::kernel::actor::CommIsendSimcall observer(sender, mbox->get_impl(), task_size, rate,
                                                      static_cast<unsigned char*>(src_buff), src_buff_size, match_fun,
                                                      nullptr, copy_data_fun, data, false, "Isend");
    simgrid::kernel::actor::simcall_blocking<void>(
        [&observer, timeout] {
          simgrid::kernel::activity::ActivityImplPtr comm = simgrid::kernel::activity::CommImpl::isend(&observer);
          comm->wait_for(observer.get_issuer(), timeout);
        },
        &observer);
  }
}

void Comm::recv(kernel::actor::ActorImpl* receiver, const Mailbox* mbox, void* dst_buff, size_t* dst_buff_size,
                const std::function<bool(void*, void*, simgrid::kernel::activity::CommImpl*)>& match_fun,
                const std::function<void(simgrid::kernel::activity::CommImpl*, void*, size_t)>& copy_data_fun,
                void* data, double timeout, double rate)
{
  xbt_assert(std::isfinite(timeout), "timeout is not finite!");
  xbt_assert(mbox, "No rendez-vous point defined for recv");

  if (MC_is_active() || MC_record_replay_is_active()) {
    /* the model-checker wants two separate simcalls, and wants comm to be nullptr during the simcall */
    simgrid::kernel::activity::ActivityImplPtr comm = nullptr;

    simgrid::kernel::actor::CommIrecvSimcall observer{receiver,
                                                      mbox->get_impl(),
                                                      static_cast<unsigned char*>(dst_buff),
                                                      dst_buff_size,
                                                      match_fun,
                                                      copy_data_fun,
                                                      data,
                                                      rate,
                                                      "Irecv"};
    comm = simgrid::kernel::actor::simcall_answered(
        [&observer] { return simgrid::kernel::activity::CommImpl::irecv(&observer); }, &observer);

    if (simgrid::kernel::actor::ActivityWaitSimcall wait_observer{receiver, comm.get(), timeout, "wait"};
        simgrid::kernel::actor::simcall_blocking(
            [&wait_observer] {
              wait_observer.get_activity()->wait_for(wait_observer.get_issuer(), wait_observer.get_timeout());
            },
            &wait_observer)) {
      throw simgrid::TimeoutException(XBT_THROW_POINT, "Timeouted");
    }
    comm = nullptr;
  } else { // Non-MC path
    simgrid::kernel::actor::CommIrecvSimcall observer(receiver, mbox->get_impl(), static_cast<unsigned char*>(dst_buff),
                                                      dst_buff_size, match_fun, copy_data_fun, data, rate, "Irecv");
    simgrid::kernel::actor::simcall_blocking<void>(
        [&observer, timeout] {
          simgrid::kernel::activity::ActivityImplPtr comm = simgrid::kernel::activity::CommImpl::irecv(&observer);
          comm->wait_for(observer.get_issuer(), timeout);
        },
        &observer);
  }
}

CommPtr Comm::sendto_init()
{
  CommPtr res(new Comm());
  res->pimpl_ = kernel::activity::CommImplPtr(new kernel::activity::CommImpl());
  boost::static_pointer_cast<kernel::activity::CommImpl>(res->pimpl_)->detach();
  res->sender_ = kernel::actor::ActorImpl::self();
  return res;
}

CommPtr Comm::sendto_init(Host* from, Host* to)
{
  auto res = Comm::sendto_init()->set_source(from)->set_destination(to);
  res->set_state(State::STARTING);
  return res;
}

CommPtr Comm::sendto_async(Host* from, Host* to, uint64_t simulated_size_in_bytes)
{
  return Comm::sendto_init()->set_payload_size(simulated_size_in_bytes)->set_source(from)->set_destination(to);
}

void Comm::sendto(Host* from, Host* to, uint64_t simulated_size_in_bytes)
{
  sendto_async(from, to, simulated_size_in_bytes)->wait();
}

CommPtr Comm::set_source(Host* from)
{
  xbt_assert(state_ == State::INITED || state_ == State::STARTING,
             "Cannot change the source of a Comm once it's started (state: %s)", to_c_str(state_));
  boost::static_pointer_cast<kernel::activity::CommImpl>(pimpl_)->set_source(from);
  // Setting 'source' may allow to start the activity, let's try
  if (state_ == State::STARTING && remains_ <= 0)
    XBT_DEBUG("This communication has a payload size of 0 byte. It cannot start yet");
  else
    start();

  return this;
}
Host* Comm::get_source() const
{
  return pimpl_ ? boost::static_pointer_cast<kernel::activity::CommImpl>(pimpl_)->get_source() : nullptr;
}

CommPtr Comm::set_destination(Host* to)
{
  xbt_assert(state_ == State::INITED || state_ == State::STARTING,
             "Cannot change the destination of a Comm once it's started (state: %s)", to_c_str(state_));
  boost::static_pointer_cast<kernel::activity::CommImpl>(pimpl_)->set_destination(to);
  // Setting 'destination' may allow to start the activity, let's try
  if (state_ == State::STARTING && remains_ <= 0)
    XBT_DEBUG("This communication has a payload size of 0 byte. It cannot start yet");
  else
    start();

  return this;
}

Host* Comm::get_destination() const
{
  return pimpl_ ? boost::static_pointer_cast<kernel::activity::CommImpl>(pimpl_)->get_destination() : nullptr;
}

CommPtr Comm::set_rate(double rate)
{
  xbt_assert(state_ == State::INITED, "You cannot use %s() once your communication started (not implemented)",
             __func__);
  rate_ = rate;
  return this;
}

CommPtr Comm::set_mailbox(Mailbox* mailbox)
{
  xbt_assert(state_ == State::INITED, "You cannot use %s() once your communication started (not implemented)",
             __func__);
  mailbox_ = mailbox;
  return this;
}

CommPtr Comm::set_src_data(void* buff)
{
  xbt_assert(state_ == State::INITED, "You cannot use %s() once your communication started (not implemented)",
             __func__);
  xbt_assert(dst_buff_ == nullptr, "Cannot set the src and dst buffers at the same time");
  src_buff_ = buff;
  return this;
}

CommPtr Comm::set_src_data_size(size_t size)
{
  xbt_assert(state_ == State::INITED, "You cannot use %s() once your communication started (not implemented)",
             __func__);
  src_buff_size_ = size;
  return this;
}

CommPtr Comm::set_src_data(void* buff, size_t size)
{
  xbt_assert(state_ == State::INITED, "You cannot use %s() once your communication started (not implemented)",
             __func__);

  xbt_assert(dst_buff_ == nullptr, "Cannot set the src and dst buffers at the same time");
  src_buff_      = buff;
  src_buff_size_ = size;
  return this;
}

CommPtr Comm::set_dst_data(void** buff)
{
  xbt_assert(state_ == State::INITED, "You cannot use %s() once your communication started (not implemented)",
             __func__);
  xbt_assert(src_buff_ == nullptr, "Cannot set the src and dst buffers at the same time");
  dst_buff_ = buff;
  return this;
}

CommPtr Comm::set_dst_data(void** buff, size_t size)
{
  xbt_assert(state_ == State::INITED, "You cannot use %s() once your communication started (not implemented)",
             __func__);

  xbt_assert(src_buff_ == nullptr, "Cannot set the src and dst buffers at the same time");
  dst_buff_      = buff;
  dst_buff_size_ = size;
  return this;
}

CommPtr Comm::set_payload_size(uint64_t bytes)
{
  set_remaining(bytes);
  if (pimpl_) {
    boost::static_pointer_cast<kernel::activity::CommImpl>(pimpl_)->set_size(bytes);
  }
  return this;
}

void* Comm::get_payload() const
{
  xbt_assert(get_state() == State::FINISHED,
             "You can only retrieve the payload of a communication that gracefully terminated, but its state is %s.",
             get_state_str());
  return static_cast<kernel::activity::CommImpl*>(pimpl_.get())->payload_;
}

Actor* Comm::get_sender() const
{
  kernel::actor::ActorImplPtr sender = nullptr;
  if (pimpl_)
    sender = boost::static_pointer_cast<kernel::activity::CommImpl>(pimpl_)->src_actor_;
  return sender ? sender->get_ciface() : nullptr;
}

Actor* Comm::get_receiver() const
{
  kernel::actor::ActorImplPtr receiver = nullptr;
  if (pimpl_)
    receiver = boost::static_pointer_cast<kernel::activity::CommImpl>(pimpl_)->dst_actor_;
  return receiver ? receiver->get_ciface() : nullptr;
}

bool Comm::is_assigned() const
{
  return (pimpl_ && boost::static_pointer_cast<kernel::activity::CommImpl>(pimpl_)->is_assigned()) ||
         mailbox_ != nullptr;
}

Comm* Comm::do_start()
{
  xbt_assert(get_state() == State::INITED || get_state() == State::STARTING,
             "You cannot use %s() once your communication started (not implemented)", __func__);

  auto myself = kernel::actor::ActorImpl::self();

  if (get_source() != nullptr || get_destination() != nullptr) {
    xbt_assert(is_assigned(), "When either from_ or to_ is specified, both must be.");
    xbt_assert(src_buff_ == nullptr && dst_buff_ == nullptr,
               "Direct host-to-host communications cannot carry any data.");
    XBT_DEBUG("host-to-host Comm. Pimpl already created and set, just start it.");
    kernel::actor::simcall_answered([this] {
      pimpl_->set_state(kernel::activity::State::READY);
      boost::static_pointer_cast<kernel::activity::CommImpl>(pimpl_)->start();
    });
    fire_on_start();
    fire_on_this_start();
  } else if (myself == sender_) {
    on_send(*this);
    on_this_send(*this);
    kernel::actor::CommIsendSimcall observer{sender_,
                                             mailbox_->get_impl(),
                                             remains_,
                                             rate_,
                                             static_cast<unsigned char*>(src_buff_),
                                             src_buff_size_,
                                             nullptr,
                                             get_clean_function(),
                                             copy_data_function_,
                                             nullptr,
                                             detached_,
                                             "Isend"};
    pimpl_ = kernel::actor::simcall_answered([&observer] { return kernel::activity::CommImpl::isend(&observer); },
                                             &observer);
  } else if (myself == receiver_) {
    xbt_assert(not detached_, "Receive cannot be detached");
    on_recv(*this);
    on_this_recv(*this);
    kernel::actor::CommIrecvSimcall observer{receiver_,
                                             mailbox_->get_impl(),
                                             static_cast<unsigned char*>(dst_buff_),
                                             &dst_buff_size_,
                                             nullptr,
                                             copy_data_function_,
                                             nullptr,
                                             rate_,
                                             "Irecv"};
    pimpl_ = kernel::actor::simcall_answered([&observer] { return kernel::activity::CommImpl::irecv(&observer); },
                                             &observer);
  } else {
    xbt_die("Cannot start a communication before specifying whether we are the sender or the receiver");
  }

  if (suspended_)
    pimpl_->suspend();

  if (not detached_) {
    pimpl_->set_iface(this);
    pimpl_->set_actor(sender_);
    // Only throw the signal when both sides are here and the status is READY
    if (pimpl_->get_state() != kernel::activity::State::WAITING) {
      fire_on_start();
      fire_on_this_start();
    }
  }

  state_ = State::STARTED;
  return this;
}

ssize_t Comm::test_any(const std::vector<CommPtr>& comms) // XBT_ATTRIB_DEPRECATED_v401
{
  std::vector<kernel::activity::ActivityImpl*> ractivities(comms.size());
  std::transform(begin(comms), end(comms), begin(ractivities), [](const CommPtr& act) { return act->pimpl_.get(); });

  kernel::actor::ActorImpl* issuer = kernel::actor::ActorImpl::self();
  kernel::actor::ActivityTestanySimcall observer{issuer, ractivities, "test_any"};
  ssize_t changed_pos = kernel::actor::simcall_answered(
      [&observer] {
        return kernel::activity::ActivityImpl::test_any(observer.get_issuer(), observer.get_activities());
      },
      &observer);
  if (changed_pos != -1)
    comms.at(changed_pos)->complete(State::FINISHED);
  return changed_pos;
}

/** @brief Block the calling actor until the communication is finished, or until timeout
 *
 * On timeout, an exception is thrown and the communication is invalidated.
 *
 * @param timeout the amount of seconds to wait for the comm termination.
 *                Negative values denote infinite wait times. 0 as a timeout returns immediately. */
Comm* Comm::wait_for(double timeout)
{
  XBT_DEBUG("Calling Comm::wait_for with state %s", get_state_str());
  kernel::actor::ActorImpl* issuer = nullptr;
  switch (state_) {
    case State::FINISHED:
      break;
    case State::FAILED:
      throw NetworkFailureException(XBT_THROW_POINT, "Cannot wait for a failed communication");
    case State::INITED:
    case State::STARTING: // It's not started yet. Do it in one simcall if it's a regular communication
      if (get_source() != nullptr || get_destination() != nullptr) {
        return start()->wait_for(timeout); // In the case of host2host comm, do it in two simcalls
      } else if (src_buff_ != nullptr) {
        on_send(*this);
        on_this_send(*this);
        send(sender_, mailbox_, remains_, rate_, src_buff_, src_buff_size_, nullptr, copy_data_function_,
             get_data<void>(), timeout);

      } else { // Receiver
        on_recv(*this);
        on_this_recv(*this);
        recv(receiver_, mailbox_, dst_buff_, &dst_buff_size_, nullptr, copy_data_function_, get_data<void>(), timeout,
             rate_);
      }
      break;
    case State::STARTED:
      try {
        issuer = kernel::actor::ActorImpl::self();
        kernel::actor::ActivityWaitSimcall observer{issuer, pimpl_.get(), timeout, "Wait"};
        if (kernel::actor::simcall_blocking(
                [&observer] { observer.get_activity()->wait_for(observer.get_issuer(), observer.get_timeout()); },
                &observer)) {
          throw TimeoutException(XBT_THROW_POINT, "Timeouted");
        }
      } catch (const NetworkFailureException& e) {
        issuer->simcall_.observer_ = nullptr; // Comm failed on network failure, reset the observer to nullptr
        complete(State::FAILED);
        e.rethrow_nested(XBT_THROW_POINT, boost::core::demangle(typeid(e).name()) + " raised in kernel mode.");
      }
      break;

    case State::CANCELED:
      throw CancelException(XBT_THROW_POINT, "Communication canceled");

    default:
      THROW_IMPOSSIBLE;
  }
  complete(State::FINISHED);
  return this;
}

ssize_t Comm::deprecated_wait_any_for(const std::vector<CommPtr>& comms, double timeout) // XBT_ATTRIB_DEPRECATED_v401
{
  if (comms.empty())
    return -1;
  ActivitySet set;
  for (const auto& comm : comms)
    set.push(comm);
  try {
    auto* ret = set.wait_any_for(timeout).get();
    for (size_t i = 0; i < comms.size(); i++)
      if (comms[i].get() == ret)
        return i;

  } catch (TimeoutException& e) {
    return -1;
  } catch (const NetworkFailureException& e) {
    for (auto c : comms)
      if (c->pimpl_->get_state() == kernel::activity::State::FAILED)
        c->complete(State::FAILED);

    e.rethrow_nested(XBT_THROW_POINT, boost::core::demangle(typeid(e).name()) + " raised in kernel mode.");
  }
  return -1;
}

void Comm::wait_all(const std::vector<CommPtr>& comms) // XBT_ATTRIB_DEPRECATED_v401
{
  // TODO: this should be a simcall or something
  for (const auto& comm : comms)
    comm->wait();
}

size_t Comm::wait_all_for(const std::vector<CommPtr>& comms, double timeout) // XBT_ATTRIB_DEPRECATED_v401
{
  if (timeout < 0.0) {
    for (const auto& comm : comms)
      comm->wait();
    return comms.size();
  }

  ActivitySet set;
  for (auto comm : comms)
    set.push(comm);
  set.wait_all_for(timeout);

  return set.size();
}
} // namespace simgrid::s4u
/* **************************** Public C interface *************************** */
int sg_comm_isinstance(sg_activity_t acti)
{
  return dynamic_cast<simgrid::s4u::Comm*>(acti) != nullptr;
}

void sg_comm_detach(sg_comm_t comm, void (*clean_function)(void*))
{
  comm->detach(clean_function);
  comm->unref();
}
void sg_comm_unref(sg_comm_t comm)
{
  comm->unref();
}
int sg_comm_test(sg_comm_t comm)
{
  bool finished = comm->test();
  if (finished)
    comm->unref();
  return finished;
}

sg_error_t sg_comm_wait(sg_comm_t comm)
{
  return sg_comm_wait_for(comm, -1);
}

sg_error_t sg_comm_wait_for(sg_comm_t comm, double timeout)
{
  sg_error_t status = SG_OK;

  simgrid::s4u::CommPtr s4u_comm(comm, false);
  try {
    s4u_comm->wait_for(timeout);
  } catch (const simgrid::TimeoutException&) {
    status = SG_ERROR_TIMEOUT;
  } catch (const simgrid::CancelException&) {
    status = SG_ERROR_CANCELED;
  } catch (const simgrid::NetworkFailureException&) {
    status = SG_ERROR_NETWORK;
  }
  return status;
}

void sg_comm_wait_all(sg_comm_t* comms, size_t count) // XBT_ATTRIB_DEPRECATED_v401
{
  simgrid::s4u::ActivitySet as;
  for (size_t i = 0; i < count; i++)
    as.push(comms[i]);

  as.wait_all();
}

ssize_t sg_comm_wait_any(sg_comm_t* comms, size_t count) // XBT_ATTRIB_DEPRECATED_v401
{
  std::vector<simgrid::s4u::CommPtr> s4u_comms;
  for (size_t i = 0; i < count; i++)
    s4u_comms.emplace_back(comms[i], false);

  ssize_t pos = simgrid::s4u::Comm::deprecated_wait_any_for(s4u_comms, -1);
  for (size_t i = 0; i < count; i++) {
    if (pos != -1 && static_cast<size_t>(pos) != i)
      s4u_comms[i]->add_ref();
  }
  return pos;
}

ssize_t sg_comm_wait_any_for(sg_comm_t* comms, size_t count, double timeout) // XBT_ATTRIB_DEPRECATED_v401
{
  std::vector<simgrid::s4u::CommPtr> s4u_comms;
  for (size_t i = 0; i < count; i++)
    s4u_comms.emplace_back(comms[i], false);

  ssize_t pos = simgrid::s4u::Comm::deprecated_wait_any_for(s4u_comms, timeout);
  for (size_t i = 0; i < count; i++) {
    if (pos != -1 && static_cast<size_t>(pos) != i)
      s4u_comms[i]->add_ref();
  }
  return pos;
}
