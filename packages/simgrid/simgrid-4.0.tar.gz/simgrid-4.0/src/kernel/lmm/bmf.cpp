/* Copyright (c) 2007-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "src/kernel/lmm/bmf.hpp"
#include "src/simgrid/math_utils.h"

#include <Eigen/LU>
#include <iostream>
#include <numeric>
#include <sstream>

XBT_LOG_NEW_DEFAULT_SUBCATEGORY(ker_bmf, kernel, "Kernel BMF solver");

namespace simgrid::kernel::lmm {

AllocationGenerator::AllocationGenerator(Eigen::MatrixXd A) : A_(std::move(A)), alloc_(A_.cols(), 0)
{
  // got a first valid allocation
  for (size_t p = 0; p < alloc_.size(); p++) {
    for (int r = 0; r < A_.rows(); r++) {
      if (A_(r, p) > 0) {
        alloc_[p] = r;
        break;
      }
    }
  }
}

bool AllocationGenerator::next(std::vector<int>& next_alloc)
{
  if (first_) {
    next_alloc = alloc_;
    first_     = false;
    return true;
  }

  auto n_resources = A_.rows();
  size_t idx      = 0;
  while (idx < alloc_.size()) {
    alloc_[idx] = (alloc_[idx] + 1) % n_resources;
    if (alloc_[idx] == 0) {
      idx++;
      continue;
    } else {
      idx = 0;
    }
    if (A_(alloc_[idx], idx) > 0) {
      next_alloc = alloc_;
      return true;
    }
  }
  return false;
}

/*****************************************************************************/

BmfSolver::BmfSolver(Eigen::MatrixXd A, Eigen::MatrixXd maxA, Eigen::VectorXd C, std::vector<bool> shared,
                     Eigen::VectorXd phi)
    : A_(std::move(A))
    , maxA_(std::move(maxA))
    , C_(std::move(C))
    , C_shared_(std::move(shared))
    , phi_(std::move(phi))
    , gen_(A_)

{
  xbt_assert(max_iteration_ > 0,
             "Invalid number of iterations for BMF solver. Please check your \"bmf/max-iterations\" configuration.");
  xbt_assert(A_.cols() == maxA_.cols(), "Invalid number of cols in matrix A (%td) or maxA (%td)", A_.cols(),
             maxA_.cols());
  xbt_assert(A_.cols() == phi_.size(), "Invalid size of phi vector (%td)", phi_.size());
  xbt_assert(static_cast<long>(C_shared_.size()) == C_.size(), "Invalid size param shared (%zu)", C_shared_.size());
}

template <typename T> std::string BmfSolver::debug_eigen(const T& obj) const
{
  std::stringstream debug;
  debug << obj;
  return debug.str();
}

template <typename C> std::string BmfSolver::debug_vector(const C& container) const
{
  std::stringstream debug;
  std::copy(container.begin(), container.end(),
            std::ostream_iterator<typename std::remove_reference_t<decltype(container)>::value_type>(debug, " "));
  return debug.str();
}

std::string BmfSolver::debug_alloc(const allocation_map_t& alloc) const
{
  std::stringstream debug;
  for (const auto& [resource, players] : alloc) {
    debug << "{" + std::to_string(resource) + ": [" + debug_vector(players) + "]}, ";
  }
  return debug.str();
}

double BmfSolver::get_resource_capacity(int resource, const std::vector<int>& bounded_players) const
{
  double capacity = C_[resource];
  if (not C_shared_[resource])
    return capacity;

  for (int p : bounded_players) {
    capacity -= A_(resource, p) * phi_[p];
  }
  return std::max(0.0, capacity);
}

double BmfSolver::get_maxmin_share(int resource, const std::vector<int>& bounded_players) const
{
  auto n_players  = (A_.row(resource).array() > 0).count() - bounded_players.size();
  double capacity = get_resource_capacity(resource, bounded_players);
  if (n_players > 0)
    capacity /= n_players;
  return capacity;
}

