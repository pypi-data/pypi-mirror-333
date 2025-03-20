/* Copyright (c) 2006-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#ifndef SIMGRID_S4U_COND_VARIABLE_HPP
#define SIMGRID_S4U_COND_VARIABLE_HPP

#include <simgrid/forward.h>

#include <simgrid/chrono.hpp>
#include <simgrid/s4u/Engine.hpp>
#include <simgrid/s4u/Mutex.hpp>

#include <future>

namespace simgrid::s4u {

/**
 * @beginrst
 * SimGrid's condition variables are meant to be drop-in replacements of ``std::condition_variable``.
 * Please refer to the `documentation of standard C++ <https://en.cppreference.com/w/cpp/thread/condition_variable>`_
 * for more information on condition variables. A SimGrid example is available in Section :ref:`s4u_ex_IPC`.
 * @endrst
 */
class XBT_PUBLIC ConditionVariable {
private:
#ifndef DOXYGEN
  friend kernel::activity::ConditionVariableImpl;
  friend XBT_PUBLIC void kernel::activity::intrusive_ptr_release(kernel::activity::ConditionVariableImpl* cond);
#endif

  kernel::activity::ConditionVariableImpl* const pimpl_;

  explicit ConditionVariable(kernel::activity::ConditionVariableImpl* cond) : pimpl_(cond) {}
  ~ConditionVariable() = default;
#ifndef DOXYGEN
  ConditionVariable(ConditionVariable const&) = delete;
  ConditionVariable& operator=(ConditionVariable const&) = delete;

  friend XBT_PUBLIC void intrusive_ptr_add_ref(const ConditionVariable* cond);
  friend XBT_PUBLIC void intrusive_ptr_release(const ConditionVariable* cond);
#endif

public:
  /** \static Create a new condition variable and return a smart pointer
   *
   * @beginrst
   * You should only manipulate :cpp:type:`simgrid::s4u::ConditionVariablePtr`, as created by this function (see also :ref:`s4u_raii`).
   * @endrst
   */
  static ConditionVariablePtr create();

  ///  Wait until notification, with no timeout
  void wait(s4u::MutexPtr lock);
  ///  Wait until notification, with no timeout
  void wait(const std::unique_lock<s4u::Mutex>& lock);
  template <class P> void wait(const std::unique_lock<Mutex>& lock, P pred)
  {
    while (not pred())
      wait(lock);
  }

  /// Wait until the given instant (specified as a plain double)
  std::cv_status wait_until(s4u::MutexPtr lock, double timeout_time);
  /// Wait until the given instant (specified as a plain double)
  std::cv_status wait_until(const std::unique_lock<s4u::Mutex>& lock, double timeout_time);
  /// Wait for the given amount of seconds (specified as a plain double)
  std::cv_status wait_for(MutexPtr lock, double timeout);
  /// Wait for the given amount of seconds (specified as a plain double)
  std::cv_status wait_for(const std::unique_lock<s4u::Mutex>& lock, double duration);

  // Wait function taking a C++ style time:

  /// Wait for the given amount of seconds (specified in C++ style)
  template <class Rep, class Period>
  std::cv_status wait_for(const std::unique_lock<s4u::Mutex>& lock, std::chrono::duration<Rep, Period> duration)
  {
    auto seconds = std::chrono::duration_cast<SimulationClockDuration>(duration);
    return this->wait_for(lock, seconds.count());
  }
  /** Wait until the given instant (specified in C++ style) */
  template <class Duration>
  std::cv_status wait_until(const std::unique_lock<s4u::Mutex>& lock, const SimulationTimePoint<Duration>& timeout_time)
  {
    auto timeout_native = std::chrono::time_point_cast<SimulationClockDuration>(timeout_time);
    return this->wait_until(lock, timeout_native.time_since_epoch().count());
  }

  /** Unblock one actor blocked on that condition variable. If none was blocked, nothing happens. */
  void notify_one();
  /** Unblock all actors blocked on that condition variable. If none was blocked, nothing happens. */
  void notify_all();
};

} // namespace simgrid::s4u

#endif
