/* Copyright (c) 2003-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "simgrid/s4u.hpp"

XBT_LOG_NEW_DEFAULT_CATEGORY(dag_from_json_simple, "Messages specific for this s4u example");

int main(int argc, char* argv[])
{
  simgrid::s4u::Engine e(&argc, argv);
  e.load_platform(argv[1]);

  std::vector<simgrid::s4u::ActivityPtr> dag = simgrid::s4u::create_DAG_from_json(argv[2]);

   simgrid::s4u::Exec::on_completion_cb([](simgrid::s4u::Exec const& exec) {
    XBT_INFO("Exec '%s' is complete (start time: %f, finish time: %f)", exec.get_cname(),
             exec.get_start_time(), exec.get_finish_time());
  });

  simgrid::s4u::Comm::on_completion_cb([](simgrid::s4u::Comm const& comm) {
    XBT_INFO("Comm '%s' is complete (start time: %f, finish time: %f)", comm.get_cname(),
             comm.get_start_time(), comm.get_finish_time());
  });

  e.run();
  return 0;
}
