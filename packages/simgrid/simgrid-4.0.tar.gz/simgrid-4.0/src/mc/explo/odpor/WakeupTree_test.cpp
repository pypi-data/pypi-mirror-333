/* Copyright (c) 2017-2025. The SimGrid Team. All rights reserved.               */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "src/3rd-party/catch.hpp"
#include "src/mc/explo/odpor/Execution.hpp"
#include "src/mc/explo/odpor/WakeupTree.hpp"
#include "src/mc/explo/odpor/odpor_forward.hpp"
#include "src/mc/explo/udpor/udpor_tests_private.hpp"

using namespace simgrid::mc;
using namespace simgrid::mc::odpor;
using namespace simgrid::mc::udpor;

static PartialExecution get_node_post_order_traversal(const WakeupTreeNode* node)
{

  PartialExecution traversal = {};
  for (auto const& child : node->get_ordered_children()) {
    auto recursive_traversal = get_node_post_order_traversal(child.get());
    traversal.insert(traversal.end(), recursive_traversal.begin(), recursive_traversal.end());
  }

  traversal.push_back(node->get_action());
  return traversal;
}

static PartialExecution get_tree_post_order_traversal(const WakeupTree& tree)
{

  PartialExecution traversal = {};
  for (auto const& child_aid : tree.get_direct_children_actors()) {
    auto const& child        = tree.get_node_after_actor(child_aid);
    auto recursive_traversal = get_node_post_order_traversal(child);
    traversal.insert(traversal.end(), recursive_traversal.begin(), recursive_traversal.end());
  }

  return traversal;
}

static void compare_tree(const WakeupTree& tree, PartialExecution seq)
{
  REQUIRE(get_tree_post_order_traversal(tree) == seq);
}

static void test_tree_empty(const WakeupTree& tree)
{
  REQUIRE(tree.empty());
  REQUIRE_FALSE(tree.get_min_single_process_node().has_value());
  REQUIRE_FALSE(tree.get_min_single_process_actor().has_value());
  REQUIRE(get_tree_post_order_traversal(tree) == PartialExecution());
}

TEST_CASE("simgrid::mc::odpor::WakeupTree: Constructing Trees")
{
  SECTION("Constructing empty trees")
  {
    test_tree_empty(WakeupTree());
  }

  SECTION("Testing subtree creation and manipulation")
  {
    // Here, we make everything dependent. This will ensure that each unique sequence
    // inserted into the tree never "eventually looks like"
    const auto a0 = std::make_shared<DependentAction>(Transition::Type::UNKNOWN, 1);
    const auto a1 = std::make_shared<DependentAction>(Transition::Type::UNKNOWN, 2);
    const auto a2 = std::make_shared<DependentAction>(Transition::Type::UNKNOWN, 3);
    const auto a3 = std::make_shared<DependentAction>(Transition::Type::UNKNOWN, 4);
    const auto a4 = std::make_shared<DependentAction>(Transition::Type::UNKNOWN, 5);
    const auto a5 = std::make_shared<DependentAction>(Transition::Type::UNKNOWN, 6);

    Execution execution;
    execution.push_transition(a0);
    execution.push_transition(a1);
    execution.push_transition(a2);
    execution.push_transition(a3);
    execution.push_transition(a4);
    execution.push_transition(a5);

    // The tree is as follows:
    //                  {}
    //               /     /
    //             a1       a4
    //           /    /       /
    //          a2    a3       a2
    //         /     /   /      /
    //        a3    a2   a5     a1
    //       /     /             /
    //      a4    a4             a3
    //
    // Recall that new nodes (in this case the one with
    // action `a2`) are added such that they are "greater than" (under
    // the tree's `<` relation) all those that exist under the given parent
    WakeupTree tree;
    REQUIRE(tree.insert({a1, a2, a3, a4}) == InsertionResult::root);
    tree.insert({a1, a3, a2, a4});
    tree.insert({a1, a3, a2, a4, a5});
    tree.insert({a1, a3, a5});
    tree.insert({a4, a2, a1, a3});
    REQUIRE(get_tree_post_order_traversal(tree) == PartialExecution{a4, a3, a2, a4, a2, a5, a3, a1, a3, a1, a2, a4});

    SECTION("Moving the first single-process subtree")
    {
      // Prior to removal, the first `a1` was the first single-process node
      REQUIRE(tree.get_min_single_process_node().has_value());
      REQUIRE(tree.get_min_single_process_actor().has_value());
      REQUIRE(tree.get_min_single_process_actor().value() == a1->aid_);

      auto subtree_a1 = tree.get_first_subtree();

      // Now the first `a4` is
      REQUIRE(tree.get_min_single_process_node().has_value());
      REQUIRE(tree.get_min_single_process_actor().has_value());
      REQUIRE(tree.get_min_single_process_actor().value() == a4->aid_);
      compare_tree(subtree_a1, {a4, a3, a2, a4, a2, a5, a3});
      compare_tree(tree, {a3, a1, a2, a4});
      tree.get_first_subtree();

      // At this point, we've removed each single-process subtree, so
      // the tree should be empty
      REQUIRE(tree.empty());
    }

    SECTION("Removing the first single-process subtree from an empty tree has no effect")
    {
      WakeupTree empty_tree;
      test_tree_empty(empty_tree);

      empty_tree.get_first_subtree();

      // There should be no effect: the tree should still be empty
      // and the function should have no effect
      test_tree_empty(empty_tree);
    }
  }
}

