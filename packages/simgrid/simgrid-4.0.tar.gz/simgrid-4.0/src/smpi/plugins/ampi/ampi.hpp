/* Copyright (c) 2010-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#ifndef INSTR_AMPI_HPP_
#define INSTR_AMPI_HPP_

#include <simgrid/s4u.hpp>

namespace simgrid::smpi::plugin::ampi {
extern xbt::signal<void(s4u::Actor const&)> on_iteration_out;
extern xbt::signal<void(s4u::Actor const&)> on_iteration_in;
} // namespace simgrid::smpi::plugin::ampi

#endif