std::vector<int> BmfSolver::alloc_map_to_vector(const allocation_map_t& alloc) const
{
  std::vector<int> alloc_by_player(A_.cols(), -1);
  for (const auto& [resource, players] : alloc) {
    for (auto p : players) {
      alloc_by_player[p] = resource;
    }
  }
  return alloc_by_player;
}

std::vector<int> BmfSolver::get_bounded_players(const allocation_map_t& alloc) const
{
  std::vector<int> bounded_players;
  for (const auto& [resource, players] : alloc) {
    if (resource == NO_RESOURCE) {
      bounded_players.insert(bounded_players.end(), players.begin(), players.end());
    }
  }
  return bounded_players;
}

Eigen::VectorXd BmfSolver::equilibrium(const allocation_map_t& alloc) const
{
  auto n_players      = A_.cols();
  Eigen::MatrixXd A_p = Eigen::MatrixXd::Zero(n_players, n_players); // square matrix with number of players
  Eigen::VectorXd C_p = Eigen::VectorXd::Zero(n_players);

  int row = 0;
  auto bounded_players = get_bounded_players(alloc);
  for (const auto& [resource, players] : alloc) {
    // add one row for the resource with A[r,]
    /* bounded players, nothing to do */
    if (resource == NO_RESOURCE)
      continue;
    /* not shared resource, each player can receive the full capacity of the resource */
    if (not C_shared_[resource]) {
      for (int i : players) {
        C_p[row]    = get_resource_capacity(resource, bounded_players);
        A_p(row, i) = A_(resource, i);
        row++;
      }
      continue;
    }

    /* shared resource: fairly share it between players */
    A_p.row(row) = A_.row(resource);
    C_p[row]     = get_resource_capacity(resource, bounded_players);
    row++;
    if (players.size() > 1) {
      // if 2 players have chosen the same resource
      // they must have a fair sharing of this resource, adjust A_p and C_p accordingly
      auto it = players.begin();
      int i   = *it; // first player
      /* for each other player sharing this resource */
      for (++it; it != players.end(); ++it) {
        /* player i and k on this resource j: so maxA_ji*rho_i - maxA_jk*rho_k = 0 */
        int k       = *it;
        C_p[row]    = 0;
        A_p(row, i) = maxA_(resource, i);
        A_p(row, k) = -maxA_(resource, k);
        row++;
      }
    }
  }
  /* clear players which are externally bounded */
  for (int p : bounded_players) {
    A_p.col(p).setZero();
  }

  XBT_DEBUG("A':\n%s", debug_eigen(A_p).c_str());

  XBT_DEBUG("C':\n%s", debug_eigen(C_p).c_str());
  /* PartialPivLU is much faster than FullPivLU but requires that the matrix is invertible
   * FullPivLU however assures that it finds come solution even if the matrix is singular
   * Ideally we would like to be optimist and try Partial and in case of error, go back
   * to FullPivLU.
   * However, this with isNaN doesn't work if compiler uses -Ofastmath. In our case,
   * the icc compiler raises an error when compiling the code (comparison with NaN always evaluates to false in fast
   * floating point modes).
   * Eigen::VectorXd rho = Eigen::PartialPivLU<Eigen::MatrixXd>(A_p).solve(C_p);
   * if (rho.array().isNaN().any()) {
   *   XBT_DEBUG("rho with nan values, falling back to FullPivLU, rho:\n%s", debug_eigen(rho).c_str());
   *   rho = Eigen::FullPivLU<Eigen::MatrixXd>(A_p).solve(C_p);
   * }
   */

  Eigen::VectorXd rho = Eigen::FullPivLU<Eigen::MatrixXd>(A_p).solve(C_p);
  for (int p : bounded_players) {
    rho[p] = phi_[p];
  }
  return rho;
}

bool BmfSolver::disturb_allocation(allocation_map_t& alloc, std::vector<int>& alloc_by_player)
{
  while (gen_.next(alloc_by_player)) {
    if (allocations_.find(alloc_by_player) == allocations_.end()) {
      allocations_.clear();
      allocations_.insert(alloc_by_player);
      alloc.clear();
      for (size_t p = 0; p < alloc_by_player.size(); p++) {
        alloc[alloc_by_player[p]].insert(p);
      }
      return false;
    }
  }
  return true;
}

