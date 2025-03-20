/* Copyright (c) 2015-2025. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#ifndef SIMGRID_MC_PROTOCOL_H
#define SIMGRID_MC_PROTOCOL_H

// ***** Environment variables for passing context to the model-checked process

#ifdef __cplusplus

#include "simgrid/forward.h" // aid_t
#include "src/mc/datatypes.h"
#include <xbt/utility.hpp>

#include <array>
#include <cstdint>
#include <sys/un.h>

// ***** Messages
namespace simgrid::mc {

XBT_DECLARE_ENUM_CLASS(MessageType, NONE, FORK, FORK_REPLY, WAIT_CHILD, WAIT_CHILD_REPLY, CONTINUE, DEADLOCK_CHECK,
                       DEADLOCK_CHECK_REPLY, WAITING, SIMCALL_EXECUTE, SIMCALL_EXECUTE_REPLY, ASSERTION_FAILED,
                       ACTORS_STATUS, ACTORS_STATUS_REPLY_COUNT, ACTORS_STATUS_REPLY_SIMCALL,
                       ACTORS_STATUS_REPLY_TRANSITION, ACTORS_MAXPID, ACTORS_MAXPID_REPLY, FINALIZE, FINALIZE_REPLY,
                       REPLAY, GO_ONE_WAY);
} // namespace simgrid::mc

constexpr unsigned MC_MESSAGE_LENGTH                 = 48 * 1024 * 1024;
constexpr unsigned MC_SOCKET_NAME_LEN                = sizeof(sockaddr_un::sun_path);
constexpr unsigned SIMCALL_SERIALIZATION_BUFFER_SIZE = 2048;

/** Basic structure for a MC message
 *
 *  The current version of the client/server protocol sends C structures over `AF_UNIX`
 *  `SOCK_SEQPACKET` sockets. This means that the protocol is ABI/architecture specific:
 *  we currently can't model-check a x86 process from a x86_64 process.
 *
 *  Moreover the protocol is not stable. The same version of the library should be used
 *  for the client and the server.
 */

/* Basic structure: all message start with a message type */
struct s_mc_message_t {
  simgrid::mc::MessageType type;
};

struct s_mc_message_int_t {
  simgrid::mc::MessageType type;
  uint64_t value;
};

/* Client->Server */

/* Server -> client */
struct s_mc_message_fork_t {
  simgrid::mc::MessageType type;
  std::array<char, MC_SOCKET_NAME_LEN> socket_name;
};

struct s_mc_message_simcall_execute_t {
  simgrid::mc::MessageType type;
  aid_t aid_;
  int times_considered_;
  bool want_transition;
};
struct s_mc_message_simcall_execute_answer_t {
  simgrid::mc::MessageType type;
  aid_t aid;
};

struct s_mc_message_actors_status_t {
  simgrid::mc::MessageType type;
  bool want_transitions_;
};

struct s_mc_message_actors_status_answer_t {
  simgrid::mc::MessageType type;
  int count;
};

struct s_mc_message_one_way_t {
  simgrid::mc::MessageType type;
  bool want_transitions;
  bool is_random;
};

struct s_mc_message_actors_status_one_t { // an array of `s_mc_message_actors_status_one_t[count]` is sent right after
                                          // after a `s_mc_message_actors_status_answer_t`
  simgrid::mc::MessageType type;
  aid_t aid;
  bool enabled;
  int max_considered;
};

#endif // __cplusplus
#endif
