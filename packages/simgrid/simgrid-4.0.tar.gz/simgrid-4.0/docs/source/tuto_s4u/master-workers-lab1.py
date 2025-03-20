# Copyright (c) 2010-2025. The SimGrid Team. All rights reserved.

# This program is free software; you can redistribute it and/or modify it
# under the terms of the license (GNU LGPL) which comes with this package.

"""
# ##################################################################################
# Take this tutorial online: https://simgrid.org/doc/latest/Tutorial_Algorithms.html
# ##################################################################################
"""

import sys
from simgrid import Engine, Mailbox, this_actor

# master-begin
def master(*args):
    if len(args) == 2:
        raise AssertionError(f"Actor master requires 4 parameters, but only {len(args)}")
    worker_count = int(args[0])
    tasks_count = int(args[1])
    compute_cost = int(args[2])
    communicate_cost = int(args[3])
    this_actor.info(f"Got {worker_count} workers and {tasks_count} tasks to process")

    for i in range(tasks_count): # For each task to be executed:
        # - Select a worker in a round-robin way
        mailbox = Mailbox.by_name(str(i % worker_count))

        # - Send the computation amount to the worker
        if (tasks_count < 10000 or (tasks_count < 100000 and i % 10000 == 0) or i % 100000 == 0):
            this_actor.info(f"Sending task {i} of {tasks_count} to mailbox '{mailbox.name}'")
        mailbox.put(compute_cost, communicate_cost)

    this_actor.info("All tasks have been dispatched. Request all workers to stop.")
    for i in range(worker_count):
        # The workers stop when receiving a negative compute_cost
        mailbox = Mailbox.by_name(str(i))
        mailbox.put(-1, 0)
# master-end

# worker-begin
def worker(*args):
    assert len(args) == 1, "The worker expects one argument"

    mailbox = Mailbox.by_name(args[0])
    done = False
    while not done:
        compute_cost = mailbox.get()
        if compute_cost > 0: # If compute_cost is valid, execute a computation of that cost
            this_actor.execute(compute_cost)
        else: # Stop when receiving an invalid compute_cost
            done = True

    this_actor.info("Exiting now.")
# worker-end

# main-begin
if __name__ == '__main__':
    assert len(sys.argv) > 2, f"Usage: python app-masterworkers.py platform_file deployment_file"

    e = Engine(sys.argv)

    # Register the classes representing the actors
    e.register_actor("master", master)
    e.register_actor("worker", worker)

    # Load the platform description and then deploy the application
    e.load_platform(sys.argv[1])
    e.load_deployment(sys.argv[2])

    # Run the simulation
    e.run()

    this_actor.info("Simulation is over")
# main-end