TEST_CASE("simgrid::mc::odpor::WakeupTree: Testing Insertion for Empty Executions")
{
  SECTION("Following an execution")
  {
    // We imagine the following completed execution `E`
    // consisting of executing actions a0-a3. Execution
    // `E` is the first such maximal execution explored
    // by ODPOR, which implies that a) all sleep sets are
    // empty and b) all wakeup trees (i.e. for each prefix) consist of the root
    // node with a single leaf containing the action
    // taken, save for the wakeup tree of the execution itself
    // which is empty.

    // We first notice that there's a reversible race between
    // events 0 and 3.

    const auto a0 = std::make_shared<DependentAction>(Transition::Type::UNKNOWN, 3);
    const auto a1 = std::make_shared<IndependentAction>(Transition::Type::UNKNOWN, 4);
    const auto a2 = std::make_shared<ConditionallyDependentAction>(Transition::Type::UNKNOWN, 1);
    const auto a3 = std::make_shared<ConditionallyDependentAction>(Transition::Type::UNKNOWN, 4);
    const auto a4 = std::make_shared<DependentAction>(Transition::Type::UNKNOWN, 2);

    Execution execution;
    execution.push_transition(a0);
    execution.push_transition(a1);
    execution.push_transition(a2);
    execution.push_transition(a3);
    execution.push_transition(a4);

    REQUIRE(execution.get_racing_events_of(2) == std::list<Execution::EventHandle>{0});
    REQUIRE(execution.get_racing_events_of(3) == std::list<Execution::EventHandle>{0});

    WakeupTree tree;

    SECTION("Attempting to insert the empty sequence into an empty tree should have no effect")
    {
      tree.insert({});
      test_tree_empty(tree);
    }

    // First, we initialize the tree to how it looked prior
    // to the insertion of the race.
    tree.insert({a0});

    // Then, after insertion, we ensure that the node was
    // indeed added to the tree.
    tree.insert({a1, a3});
    compare_tree(tree, {a0, a3, a1});

    SECTION("Attempting to re-insert the same EXACT sequence should have no effect")
    {
      tree.insert({a1, a3});
      compare_tree(tree, {a0, a3, a1});
    }

    SECTION("Attempting to re-insert an equivalent sequence should have no effect")
    {
      // a3 and a1 are interchangeable since `a1` is independent with everything.
      // Since we found an equivalent sequence that is a leaf, nothing should result..
      tree.insert({a3, a1});
      compare_tree(tree, {a0, a3, a1});
    }

    SECTION("Attempting to insert the empty sequence should have no effect")
    {
      tree.insert({});
      compare_tree(tree, {a0, a3, a1});
    }

    SECTION("Inserting an extension should create a branch point")
    {
      // `a1.a2` shares the same `a1` prefix as `a1.a3`. Thus, the tree
      // should now look as follows:
      //
      //                 {}
      //               /    /
      //             a0     a1
      //                   /   /
      //                  a3   a4
      //
      // Recall that new nodes (in this case the one with
      // action `a2`) are added such that they are "greater than" (under
      // the tree's `<` relation) all those that exist under the given parent.
      tree.insert({a1, a4});
      compare_tree(tree, {a0, a3, a4, a1});
    }

    SECTION("Inserting an equivalent sequence to a leaf should preserve the tree as-is")
    {
      // `a1.a2` is equivalent to `a1.a3` since `a2` and `a3` are independent
      // (`E ⊢ p ◊ w` where `p := proc(a2)` and `w := a3`). Thus, the tree
      // should now STILL look as follows:
      //
      //                 {}
      //               /    /
      //             a0     a1
      //                   /
      //                  a3
      //
      // Recall that new nodes (in this case the one with
      // action `a2`) are added such that they are "greater than" (under
      // the tree's `<` relation) all those that exist under the given parent.
      tree.insert({a1, a3});
      compare_tree(tree, {a0, a3, a1});
    }

  SECTION("Performing Arbitrary Insertions")
  {
    const auto a0 = std::make_shared<DependentAction>(Transition::Type::UNKNOWN, 2);
    const auto a1 = std::make_shared<IndependentAction>(Transition::Type::UNKNOWN, 4);
    const auto a2 = std::make_shared<ConditionallyDependentAction>(Transition::Type::UNKNOWN, 3);
    const auto a3 = std::make_shared<DependentAction>(Transition::Type::UNKNOWN, 1);
    const auto a4 = std::make_shared<IndependentAction>(Transition::Type::UNKNOWN, 2);
    const auto a5 = std::make_shared<ConditionallyDependentAction>(Transition::Type::UNKNOWN, 4);
    WakeupTree tree;

    SECTION("Attempting to insert the empty sequence into an empty tree should have no effect")
    {
      tree.insert({});
      test_tree_empty(tree);
    }

    SECTION("Attempting to re-insert the same sequence multiple times should have no extra effect")
    {
      tree.insert({a4});
      tree.insert({a4});
      tree.insert({a4});
      compare_tree(tree, {a4});
    }

    SECTION("Attempting to insert an independent sequence same should have no extra effect")
    {
      // a4 and a1 are independent actions. Intuitively, then, we need only
      // search one ordering of the two actions. The wakeup tree handles
      // this by computing the `~` relation. The relation itself determines
      // whether the `a1` is an initial of `a3`, which it is not. It then
      // checks whether `a1` is independent with everything in the sequence
      // (in this case, consisting only of `a1`) which IS true. Since `a4`
      // is already a leaf node of the tree, it suffices to only have `a4`
      // in this tree to guide ODPOR.
      tree.insert({a4});
      tree.insert({a1});
      compare_tree(tree, {a4});
    }

    SECTION(
        "Attempting to insert a progression of executions should have no extra effect when the first process is a leaf")
    {
      // All progressions starting with `a0` are effectively already accounted
      // for by inserting `a0` since we `a0` "can always be made to look like"
      // (viz. the `~` relation) `a0.*` where `*` is some sequence of actions
      tree.insert({a0});
      tree.insert({a0, a3});
      tree.insert({a0, a3, a2});
      tree.insert({a0, a3, a2, a4});
      tree.insert({a0, a3, a2, a4});
      compare_tree(tree, {a0});
    }

    SECTION("Stress test with multiple branch points: `~_E` with different looking sequences")
    {
      // After the insertions below, the tree looks like the following:
      //                {}
      //              /    /
      //            a0     a2
      //                 /  |   /
      //               a0  a3   a5
      tree.insert({a0});
      tree.insert({a2, a0});
      tree.insert({a2, a3});
      tree.insert({a2, a5});
      compare_tree(tree, {a0, a0, a3, a5, a2});
      SECTION("Adding more stress")
      {
        // In this case, `a2` and `a1` can be interchanged with each other.
        // Thus `a2.a1 == a1.a2`. Since there is already an interior node
        // containing `a2`, we attempt to add the what remains (viz. `a1`) to the
        // series. HOWEVER: we notice that `a2.a5` is "eventually equivalent to"
        // (that is `~` with) `a1.a2` since `a2` is an initial of the latter and
        // `a1` and `a5` are independent of each other.
        tree.insert({a1, a2});
        compare_tree(tree, {a0, a0, a3, a5, a2});

        // With a3.a0, we notice that starting a sequence with `a3` is
        // always different than starting one with either `a0` or
        //
        // After the insertion, the tree looks like the following:
        //                     {}
        //              /     /        /
        //            a0     a2        a3
        //                 /  |  \     |
        //               a0  a3  a5    a0
        tree.insert({a3, a0});
        compare_tree(tree, {a0, a0, a3, a5, a2, a0, a3});
      }
    }
  }

  SECTION("Insertion with more subtle equivalents")
  {
    const auto cd_1 = std::make_shared<ConditionallyDependentAction>(Transition::Type::UNKNOWN, 1);
    const auto i_2  = std::make_shared<IndependentAction>(Transition::Type::UNKNOWN, 2);
    const auto i_3  = std::make_shared<IndependentAction>(Transition::Type::UNKNOWN, 3);
    const auto d_1  = std::make_shared<DependentAction>(Transition::Type::UNKNOWN, 1);
    const auto d_2  = std::make_shared<DependentAction>(Transition::Type::UNKNOWN, 2);
    WakeupTree complex_tree;
    // After the insertions below, the tree looks like the following:
    //                              {}
    //                           /     /
    //                       cd_1      i_2
    //                       /            /
    //                    i_2              d_2
    //                   /                  /
    //                 d_1                 cd_1
    //                 /                 /      /
    //               i_3               d_1      i_3
    //              /                  /          /
    //            d_2                i_3          d_2
    //            /                  /              /
    //          d_2                d_2              d_1
    //
    // d_1.i_3.d_2 is equivalent to i_3.d_2.d_1
    complex_tree.insert({cd_1, i_2, d_1, i_3, d_2, d_2});
    complex_tree.insert({i_2, d_2, cd_1, d_1, i_3, d_2});
    complex_tree.insert({i_2, d_2, cd_1, i_3, d_2, d_1});
    compare_tree(complex_tree, {d_2, d_2, i_3, d_1, i_2, cd_1, d_2, i_3, d_1, d_1, d_2, i_3, cd_1, d_2, i_2});

    // Here we note that the sequence that we are attempting to insert, viz.
    //
    //    i_3.i_2.d_2.cd_1.d_2.d_1
    //
    // is already equivalent to
    //
    //    i_2.d_2.cd_1.i_3.d_2.d_1
    complex_tree.insert({i_3, i_2, d_2, cd_1, d_2, d_1});
    compare_tree(complex_tree, {d_2, d_2, i_3, d_1, i_2, cd_1, d_2, i_3, d_1, d_1, d_2, i_3, cd_1, d_2, i_2});

    // Here we note that the sequence that we are attempting to insert, viz.
    //
    //    i_2.d_2.cd_1.d_1.i_3
    //
    // is already equivalent to
    //
    //    i_2.d_2.cd_1.i_3.d_2.d_1
    complex_tree.insert({i_2, d_2, cd_1, d_1, i_3});
    compare_tree(complex_tree, {d_2, d_2, i_3, d_1, i_2, cd_1, d_2, i_3, d_1, d_1, d_2, i_3, cd_1, d_2, i_2});

    // Here we note that the sequence that we are attempting to insert, viz.
    //
    //    i_2.d_2.cd_1
    //
    // is accounted for by an interior node of the tree. Since there is no
    // "extra" portions that are different from what is already
    // contained in the tree, nothing is added and the tree stays the same
    complex_tree.insert({i_2, d_2, cd_1});
    compare_tree(complex_tree, {d_2, d_2, i_3, d_1, i_2, cd_1, d_2, i_3, d_1, d_1, d_2, i_3, cd_1, d_2, i_2});
  }
  }
}