bool BmfSolver::get_alloc(const Eigen::VectorXd& fair_sharing, const allocation_map_t& last_alloc,
                          allocation_map_t& alloc, bool initial)
{
  alloc.clear();
  for (int player_idx = 0; player_idx < A_.cols(); player_idx++) {
    int selected_resource = NO_RESOURCE;

    /* the player's maximal rate is the minimum among all resources */
    double min_rate = -1;
    for (int cnst_idx = 0; cnst_idx < A_.rows(); cnst_idx++) {
      if (A_(cnst_idx, player_idx) <= 0.0)
        continue;

      /* Note: the max_ may artificially increase the rate if priority < 0
       * The equilibrium sets a rho which respects the C_ though */
      if (double rate = fair_sharing[cnst_idx] / maxA_(cnst_idx, player_idx);
          min_rate == -1 || double_positive(min_rate - rate, cfg_bmf_precision)) {
        selected_resource = cnst_idx;
        min_rate          = rate;
      }
      /* Given that the priority may artificially increase the rate,
       * we need to check that the bound given by user respects the resource capacity C_ */
      if (double bound = initial ? -1 : phi_[player_idx]; bound > 0 &&
                                                          bound * A_(cnst_idx, player_idx) < C_[cnst_idx] &&
                                                          double_positive(min_rate - bound, cfg_bmf_precision)) {
        selected_resource = NO_RESOURCE;
        min_rate          = bound;
      }
    }
    alloc[selected_resource].insert(player_idx);
  }
  if (alloc == last_alloc) // considered stable
    return true;

  if (auto alloc_by_player = alloc_map_to_vector(alloc); not allocations_.insert(alloc_by_player).second) {
    /* oops, allocation already tried, let's pertube it a bit */
    XBT_DEBUG("Allocation already tried: %s", debug_alloc(alloc).c_str());
    return disturb_allocation(alloc, alloc_by_player);
  }
  return false;
}

void BmfSolver::set_fair_sharing(const allocation_map_t& alloc, const Eigen::VectorXd& rho,
                                 Eigen::VectorXd& fair_sharing) const
{
  std::vector<int> bounded_players = get_bounded_players(alloc);

  for (int r = 0; r < fair_sharing.size(); r++) {
    auto it = alloc.find(r);
    if (it != alloc.end()) { // resource selected by some player, fair share depends on rho
      double min_share = std::numeric_limits<double>::max();
      for (int p : it->second) {
        double share = A_(r, p) * rho[p];
        min_share    = std::min(min_share, share);
      }
      fair_sharing[r] = min_share;
    } else { // nobody selects this resource, fair_sharing depends on resource saturation
      // resource r is saturated (A[r,*] * rho > C), divide it among players
      double consumption_r = A_.row(r) * rho;
      double_update(&consumption_r, C_[r], cfg_bmf_precision);
      if (consumption_r > 0.0) {
        fair_sharing[r] = get_maxmin_share(r, bounded_players);
      } else {
        fair_sharing[r] = C_[r];
      }
    }
  }
}

