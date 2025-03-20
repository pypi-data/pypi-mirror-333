/* Copyright (c) 2014-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#ifndef SIMGRID_MC_MMU_HPP
#define SIMGRID_MC_MMU_HPP

#include "xbt/misc.h"
#include <cstdint>
#include <utility>

namespace simgrid::mc::mmu {
// TODO, do not depend on xbt_pagesize/xbt_pagebits but our own chunk size

/** @brief How many memory pages are necessary to store size bytes?
 *
 *  @param size Byte size
 *  @return Number of memory pages
 */
static XBT_ALWAYS_INLINE std::size_t chunk_count(std::size_t size)
{
  std::size_t page_count = size >> xbt_pagebits;
  if (size & (xbt_pagesize - 1))
    page_count++;
  return page_count;
}

/** @brief Split into chunk number and remaining offset */
static XBT_ALWAYS_INLINE std::pair<std::size_t, std::uintptr_t> split(std::uintptr_t offset)
{
  return {offset >> xbt_pagebits, offset & (xbt_pagesize - 1)};
}

/** Merge chunk number and remaining offset into a global offset */
static XBT_ALWAYS_INLINE std::uintptr_t join(std::size_t page, std::uintptr_t offset)
{
  return ((std::uintptr_t)page << xbt_pagebits) + offset;
}

static XBT_ALWAYS_INLINE std::uintptr_t join(std::pair<std::size_t, std::uintptr_t> value)
{
  return join(value.first, value.second);
}

static XBT_ALWAYS_INLINE bool same_chunk(std::uintptr_t a, std::uintptr_t b)
{
  return (a >> xbt_pagebits) == (b >> xbt_pagebits);
}
} // namespace simgrid::mc::mmu

#endif
