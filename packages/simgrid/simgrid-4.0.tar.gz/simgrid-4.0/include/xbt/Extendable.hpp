/* Copyright (c) 2015-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#ifndef SIMGRID_XBT_LIB_HPP
#define SIMGRID_XBT_LIB_HPP

#include <cstddef>
#include <functional>
#include <limits>
#include <memory>
#include <vector>

namespace simgrid::xbt {

template<class T, class U> class Extension;
template<class T>          class Extendable;

template<class T, class U>
class Extension {
  static constexpr std::size_t INVALID_ID = std::numeric_limits<std::size_t>::max();
  std::size_t id_                         = INVALID_ID;
  friend class Extendable<T>;
  explicit constexpr Extension(std::size_t id) : id_(id) {}
public:
  explicit constexpr Extension() = default;
  std::size_t id() const { return id_; }
  bool valid() const { return id_ != INVALID_ID; }
};

/** An Extendable is an object that you can extend with external elements.
 *
 * An Extension is one dimension of such extension. They are similar to the concept of mixins, that is, a set of behavior that is injected into a class without derivation.
 *
 * Imagine that you want to write a plugin dealing with the energy in SimGrid.
 * You will have to store some information about each and every host.
 *
 * You could modify the Host class directly (but your code will soon become messy).
 * You could create a class EnergyHost deriving Host, but it is not easily combinable
 *    with a notion of Host extended with another concept (such as mobility).
 * You could completely externalize these data with an associative map Host->EnergyHost.
 *    It would work, provided that you implement this classical feature correctly (and it would induce a little performance penalty).
 * Instead, you should add a new extension to the Host class, that happens to be Extendable.
 *
 */
template<class T>
class Extendable {
private:
  static std::vector<std::function<void(void*)>> deleters_;
  std::vector<void*> extensions_{deleters_.size(), nullptr};

public:
  static size_t extension_create(const std::function<void(void*)>& deleter)
  {
    deleters_.emplace_back(deleter);
    return deleters_.size() - 1;
  }
  template <class U> static Extension<T, U> extension_create(const std::function<void(void*)>& deleter)
  {
    return Extension<T,U>(extension_create(deleter));
  }
  template<class U> static
  Extension<T,U> extension_create()
  {
    return Extension<T, U>(extension_create([](void* p) { delete static_cast<U*>(p); }));
  }
  Extendable()                  = default;
  Extendable(const Extendable&) = delete;
  Extendable& operator=(const Extendable&) = delete;
  ~Extendable()
  {
    /* Call destructors in reverse order of their registrations
     *
     * The rationale for this, is that if an extension B as been added after
     * an extension A, the subsystem of B might depend on the subsystem on A and
     * an extension of B might need to have the extension of A around when executing
     * its cleanup function/destructor. */
    for (std::size_t i = extensions_.size(); i > 1; --i) // rank=0 is the spot of user's void*
      if (extensions_[i - 1] != nullptr && deleters_[i - 1])
        deleters_[i - 1](extensions_[i - 1]);
  }

  // Type-unsafe versions of the facet access methods:
  void* extension(std::size_t rank) const
  {
    return rank < extensions_.size() ? extensions_[rank] : nullptr;
  }
  void extension_set(std::size_t rank, void* value, bool use_dtor = true)
  {
    if (rank >= extensions_.size())
      extensions_.resize(rank + 1, nullptr);
    void* old_value = this->extension(rank);
    extensions_[rank] = value;
    if (use_dtor && old_value != nullptr && deleters_[rank])
      deleters_[rank](old_value);
  }

  // Type safe versions of the facet access methods:
  template <class U> U* extension(Extension<T, U> rank) const { return static_cast<U*>(extension(rank.id())); }
  template<class U>
  void extension_set(Extension<T,U> rank, U* value, bool use_dtor = true)
  {
    extension_set(rank.id(), value, use_dtor);
  }
  // void* version, for C users and nostalgics
  void set_data(void* data){
    extensions_[0]=data;
  }
  template <typename D> D* get_data() const { return static_cast<D*>(extensions_[0]); }
  template <typename D> std::unique_ptr<D> get_unique_data() { return std::unique_ptr<D>(get_data<D>()); }

  // Convenience extension access when the type has an associated EXTENSION ID:
  template <class U> U* extension() const { return extension<U>(U::EXTENSION_ID); }
  template<class U> void extension_set(U* p) { extension_set<U>(U::EXTENSION_ID, p); }
};

// Initialized with a first element, to save space for void* user data
template <class T> std::vector<std::function<void(void*)>> Extendable<T>::deleters_{1};
} // namespace simgrid::xbt

#endif