bool BmfSolver::is_bmf(const Eigen::VectorXd& rho) const
{
  bool bmf = true;

  // 1) the capacity of all resources is respected
  Eigen::VectorXd shared(C_shared_.size());
  for (int j = 0; j < shared.size(); j++)
    shared[j] = C_shared_[j] ? 1.0 : 0.0;

  Eigen::VectorXd remaining = (A_ * rho) - C_;
  remaining                 = remaining.array() * shared.array(); // ignore non shared resources
  bmf                       = bmf && (not std::any_of(remaining.data(), remaining.data() + remaining.size(),
                                                      [](double v) { return double_positive(v, sg_precision_workamount); }));

  // 3) every player receives maximum share in at least 1 saturated resource
  // due to subflows, compare with the maximum consumption and not the A matrix
  Eigen::MatrixXd usage =
      maxA_.array().rowwise() * rho.transpose().array(); // usage_ji: indicates the usage of player i on resource j

  XBT_DEBUG("Usage_ji considering max consumption:\n%s", debug_eigen(usage).c_str());
  auto max_share = usage.rowwise().maxCoeff(); // max share for each resource j

  // matrix_ji: boolean indicating player p has the maximum share at resource j
  Eigen::MatrixXi player_max_share =
      ((usage.array().colwise() - max_share.array()).abs() <= sg_precision_workamount).cast<int>();
  // but only saturated resources must be considered
  Eigen::VectorXi saturated = (remaining.array().abs() <= sg_precision_workamount).cast<int>();
  XBT_DEBUG("Saturated_j resources:\n%s", debug_eigen(saturated).c_str());
  player_max_share.array().colwise() *= saturated.array();

  // just check if it has received at least it's bound
  for (int p = 0; p < rho.size(); p++) {
    if (double_equals(rho[p], phi_[p], sg_precision_workamount)) {
      player_max_share(0, p) = 1; // it doesn't really matter, just to say that it's a bmf
      saturated[0]           = 1;
    }
  }

  // 2) at least 1 resource is saturated
  bmf = bmf && (saturated.array() == 1).any();

  XBT_DEBUG("Player_ji usage of saturated resources:\n%s", debug_eigen(player_max_share).c_str());
  // for all columns(players) it has to be the max at least in 1
  bmf = bmf && (player_max_share.colwise().sum().array() >= 1).all();
  return bmf;
}

Eigen::VectorXd BmfSolver::solve()
{
  XBT_DEBUG("Starting BMF solver");

  XBT_DEBUG("A:\n%s", debug_eigen(A_).c_str());
  XBT_DEBUG("maxA:\n%s", debug_eigen(maxA_).c_str());
  XBT_DEBUG("C:\n%s", debug_eigen(C_).c_str());
  XBT_DEBUG("phi:\n%s", debug_eigen(phi_).c_str());

  /* no flows to share, just returns */
  if (A_.cols() == 0)
    return {};

  int it            = 0;
  auto fair_sharing = C_;

  /* BMF allocation for each player (current and last one) stop when are equal */
  allocation_map_t last_alloc;
  allocation_map_t cur_alloc;
  Eigen::VectorXd rho;

  while (it < max_iteration_ && not get_alloc(fair_sharing, last_alloc, cur_alloc, it == 0)) {
    last_alloc = cur_alloc;
    XBT_DEBUG("BMF: iteration %d", it);
    XBT_DEBUG("B (current allocation): %s", debug_alloc(cur_alloc).c_str());

    // solve inv(A)*rho = C
    rho = equilibrium(cur_alloc);
    XBT_DEBUG("rho:\n%s", debug_eigen(rho).c_str());

    // get fair sharing for each resource
    set_fair_sharing(cur_alloc, rho, fair_sharing);
    XBT_DEBUG("Fair sharing vector (per resource):\n%s", debug_eigen(fair_sharing).c_str());

    // get new allocation for players
    it++;
  }

  /* Not mandatory but a safe check to assure we have a proper solution */
  if (not is_bmf(rho)) {
    fprintf(stderr, "Unable to find a BMF allocation for your system.\n"
                    "You may try to increase the maximum number of iterations performed by BMF solver "
                    "(\"--cfg=bmf/max-iterations\").\n"
                    "Additionally, you could adjust numerical precision (\"--cfg=bmf/precision\").\n");
    fprintf(stderr, "Internal states (after %d iterations):\n", it);
    fprintf(stderr, "A:\n%s\n", debug_eigen(A_).c_str());
    fprintf(stderr, "maxA:\n%s\n", debug_eigen(maxA_).c_str());
    fprintf(stderr, "C:\n%s\n", debug_eigen(C_).c_str());
    fprintf(stderr, "C_shared:\n%s\n", debug_vector(C_shared_).c_str());
    fprintf(stderr, "phi:\n%s\n", debug_eigen(phi_).c_str());
    fprintf(stderr, "rho:\n%s\n", debug_eigen(rho).c_str());
    xbt_abort();
  }

  XBT_DEBUG("BMF done after %d iterations", it);
  return rho;
}

