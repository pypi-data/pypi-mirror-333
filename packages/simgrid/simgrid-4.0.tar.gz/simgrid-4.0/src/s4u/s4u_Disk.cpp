/* Copyright (c) 2019-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include <simgrid/s4u/Disk.hpp>
#include <simgrid/s4u/Io.hpp>
#include <simgrid/simcall.hpp>

#include "src/kernel/resource/DiskImpl.hpp"

namespace simgrid {

template class xbt::Extendable<s4u::Disk>;

namespace s4u {

xbt::signal<void(Disk&)> Disk::on_creation;
xbt::signal<void(Disk const&)> Disk::on_onoff;
xbt::signal<void(Disk const&)> Disk::on_read_bandwidth_change;
xbt::signal<void(Disk const&)> Disk::on_write_bandwidth_change;
xbt::signal<void(kernel::resource::DiskAction&, kernel::resource::Action::State)> Disk::on_io_state_change;
xbt::signal<void(Disk const&)> Disk::on_destruction;

const std::string& Disk::get_name() const
{
  return pimpl_->get_name();
}

const char* Disk::get_cname() const
{
  return pimpl_->get_cname();
}

Disk* Disk::set_read_bandwidth(double read_bw)
{
  kernel::actor::simcall_object_access(pimpl_, [this, read_bw] { pimpl_->set_read_bandwidth(read_bw); });
  return this;
}

Disk* Disk::set_write_bandwidth(double write_bw)
{
  kernel::actor::simcall_object_access(pimpl_, [this, write_bw] { pimpl_->set_write_bandwidth(write_bw); });
  return this;
}

double Disk::get_read_bandwidth() const
{
  return pimpl_->get_read_bandwidth();
}

Disk* Disk::set_readwrite_bandwidth(double bw)
{
  kernel::actor::simcall_object_access(pimpl_, [this, bw] { pimpl_->set_readwrite_bandwidth(bw); });
  return this;
}

double Disk::get_write_bandwidth() const
{
  return pimpl_->get_write_bandwidth();
}

Disk* Disk::set_host(Host* host)
{
  pimpl_->set_host(host);
  return this;
}

Host* Disk::get_host() const
{
  return pimpl_->get_host();
}

void Disk::turn_on()
{
  if (not is_on()) {
    kernel::actor::simcall_answered([this] {
      this->pimpl_->turn_on();
      on_onoff(*this);
      on_this_onoff(*this);
    });
  }
}

void Disk::turn_off()
{
  if (is_on()) {
    kernel::actor::simcall_answered([this] {
      this->pimpl_->turn_off();

      on_onoff(*this);
      on_this_onoff(*this);
    });
  }
}

bool Disk::is_on() const
{
  return this->pimpl_->is_on();
}



const std::unordered_map<std::string, std::string>* Disk::get_properties() const
{
  return pimpl_->get_properties();
}

const char* Disk::get_property(const std::string& key) const
{
  return pimpl_->get_property(key);
}

Disk* Disk::set_property(const std::string& key, const std::string& value)
{
  kernel::actor::simcall_object_access(pimpl_, [this, &key, &value] { this->pimpl_->set_property(key, value); });
  return this;
}

Disk* Disk::set_properties(const std::unordered_map<std::string, std::string>& properties)
{
  kernel::actor::simcall_object_access(pimpl_, [this, properties] { this->pimpl_->set_properties(properties); });
  return this;
}

Disk* Disk::set_state_profile(kernel::profile::Profile* profile)
{
  xbt_assert(not pimpl_->is_sealed(), "Cannot set a state profile once the Disk is sealed");
  kernel::actor::simcall_object_access(pimpl_, [this, profile]() { this->pimpl_->set_state_profile(profile); });
  return this;
}

Disk* Disk::set_read_bandwidth_profile(kernel::profile::Profile* profile)
{
  xbt_assert(not pimpl_->is_sealed(), "Cannot set a bandwidth profile once the Disk is sealed");
  kernel::actor::simcall_object_access(pimpl_,
                                       [this, profile]() { this->pimpl_->set_read_bandwidth_profile(profile); });
  return this;
}

Disk* Disk::set_write_bandwidth_profile(kernel::profile::Profile* profile)
{
  xbt_assert(not pimpl_->is_sealed(), "Cannot set a bandwidth profile once the Disk is sealed");
  kernel::actor::simcall_object_access(pimpl_,
                                       [this, profile]() { this->pimpl_->set_write_bandwidth_profile(profile); });
  return this;
}
int Disk::get_concurrency_limit() const
{
  return pimpl_->get_concurrency_limit();
}

Disk* Disk::set_concurrency_limit(int limit)
{
  kernel::actor::simcall_object_access(pimpl_, [this, limit] { pimpl_->set_concurrency_limit(limit); });
  return this;
}

IoPtr Disk::io_init(sg_size_t size, Io::OpType type) const
{
  return Io::init()->set_disk(this)->set_size(size)->set_op_type(type);
}

IoPtr Disk::read_async(sg_size_t size) const
{
  return IoPtr(io_init(size, Io::OpType::READ))->start();
}

sg_size_t Disk::read(sg_size_t size) const
{
  return IoPtr(io_init(size, Io::OpType::READ))->start()->wait()->get_performed_ioops();
}

sg_size_t Disk::read(sg_size_t size, double priority) const
{
  return IoPtr(io_init(size, Io::OpType::READ))
      ->set_priority(priority)
      ->start()
      ->wait()
      ->get_performed_ioops();
}

IoPtr Disk::write_async(sg_size_t size) const
{
  return IoPtr(io_init(size, Io::OpType::WRITE)->start());
}

sg_size_t Disk::write(sg_size_t size) const
{
  return IoPtr(io_init(size, Io::OpType::WRITE))->start()->wait()->get_performed_ioops();
}

sg_size_t Disk::write(sg_size_t size, double priority) const
{
  return IoPtr(io_init(size, Io::OpType::WRITE))
      ->set_priority(priority)
      ->start()
      ->wait()
      ->get_performed_ioops();
}

Disk* Disk::set_sharing_policy(Disk::Operation op, Disk::SharingPolicy policy, const NonLinearResourceCb& cb)
{
  kernel::actor::simcall_object_access(pimpl_, [this, op, policy, &cb] { pimpl_->set_sharing_policy(op, policy, cb); });
  return this;
}

Disk::SharingPolicy Disk::get_sharing_policy(Operation op) const
{
  return this->pimpl_->get_sharing_policy(op);
}

Disk* Disk::set_factor_cb(const std::function<IoFactorCb>& cb)
{
  kernel::actor::simcall_object_access(pimpl_, [this, &cb] { pimpl_->set_factor_cb(cb); });
  return this;
}

Disk* Disk::seal()
{
  kernel::actor::simcall_answered([this] { pimpl_->seal(); });
  Disk::on_creation(*this); // notify the signal
  return this;
}
} // namespace s4u
} // namespace simgrid

/* **************************** Public C interface *************************** */

const char* sg_disk_get_name(const_sg_disk_t disk)
{
  return disk->get_cname();
}

sg_host_t sg_disk_get_host(const_sg_disk_t disk)
{
  return disk->get_host();
}

double sg_disk_read_bandwidth(const_sg_disk_t disk)
{
  return disk->get_read_bandwidth();
}

double sg_disk_write_bandwidth(const_sg_disk_t disk)
{
  return disk->get_write_bandwidth();
}

sg_size_t sg_disk_read(const_sg_disk_t disk, sg_size_t size)
{
  return disk->read(size);
}
sg_size_t sg_disk_write(const_sg_disk_t disk, sg_size_t size)
{
  return disk->write(size);
}

void* sg_disk_get_data(const_sg_disk_t disk)
{
  return disk->get_data<void>();
}

void sg_disk_set_data(sg_disk_t disk, void* data)
{
  disk->set_data(data);
}
