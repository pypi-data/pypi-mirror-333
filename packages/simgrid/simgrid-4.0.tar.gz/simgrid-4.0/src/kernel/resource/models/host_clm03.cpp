/* Copyright (c) 2013-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include <simgrid/kernel/routing/NetPoint.hpp>
#include <simgrid/kernel/routing/NetZoneImpl.hpp>
#include <simgrid/s4u/Engine.hpp>

#include "src/kernel/EngineImpl.hpp"
#include "src/kernel/resource/NetworkModel.hpp"
#include "src/kernel/resource/models/host_clm03.hpp"
#include "src/simgrid/module.hpp"
#include "src/simgrid/sg_config.hpp"

XBT_LOG_EXTERNAL_DEFAULT_CATEGORY(res_host);

SIMGRID_REGISTER_HOST_MODEL(
    default, "Default host model. Currently, CPU:Cas01, network:LV08 (with cross traffic enabled), and disk:S19", []() {
      simgrid::config::set_default<bool>("network/crosstraffic", true);
      auto host_model = std::make_shared<simgrid::kernel::resource::HostCLM03Model>("Host_CLM03");
      auto* engine    = simgrid::kernel::EngineImpl::get_instance();
      engine->add_model(host_model);
      engine->get_netzone_root()->set_host_model(host_model);

      simgrid_cpu_models().init_from_flag_value();
      simgrid_disk_models().init_from_flag_value();
      simgrid_network_models().init_from_flag_value();
    });

namespace simgrid::kernel::resource {

double HostCLM03Model::next_occurring_event(double /*now*/)
{
  /* nothing specific to be done here
   * EngineImpl::solve already calls all the models next_occurring_event properly */
  return -1.0;
}

void HostCLM03Model::update_actions_state(double /*now*/, double /*delta*/)
{
  /* I've no action to update */
}

/* Helper function for executeParallelTask */
static inline double has_cost(const double* array, size_t pos)
{
  if (array)
    return array[pos];
  return -1.0;
}

Action* HostCLM03Model::execute_parallel(const std::vector<s4u::Host*>& host_list, const double* flops_amount,
                                         const double* bytes_amount, double rate)
{
  Action* action = nullptr;
  auto net_model = host_list[0]->get_netpoint()->get_englobing_zone()->get_network_model();
  if ((host_list.size() == 1) && (has_cost(bytes_amount, 0) <= 0) && (has_cost(flops_amount, 0) > 0)) {
    action = host_list[0]->get_cpu()->execution_start(flops_amount[0], rate);
  } else if ((host_list.size() == 1) && (has_cost(flops_amount, 0) <= 0)) {
    action = net_model->communicate(host_list[0], host_list[0], bytes_amount[0], rate, false);
  } else if ((host_list.size() == 2) && (has_cost(flops_amount, 0) <= 0) && (has_cost(flops_amount, 1) <= 0)) {
    int nb       = 0;
    double value = 0.0;

    for (size_t i = 0; i < host_list.size() * host_list.size(); i++) {
      if (has_cost(bytes_amount, i) > 0.0) {
        nb++;
        value = has_cost(bytes_amount, i);
      }
    }
    if (nb == 1) {
      action = net_model->communicate(host_list[0], host_list[1], value, rate, false);
    } else if (nb == 0) {
      xbt_die("Cannot have a communication with no flop to exchange in this model. You should consider using the "
              "ptask model");
    } else {
      xbt_die("Cannot have a communication that is not a simple point-to-point in this model. You should consider "
              "using the ptask model");
    }
  } else {
    xbt_die(
        "This model only accepts one of the following. You should consider using the ptask model for the other cases.\n"
        " - execution with one host only and no communication\n"
        " - Self-comms with one host only\n"
        " - Communications with two hosts and no computation");
  }
  return action;
}

Action* HostCLM03Model::execute_thread(const s4u::Host* host, double flops_amount, int thread_count)
{
  auto* cpu = host->get_cpu();
  /* Create a single action whose cost is thread_count * flops_amount and that requests thread_count cores. */
  return cpu->execution_start(thread_count * flops_amount, thread_count, -1);
}

} // namespace simgrid::kernel::resource
