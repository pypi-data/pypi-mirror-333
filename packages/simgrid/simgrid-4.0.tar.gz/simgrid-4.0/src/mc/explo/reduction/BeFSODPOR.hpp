/* Copyright (c) 2007-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#ifndef SIMGRID_MC_BeFSODPOR_HPP
#define SIMGRID_MC_BeFSODPOR_HPP

#include "simgrid/forward.h"
#include "src/mc/explo/odpor/Execution.hpp"
#include "src/mc/explo/reduction/Reduction.hpp"

namespace simgrid::mc {

class BeFSODPOR : public Reduction {

public:
  BeFSODPOR()  = default;
  ~BeFSODPOR() = default;

  class RaceUpdate : public Reduction::RaceUpdate {
    std::vector<std::pair<StatePtr, odpor::PartialExecution>> state_and_exec_;

  public:
    RaceUpdate() = default;
    void add_element(StatePtr state, odpor::PartialExecution v) { state_and_exec_.emplace_back(state, v); }
    std::vector<std::pair<StatePtr, odpor::PartialExecution>> get_value() { return state_and_exec_; }
  };

  std::unique_ptr<Reduction::RaceUpdate> races_computation(odpor::Execution& E, stack_t* S,
                                                           std::vector<StatePtr>* opened_states) override;
  unsigned long apply_race_update(std::unique_ptr<Reduction::RaceUpdate> updates,
                                  std::vector<StatePtr>* opened_states = nullptr) override;
  aid_t next_to_explore(odpor::Execution& E, stack_t* S) override;
  StatePtr state_create(RemoteApp& remote_app, StatePtr parent_state) override;
  void on_backtrack(State* s) override {}
};

} // namespace simgrid::mc

#endif
