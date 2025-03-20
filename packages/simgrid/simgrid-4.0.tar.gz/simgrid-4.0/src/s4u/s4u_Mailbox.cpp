/* Copyright (c) 2006-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include <simgrid/mailbox.h>
#include <simgrid/s4u/Engine.hpp>
#include <simgrid/s4u/Mailbox.hpp>

#include "src/kernel/activity/MailboxImpl.hpp"
#include "src/kernel/actor/CommObserver.hpp"

XBT_LOG_EXTERNAL_CATEGORY(s4u);
XBT_LOG_NEW_DEFAULT_SUBCATEGORY(s4u_channel, s4u, "S4U Communication Mailboxes");

namespace simgrid::s4u {

const std::string& Mailbox::get_name() const
{
  return pimpl_->get_name();
}

const char* Mailbox::get_cname() const
{
  return pimpl_->get_cname();
}

Mailbox* Mailbox::by_name(const std::string& name)
{
  return Engine::get_instance()->mailbox_by_name_or_create(name);
}

bool Mailbox::empty() const
{
  return pimpl_->empty();
}

size_t Mailbox::size() const
{
  return pimpl_->size();
}

bool Mailbox::listen() const
{
  return not pimpl_->empty() || (pimpl_->is_permanent() && pimpl_->has_some_done_comm());
}

aid_t Mailbox::listen_from() const
{
  kernel::activity::CommImplPtr comm = front();
  if (comm && comm->src_actor_)
    return comm->src_actor_->get_pid();
  else
    return -1;
}

bool Mailbox::ready() const
{
  bool comm_ready = false;
  if (not pimpl_->empty()) {
    comm_ready = pimpl_->front()->get_state() == kernel::activity::State::DONE;

  } else if (pimpl_->is_permanent() && pimpl_->has_some_done_comm()) {
    comm_ready = pimpl_->done_front()->get_state() == kernel::activity::State::DONE;
  }
  return comm_ready;
}

kernel::activity::CommImplPtr Mailbox::front() const
{
  return pimpl_->empty() ? nullptr : pimpl_->front();
}

void Mailbox::set_receiver(ActorPtr actor)
{
  kernel::actor::simcall_answered([this, actor]() { this->pimpl_->set_receiver(actor); });
}

/** @brief get the receiver (process associated to the mailbox) */
ActorPtr Mailbox::get_receiver() const
{
  if (pimpl_->is_permanent())
    return ActorPtr();
  return pimpl_->get_permanent_receiver()->get_iface();
}

CommPtr Mailbox::put_init()
{
  CommPtr res(new Comm());
  res->sender_  = kernel::actor::ActorImpl::self();
  res->set_mailbox(this);
  return res;
}

CommPtr Mailbox::put_init(void* payload, uint64_t simulated_size_in_bytes)
{
  xbt_assert(payload != nullptr, "You cannot send nullptr");

  return put_init()->set_payload_size(simulated_size_in_bytes)->set_src_data(payload)->set_src_data_size(sizeof(void*));
}

CommPtr Mailbox::put_async(void* payload, uint64_t simulated_size_in_bytes)
{
  xbt_assert(payload != nullptr, "You cannot send nullptr");

  CommPtr res = put_init(payload, simulated_size_in_bytes);
  res->start();
  return res;
}

void Mailbox::put(void* payload, uint64_t simulated_size_in_bytes)
{
  xbt_assert(payload != nullptr, "You cannot send nullptr");

  CommPtr comm = put_init()->set_payload_size(simulated_size_in_bytes)->set_src_data(payload)->start();
  try {
    comm->wait();
  } catch (simgrid::TimeoutException&) {
    comm->cancel();
    // Rethrowing the original exception segfaults in parallel tests
    throw TimeoutException(XBT_THROW_POINT, "Timeouted");
  }
}

/** Blocking send with timeout */
void Mailbox::put(void* payload, uint64_t simulated_size_in_bytes, double timeout)
{
  xbt_assert(payload != nullptr, "You cannot send nullptr");

  put_init()->set_payload_size(simulated_size_in_bytes)->set_src_data(payload)->start()->wait_for_or_cancel(timeout);
}

CommPtr Mailbox::get_init()
{
  auto res       = CommPtr(new Comm())->set_mailbox(this);
  res->receiver_ = kernel::actor::ActorImpl::self();
  return res;
}

CommPtr Mailbox::get_async()
{
  CommPtr res = get_init()->set_dst_data(nullptr, sizeof(void*));
  res->start();
  return res;
}

kernel::activity::ActivityImplPtr
Mailbox::iprobe(IprobeKind kind, const std::function<bool(void*, void*, kernel::activity::CommImpl*)>& match_fun,
                void* data)
{
  auto self = kernel::actor::ActorImpl::self();
  kernel::actor::IprobeSimcall observer(self, pimpl_, kind, match_fun, data);
  return kernel::actor::simcall_answered(
      [this, kind, &match_fun, data] { return pimpl_->iprobe(kind, match_fun, data); }, &observer);
}

void Mailbox::clear()
{
  kernel::actor::simcall_answered([this]() { this->pimpl_->clear(true); });
}

} // namespace simgrid::s4u

/* **************************** Public C interface *************************** */
sg_mailbox_t sg_mailbox_by_name(const char* alias)
{
  return simgrid::s4u::Mailbox::by_name(alias);
}

const char* sg_mailbox_get_name(const_sg_mailbox_t mailbox)
{
  return mailbox->get_cname();
}

/** @brief Set the mailbox to receive in asynchronous mode
 *
 * All messages sent to this mailbox will be transferred to the receiver without waiting for the receive call.
 * The receive call will still be necessary to use the received data.
 * If there is a need to receive some messages asynchronously, and some not, two different mailboxes should be used.
 *
 * @param alias The name of the mailbox
 */
void sg_mailbox_set_receiver(const char* alias)
{
  simgrid::s4u::Mailbox::by_name(alias)->set_receiver(simgrid::s4u::Actor::self());
  XBT_VERB("%s mailbox set to receive eagerly for myself\n", alias);
}

/** @brief Check if there is a communication going on in a mailbox.
 *
 * @param alias the name of the mailbox to be considered
 * @return Returns 1 if there is a communication, 0 otherwise
 */
int sg_mailbox_listen(const char* alias)
{
  return simgrid::s4u::Mailbox::by_name(alias)->listen() ? 1 : 0;
}

void* sg_mailbox_get(sg_mailbox_t mailbox)
{
  return mailbox->get<void>();
}

sg_comm_t sg_mailbox_get_async(sg_mailbox_t mailbox, void** data)
{
  auto comm = mailbox->get_async<void>(data);
  comm->add_ref();
  return comm.get();
}

void sg_mailbox_put(sg_mailbox_t mailbox, void* payload, long simulated_size_in_bytes)
{
  mailbox->put(payload, simulated_size_in_bytes);
}

sg_comm_t sg_mailbox_put_async(sg_mailbox_t mailbox, void* payload, long simulated_size_in_bytes)
{
  auto comm = mailbox->put_async(payload, simulated_size_in_bytes);
  comm->add_ref();
  return comm.get();
}

sg_comm_t sg_mailbox_put_init(sg_mailbox_t mailbox, void* payload, long simulated_size_in_bytes)
{
  auto comm = mailbox->put_init(payload, simulated_size_in_bytes);
  comm->add_ref();
  return comm.get();
}
