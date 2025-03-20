/* Copyright (c) 2010-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

/* ************************************************************************* */
/* Take this tutorial online: https://simgrid.org/doc/latest/Tutorial_Algorithms.html */
/* ************************************************************************* */

#include <simgrid/s4u.hpp>
namespace sg4 = simgrid::s4u;

XBT_LOG_NEW_DEFAULT_CATEGORY(s4u_app_masterworker, "Messages specific for this example");

// master-begin
static void master(std::vector<std::string> args)
{
  xbt_assert(args.size() > 4, "The master function expects at least 3 arguments");

  long tasks_count        = std::stol(args[1]);
  double compute_cost     = std::stod(args[2]);
  long communication_cost = std::stol(args[3]);
  std::vector<sg4::Mailbox*> workers;
  for (unsigned int i = 4; i < args.size(); i++)
    workers.push_back(sg4::Mailbox::by_name(args[i]));

  XBT_INFO("Got %zu workers and %ld tasks to process", workers.size(), tasks_count);

  for (int i = 0; i < tasks_count; i++) { /* For each task to be executed: */
    /* - Select a worker in a round-robin way */
    sg4::Mailbox* mailbox = workers[i % workers.size()];

    /* - Send the computation cost to that worker */
    XBT_INFO("Sending task %d of %ld to mailbox '%s'", i, tasks_count, mailbox->get_cname());
    mailbox->put(new double(compute_cost), communication_cost);
  }

  XBT_INFO("All tasks have been dispatched. Request all workers to stop.");
  for (unsigned int i = 0; i < workers.size(); i++) {
    /* The workers stop when receiving a negative compute_cost */
    sg4::Mailbox* mailbox = workers[i % workers.size()];

    mailbox->put(new double(-1.0), 0);
  }
}
// master-end

// worker-begin
static void worker(std::vector<std::string> args)
{
  xbt_assert(args.size() == 1, "The worker expects no argument");

  const sg4::Host* my_host = sg4::this_actor::get_host();
  sg4::Mailbox* mailbox    = sg4::Mailbox::by_name(my_host->get_name());

  double compute_cost;
  do {
    auto msg     = mailbox->get_unique<double>();
    compute_cost = *msg;

    if (compute_cost > 0) /* If compute_cost is valid, execute a computation of that cost */
      sg4::this_actor::execute(compute_cost);
  } while (compute_cost > 0); /* Stop when receiving an invalid compute_cost */

  XBT_INFO("Exiting now.");
}
// worker-end

// main-begin
int main(int argc, char* argv[])
{
  sg4::Engine e(&argc, argv);
  xbt_assert(argc > 2, "Usage: %s platform_file deployment_file\n", argv[0]);

  /* Register the functions representing the actors */
  e.register_function("master", &master);
  e.register_function("worker", &worker);

  /* Load the platform description and then deploy the application */
  e.load_platform(argv[1]);
  e.load_deployment(argv[2]);

  /* Run the simulation */
  e.run();

  XBT_INFO("Simulation is over");

  return 0;
}
// main-end