/*****************************************************************************/

void BmfSystem::get_flows_data(Eigen::Index number_cnsts, Eigen::MatrixXd& A, Eigen::MatrixXd& maxA,
                               Eigen::VectorXd& phi)
{
  A.resize(number_cnsts, variable_set.size());
  A.setZero();
  maxA.resize(number_cnsts, variable_set.size());
  maxA.setZero();
  phi.resize(variable_set.size());

  int var_idx = 0;
  for (Variable& var : variable_set) {
    if (var.sharing_penalty_ <= 0)
      continue;
    bool active = false;
    bool linked = false; // variable is linked to some constraint (specially for selective_update)
    for (const Element& elem : var.cnsts_) {
      if (const auto& cnst_hook = selective_update_active ? elem.constraint->modified_constraint_set_hook_
                                                          : elem.constraint->active_constraint_set_hook_;
          not cnst_hook.is_linked())
        continue;
      /* active and linked variable, lets check its consumption */
      linked             = true;
      double consumption = elem.consumption_weight;
      if (consumption > 0) {
        int cnst_idx = cnst2idx_[elem.constraint];
        A(cnst_idx, var_idx) += consumption;
        // a variable with double penalty must receive half share, so it max weight is greater
        maxA(cnst_idx, var_idx) = std::max(maxA(cnst_idx, var_idx), elem.max_consumption_weight * var.sharing_penalty_);
        active                  = true;
      }
    }
    /* skip variables not linked to any modified or active constraint */
    if (not linked)
      continue;
    if (active) {
      phi[var_idx]      = var.get_bound();
      idx2Var_[var_idx] = &var;
      var_idx++;
    } else {
      var.value_ = 1; // assign something by default for tasks with 0 consumption
    }
  }
  // resize matrix to active variables only
  A.conservativeResize(Eigen::NoChange_t::NoChange, var_idx);
  maxA.conservativeResize(Eigen::NoChange_t::NoChange, var_idx);
  phi.conservativeResize(var_idx);
}

template <class CnstList>
void BmfSystem::get_constraint_data(const CnstList& cnst_list, Eigen::VectorXd& C, std::vector<bool>& shared)
{
  C.resize(cnst_list.size());
  shared.resize(cnst_list.size());
  cnst2idx_.clear();
  int cnst_idx = 0;
  for (const Constraint& cnst : cnst_list) {
    C(cnst_idx)      = cnst.bound_;
    if (cnst.get_sharing_policy() == Constraint::SharingPolicy::NONLINEAR && cnst.dyn_constraint_cb_) {
      C(cnst_idx) = cnst.dyn_constraint_cb_(cnst.bound_, cnst.concurrency_current_);
    }
    cnst2idx_[&cnst] = cnst_idx;
    // FATPIPE links aren't really shared
    shared[cnst_idx] = (cnst.sharing_policy_ != Constraint::SharingPolicy::FATPIPE);
    cnst_idx++;
  }
}

void BmfSystem::do_solve()
{
  if (selective_update_active)
    bmf_solve(modified_constraint_set);
  else
    bmf_solve(active_constraint_set);
}

template <class CnstList> void BmfSystem::bmf_solve(const CnstList& cnst_list)
{
  idx2Var_.clear();
  cnst2idx_.clear();
  Eigen::MatrixXd A;
  Eigen::MatrixXd maxA;
  Eigen::VectorXd C;
  Eigen::VectorXd bounds;
  std::vector<bool> shared;
  get_constraint_data(cnst_list, C, shared);
  get_flows_data(C.size(), A, maxA, bounds);

  auto solver = BmfSolver(std::move(A), std::move(maxA), std::move(C), std::move(shared), std::move(bounds));
  auto rho    = solver.solve();

  if (rho.size() == 0)
    return;

  /* setting rhos */
  for (int i = 0; i < rho.size(); i++) {
    idx2Var_[i]->value_ = rho[i];
  }
}

} // namespace simgrid::kernel::lmm
