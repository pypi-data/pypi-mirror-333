.. _S4U_doc:

The S4U Interface
#################

.. raw:: html

   <object id="TOC" data="graphical-toc.svg" type="image/svg+xml"></object>
   <script>
   window.onload=function() { // Wait for the SVG to be loaded before changing it
     var elem=document.querySelector("#TOC").contentDocument.getElementById("ActorBox")
     elem.style="opacity:0.93999999;fill:#ff0000;fill-opacity:0.1;stroke:#000000;stroke-width:0.35277778;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1";
   }
   </script>
   <br/>
   <br/>

The S4U interface (SimGrid for you) mixes the full power of SimGrid
with the full power of C++. This is the preferred interface to describe
abstract algorithms in the domains of Cloud, P2P, HPC, IoT, and similar
settings.

Since v3.33 (Spring 2023), S4U is the main interface of SimGrid for algorithms.
It is feature complete, but may still evolve slightly in future releases.
When this happens, compiling your code will produce deprecation warnings for 4
releases (one year) before the removal of the old symbols.

.. _S4U_main_concepts:

Main Concepts
*************

A typical SimGrid simulation is composed of several |API_s4u_Actors|_, that
execute user-provided functions. The actors have to explicitly use the
S4U interface to express their :ref:`computation <API_s4u_Exec>`,
:ref:`communication <API_s4u_Comm>`, :ref:`disk usage <API_s4u_Io>`,
and other |API_s4u_Activities|_, so that they get reflected within the
simulator. These activities take place on resources such as |API_s4u_Hosts|_,
|API_s4u_Links|_, and |API_s4u_Disks|_. SimGrid predicts the time taken by each
activity and orchestrates the actors accordingly, waiting for the
completion of these activities.


When **communicating**, data is not directly sent to other actors but
posted onto a |API_s4u_Mailbox|_ that serves as a rendezvous point between
communicating actors. This means that you don't need to know who you
are talking to, you just put your communication `Put` request in a
mailbox, and it will be matched with a complementary `Get`
request.  Alternatively, actors can interact through **classical
synchronization mechanisms** such as |API_s4u_Barrier|_, |API_s4u_Semaphore|_,
|API_s4u_Mutex|_, and |API_s4u_ConditionVariable|_.

Each actor is located on a simulated |API_s4u_Host|_. Each host is located
in a |API_s4u_NetZone|_, that knows the networking path between one
resource to another. Each NetZone is included in another one, forming
a tree of NetZones which root zone contains the whole platform. The
actors can also be located on a |API_s4U_VirtualMachine|_ that may
restrict the activities it contains to a limited amount of cores.
Virtual machines can also be migrated between hosts.

The :ref:`simgrid::s4u::this_actor <API_s4u_this_actor>` namespace
provides many helper functions to simplify the code of actors.

.. rst-class:: compact-list

   - **Simulation Elements**

      - :ref:`class Actor <API_s4u_Actor>`: Active entities executing your application.
      - :ref:`class Engine <API_s4u_Engine>`: Simulation engine (singleton).
      - :ref:`class Mailbox <API_s4u_Mailbox>`: Communication rendezvous, with which actors meet each other.

   - **Resources**

      - :ref:`class Disk <API_s4u_Disk>`: Resource on which actors can write and read data.
      - :ref:`class Host <API_s4u_Host>`: Actor location, providing computational power.
      - :ref:`class Link <API_s4u_Link>`: Interconnecting hosts.
      - :ref:`class NetZone <API_s4u_NetZone>`: Sub-region of the platform, containing resources (Hosts, Links, etc).
      - :ref:`class VirtualMachine <API_s4u_VirtualMachine>`: Execution containers that can be moved between Hosts.

   - **Activities** (:ref:`class Activity <API_s4u_Activity>`): The things that actors can do on resources.

      - :ref:`class Comm <API_s4u_Comm>`: Communication activity, started on Mailboxes and consuming links.
      - :ref:`class Exec <API_s4u_Exec>`: Computation activity, started on Host and consuming CPU resources.
      - :ref:`class Io <API_s4u_Io>`: I/O activity, started on and consuming disks.
      - :ref:`class ActivtySet <API_s4u_ActivitySet>`: Bag of activities, to wait for any of the set, or all of them.

   - **Synchronization Objects**: Classical IPC that actors can use

      - :ref:`class Barrier <API_s4u_Barrier>`
      - :ref:`class ConditionVariable <API_s4u_ConditionVariable>`
      - :ref:`class Mutex <API_s4u_Mutex>`
      - :ref:`class Semaphore <API_s4u_Semaphore>`

.. |API_s4u_Actors| replace:: **Actors**
.. _API_s4u_Actors: #api-s4u-actor

.. |API_s4u_Activities| replace:: **Activities**
.. _API_s4u_Activities: #api-s4u-activity

.. |API_s4u_Tasks_link| replace:: **Tasks**
.. _API_s4u_Tasks_link: #api-s4u-task

.. |API_s4u_Hosts| replace:: **Hosts**
.. _API_s4u_Hosts: #api-s4u-host

.. |API_s4u_Links| replace:: **Links**
.. _API_s4u_Links: #api-s4u-link

.. |API_s4u_Disks| replace:: **Disks**
.. _API_s4u_Disks: #api-s4u-disk

.. |API_s4u_VirtualMachine| replace:: **VirtualMachines**

.. |API_s4u_Host| replace:: **Host**

.. |API_s4u_Mailbox| replace:: **Mailbox**

.. |API_s4u_Mailboxes| replace:: **Mailboxes**
.. _API_s4u_Mailboxes: #s4u-mailbox

.. |API_s4u_NetZone| replace:: **NetZone**

.. |API_s4u_Barrier| replace:: **Barrier**

.. |API_s4u_Semaphore| replace:: **Semaphore**

.. |API_s4u_ConditionVariable| replace:: **ConditionVariable**

.. |API_s4u_Mutex| replace:: **Mutex**

.. _s4u_Activities:

Activities
**********

Activities represent the actions that consume a resource, such as a
:ref:`Comm <API_s4u_Comm>` that consumes the *transmitting power* of
:ref:`Link <API_s4u_Link>` resources, or an :ref:`Exec <API_s4u_Exec>`
that consumes the *computing power* of :ref:`Host <API_s4u_Host>` resources.
See also the :ref:`full API <API_s4u_Activity>` below.

=======================
Asynchronous Activities
=======================

Every activity can be either **blocking** or **asynchronous**. For
example, :cpp:func:`s4u::Mailbox::put() <simgrid::s4u::Mailbox::put>`
and :cpp:func:`s4u::Mailbox::get() <simgrid::s4u::Mailbox::get>`
create blocking communications: the actor is blocked until the
completion of that communication. Asynchronous communications do not
block the actor during their execution but progress on their own.

Once your asynchronous activity is started, you can test for its
completion using :cpp:func:`s4u::Activity::test() <simgrid::s4u::Activity::test>`.
This function returns ``true`` if the activity is completed already.
You can also use :cpp:func:`s4u::Activity::wait() <simgrid::s4u::Activity::wait>`
to block until the completion of the activity. To wait for at most a given amount of time,
use  :cpp:func:`s4u::Activity::wait_for() <simgrid::s4u::Activity::wait_for>`.
Finally, to wait at most until a specified time limit, use
:cpp:func:`s4u::Activity::wait_until() <simgrid::s4u::Activity::wait_until>`.

Every kind of activity can be asynchronous.
:ref:`s4u::CommPtr <API_s4u_Comm>` are created with :cpp:func:`s4u::Mailbox::put_async() <simgrid::s4u::Mailbox::put_async>` and
:cpp:func:`s4u::Mailbox::get_async() <simgrid::s4u::Mailbox::get_async>`;
:ref:`s4u::IoPtr <API_s4u_Io>` are created with :cpp:func:`s4u::Disk::read_async() <simgrid::s4u::Disk::read_async>` and
:cpp:func:`s4u::Disk::write_async() <simgrid::s4u::Disk::write_async>`; and
:ref:`s4u::ExecPtr <API_s4u_Exec>` are created with
:cpp:func:`s4u::Host::exec_async() <simgrid::s4u::Host::exec_async>`.
In the future, it will become possible to have asynchronous IPC such as asynchronous mutex lock requests (it is already possible
internally, but the interface is not exposed in S4U yet).

If you want for the completion of any activity in a given set, to react to the earlier occuring completion, then you need an
:ref:`activity set <API_s4u_ActivitySet>`. Please refer to the :ref:`relevant examples <s4u_ex_activityset>` for more information.

=====================
Activities Life Cycle
=====================

Sometimes, you want to change the setting of an activity before it even starts.

.. todo:: write this section

=====================
Repeatable Activities
=====================

In order to simulate the execution of Dataflow applications, we introduced the
concept of |API_s4u_Tasks_link|, that can be seen as repeatable activities. A Dataflow
is defined as a graph of |API_s4u_Tasks_link|, where each |API_s4u_Tasks_link| has a set of
successors and predecessors. When a |API_s4u_Tasks_link| ends it sends a token to each
of its successors. Each |API_s4u_Tasks_link| has to receive a token from each of its
predecessor to start. Tokens can carry any user-defined data.

|API_s4u_Tasks_link| are composed of several instances: a dispatcher, a collector, and
instance_0 to instance_n. The dispatcher rely on a load balancing function to select
the next instance to fire. Once this instance finishes it fires the collector.

Each instance of an |API_s4u_ExecTask| can be placed on a different host.
|API_s4u_Comm| activities are automatically created when an instance triggers
another instance on a different host. Each instance has its own parallelism degree
to scale horizontally on several cores.

To initiate the execution of a Dataflow, it is possible to some make
|API_s4u_Tasks_link| fire one or more activities without waiting for any token with the
:cpp:func:`s4u::Task::enqueue_firings() <simgrid::s4u::Task::enqueue_firings>`
function.

The parameters of Tasks can be redefined at runtime by attaching
callbacks to the
:cpp:func:`s4u::Task::on_this_start <simgrid::s4u::Task::on_this_start>`
and
:cpp:func:`s4u::Task::on_this_completion <simgrid::s4u::Task::on_this_completion>`
signals. The former is triggered by instances others than the dispatcher and the collector,
and the latter is triggered by the collector.



.. _s4u_mailbox:

Mailboxes
*********

Please also refer to the :ref:`API reference for s4u::Mailbox
<API_s4u_Mailbox>`.

===================
What are Mailboxes?
===================

|API_s4u_Mailboxes|_ are rendezvous points for network communications,
similar to URLs on which you could post and retrieve data. Actually,
the mailboxes are not involved in the communication once it starts,
but only to find the contact with which you want to communicate.

They are similar to many common things: The phone number, which allows
the caller to find the receiver. The Twitter hashtag, which helps
senders and receivers to find each other. In TCP, the pair
``{host name, host port}`` to which you can connect to find your peer.
In HTTP, URLs through which the clients can connect to the servers.
In ZeroMQ, the queues are used to match senders and receivers.

One big difference with most of these systems is that no actor is the
exclusive owner of a mailbox, neither in sending nor in receiving.
Many actors can send into and/or receive from the same mailbox.  TCP
socket ports for example are shared on the sender side but exclusive
on the receiver side (only one process can receive from a given socket
at a given point of time).

A big difference with TCP sockets or MPI communications is that
communications do not start right away after a
:cpp:func:`Mailbox::put() <simgrid::s4u::Mailbox::put>`, but wait
for the corresponding :cpp:func:`Mailbox::get() <simgrid::s4u::Mailbox::get>`.
You can change this by :ref:`declaring a receiving actor <s4u_receiving_actor>`.

A big difference with Twitter hashtags is that SimGrid does not
offer easy support to broadcast a given message to many
receivers. So that would be like a Twitter tag where each message
is consumed by the first receiver.

A big difference with the ZeroMQ queues is that you cannot filter
on the data you want to get from the mailbox. To model such settings
in SimGrid, you'd have one mailbox per potential topic, and subscribe
to each topic individually with a
:cpp:func:`get_async() <simgrid::s4u::Mailbox::get_async>` on each mailbox.
Then, use an :ref:`class ActivtySet <API_s4u_ActivitySet>` to get the first
message on any of the mailboxes you are subscribed to.

The mailboxes are not located on the network, and you can access
them without any latency. The network delays are only related to the
location of the sender and receiver once the match between them is
done on the mailbox. This is just like the phone number that you
can use locally, and the geographical distance only comes into play
once you start the communication by dialing this number.

=====================
How to use Mailboxes?
=====================

You can retrieve any existing mailbox from its name (which is a
unique string, just like a Twitter tag). This results in a
versatile tool that can be used to build many different
situations.

To model classical socket communications, use "hostname:port" as
mailbox names, and make sure that only one actor reads into a given
mailbox. This does not make it easy to build a perfectly realistic
model of the TCP sockets, but in most cases, this system is too
cumbersome for your simulations anyway. You probably want something
simpler, that turns out to be easy to build with the mailboxes.

Many SimGrid examples use a sort of yellow page system where the
mailbox names are the name of the service (such as "worker",
"master", or "reducer"). That way, you don't have to know where your
peer is located to contact it. You don't even need its name. Its
function is enough for that. This also gives you some sort of load
balancing for free if more than one actor pulls from the mailbox:
the first actor that can deal with the request will handle it.

=========================================
How are put() and get() requests matched?
=========================================

The matching algorithm simple: first come, first serve. When a new
send arrives, it matches the oldest enqueued receive. If no receive is
currently enqueued, then the incoming send is enqueued. As you can
see, the mailbox cannot contain both send and receive requests: all
enqueued requests must be of the same sort.

.. _s4u_receiving_actor:

===========================
Declaring a Receiving Actor
===========================

The last twist is that by default in the simulator, the data starts
to be exchanged only when both the sender and the receiver are
announced (it waits until both :cpp:func:`put() <simgrid::s4u::Mailbox::put()>`
and :cpp:func:`get() <simgrid::s4u::Mailbox::get()>` are posted).
In TCP, since you establish connections beforehand, the data starts to
flow as soon as the sender posts it, even if the receiver did not post
its :cpp:func:`put() <simgrid::s4u::Mailbox::put()>` yet.

To model this in SimGrid, you can declare a specific receiver to a
given mailbox (with the function
:cpp:func:`set_receiver() <simgrid::s4u::Mailbox::set_receiver()>`).
That way, any :cpp:func:`put() <simgrid::s4u::Mailbox::put()>`
posted to that mailbox will start as soon as possible, and the data
will already be there on the receiver host when the receiver actor
posts its :cpp:func:`get() <simgrid::s4u::Mailbox::get()>`

Note that being permanent receivers of a mailbox prevents actors to be
garbage-collected. If your simulation creates many short-lived actors
that are marked as permanent receiver, you should call
``mailbox->set_receiver(nullptr)`` by the end of the actors so that their
memory gets properly reclaimed. This call should be at the end of the
actor's function, not in an on_exit callback.

===============================
Communicating without Mailboxes
===============================

Sometimes you don't want to simulate communications between actors as
allowed by mailboxes, but you want to create a direct communication
between two arbitrary hosts. This can arise when you write a
high-level model of a centralized scheduler, or when you model direct
communications such as one-sided communications in MPI or remote
memory direct access in PGAS.

For that, :cpp:func:`Comm::sendto() <simgrid::s4u::Comm::sendto()>`
simulates a direct communication between the two specified hosts. No
mailbox is used, and there is no rendezvous between actors. You can
freely mix such direct communications and rendezvous-based
communications. Alternatively, :cpp:func:`Comm::sendto_init()
<simgrid::s4u::Comm::sendto_init()>` and
:cpp:func:`Comm::sendto_async() <simgrid::s4u::Comm::sendto_async()>`
create asynchronous direct communications.

.. _s4u_raii:

Memory Management
*****************

For sake of simplicity, we use `RAII
<https://en.wikipedia.org/wiki/Resource_Acquisition_Is_Initialization>`_
for many classes in S4U. This is an idiom where resources are automatically
managed through the context. Provided that you never manipulate
objects of type Foo directly but always FooPtr references (which are
defined as `boost::intrusive_ptr
<http://www.boost.org/doc/libs/1_61_0/libs/smart_ptr/intrusive_ptr.html>`_
<Foo>), you will never have to explicitly release the resource that
you use nor to free the memory of unused objects.
Here is a little example:

.. code-block:: cpp

   void myFunc()
   {
     simgrid::s4u::MutexPtr mutex = simgrid::s4u::Mutex::create(); // Too bad we cannot use `new`

     mutex->lock();   // use the mutex as a simple reference
     //  bla bla
     mutex->unlock();

   } // The mutex gets automatically freed because the only existing reference gets out of scope

Note that Mailboxes, Hosts, and Links are not handled through smart
pointers (yet?). This means that it is currently impossible to destroy a
mailbox or a link. You can still destroy a host (but probably
shouldn't), using :cpp:func:`simgrid::s4u::Host::destroy`.

API Reference
*************

.. _API_s4u_simulation_object:

==================
Simulation objects
==================

.. _API_s4u_Actor:

==============
⁣  class Actor
==============

.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::Actor

      .. doxygentypedef:: aid_t


   .. group-tab:: Python

      .. autoclass:: simgrid.Actor

Basic management
----------------

.. tabs::

   .. group-tab:: C++

      .. code:: C++

         #include <simgrid/s4u/Actor.hpp>

      .. doxygentypedef:: ActorPtr

   .. group-tab:: Python

      .. code:: Python

         from simgrid import Actor

   .. group-tab:: C

      .. code:: C

         #include <simgrid/actor.h>

      .. doxygentypedef:: sg_actor_t
      .. doxygentypedef:: const_sg_actor_t
      .. doxygenfunction:: sg_actor_ref
      .. doxygenfunction:: sg_actor_unref


Creating actors
---------------

See also :ref:`the relevant example <s4u_ex_actors_create>`.

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Actor::create(const std::string &name, s4u::Host *host, const std::function< void()> &code)
      .. doxygenfunction:: simgrid::s4u::Actor::create(const std::string &name, s4u::Host *host, F code)
      .. doxygenfunction:: simgrid::s4u::Actor::create(const std::string &name, s4u::Host *host, F code, Args... args)
      .. doxygenfunction:: simgrid::s4u::Actor::create(const std::string &name, s4u::Host *host, const std::string &function, std::vector< std::string > args)

      .. doxygenfunction:: simgrid::s4u::Actor::init(const std::string &name, s4u::Host *host)
      .. doxygenfunction:: simgrid::s4u::Actor::start(const std::function< void()> &code)
      .. doxygenfunction:: simgrid::s4u::Actor::set_stacksize

   .. group-tab:: Python

      .. automethod:: simgrid.Actor.create

   .. group-tab:: C

      .. doxygentypedef:: xbt_main_func_t

      .. doxygenfunction:: sg_actor_create(const char *name, sg_host_t host, xbt_main_func_t code, int argc, char *const *argv)
      .. doxygenfunction:: sg_actor_init(const char *name, sg_host_t host)
      .. doxygenfunction:: sg_actor_start(sg_actor_t actor, xbt_main_func_t code, int argc, char *const *argv)
      .. doxygenfunction:: sg_actor_start_voidp
      .. doxygenfunction:: sg_actor_set_stacksize

      .. doxygenfunction:: sg_actor_attach_pthread(const char *name, void *data, sg_host_t host)
      .. doxygenfunction:: sg_actor_detach()

      See also :ref:`s4u_ex_actor_attach` for an example of use of ``sg_actor_attach_pthread()`` and ``sg_actor_detach()``.

Retrieving actors
-----------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Actor::by_pid(aid_t pid)
      .. doxygenfunction:: simgrid::s4u::Actor::self()

   .. group-tab:: Python

      .. automethod:: simgrid.Actor.by_pid
      .. automethod:: simgrid.Actor.self

   .. group-tab:: C

      .. doxygenfunction:: sg_actor_by_pid(aid_t pid)
      .. doxygenfunction:: sg_actor_self()
      .. doxygenfunction:: sg_actor_list()

Querying info
-------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Actor::get_cname
      .. doxygenfunction:: simgrid::s4u::Actor::get_name
      .. doxygenfunction:: simgrid::s4u::Actor::get_pid
      .. doxygenfunction:: simgrid::s4u::Actor::get_ppid
      .. doxygenfunction:: simgrid::s4u::Actor::get_properties() const
      .. doxygenfunction:: simgrid::s4u::Actor::get_property(const std::string &key) const
      .. doxygenfunction:: simgrid::s4u::Actor::set_property(const std::string &key, const std::string &value)

      .. doxygenfunction:: simgrid::s4u::Actor::get_host
      .. doxygenfunction:: simgrid::s4u::Actor::set_host

      .. doxygenfunction:: simgrid::s4u::Actor::get_refcount
      .. doxygenfunction:: simgrid::s4u::Actor::get_impl

   .. group-tab:: Python

      .. autoattribute:: simgrid.Actor.name
      .. autoattribute:: simgrid.Actor.host
      .. autoattribute:: simgrid.Actor.pid
      .. autoattribute:: simgrid.Actor.ppid

   .. group-tab:: C

      .. doxygenfunction:: sg_actor_get_name(const_sg_actor_t actor)
      .. doxygenfunction:: sg_actor_get_pid(const_sg_actor_t actor)
      .. doxygenfunction:: sg_actor_get_ppid(const_sg_actor_t actor)
      .. doxygenfunction:: sg_actor_get_property_names(const_sg_actor_t actor, int* size)
      .. doxygenfunction:: sg_actor_get_property_value(const_sg_actor_t actor, const char *name)

      .. doxygenfunction:: sg_actor_get_host(const_sg_actor_t actor)
      .. doxygenfunction:: sg_actor_set_host(sg_actor_t actor, sg_host_t host)

      .. doxygenfunction:: sg_actor_get_data(const_sg_actor_t actor)
      .. doxygenfunction:: sg_actor_set_data(sg_actor_t actor, void *userdata)

Suspending and resuming actors
------------------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Actor::suspend()
      .. doxygenfunction:: simgrid::s4u::Actor::resume()
      .. doxygenfunction:: simgrid::s4u::Actor::is_suspended

   .. group-tab:: Python

      .. automethod:: simgrid.Actor.resume
      .. automethod:: simgrid.Actor.suspend
      .. automethod:: simgrid.Actor.is_suspended

   .. group-tab:: C

      .. doxygenfunction:: sg_actor_suspend(sg_actor_t actor)
      .. doxygenfunction:: sg_actor_resume(sg_actor_t actor)
      .. doxygenfunction:: sg_actor_is_suspended(const_sg_actor_t actor)

Specifying when actors should terminate
---------------------------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Actor::kill()
      .. doxygenfunction:: simgrid::s4u::Actor::kill_all()
      .. doxygenfunction:: simgrid::s4u::Actor::set_kill_time(double time)
      .. doxygenfunction:: simgrid::s4u::Actor::get_kill_time

      .. doxygenfunction:: simgrid::s4u::Actor::restart()
      .. doxygenfunction:: simgrid::s4u::Actor::daemonize()
      .. doxygenfunction:: simgrid::s4u::Actor::is_daemon

   .. group-tab:: Python

      .. automethod:: simgrid.Actor.kill
      .. automethod:: simgrid.Actor.kill_all

      .. automethod:: simgrid.Actor.daemonize
      .. automethod:: simgrid.Actor.is_daemon

   .. group-tab:: C

      .. doxygenfunction:: sg_actor_kill(sg_actor_t actor)
      .. doxygenfunction:: sg_actor_kill_all()
      .. doxygenfunction:: sg_actor_set_kill_time(sg_actor_t actor, double kill_time)

      .. doxygenfunction:: sg_actor_restart(sg_actor_t actor)
      .. doxygenfunction:: sg_actor_daemonize(sg_actor_t actor)
      .. doxygenfunction:: sg_actor_is_daemon

   .. group-tab:: java

      .. js::method:: void org.simgrid.s4u.Actor.kill()

         Ask the actor to die.

         Any blocking activity will be canceled, and it will be rescheduled to free its memory.<br>
         Being killed is not something that actors can defer or avoid.

      .. js::method:: void org.simgrid.s4u.Actor.kill_all()

         Kill all actors (but the issuer). Being killed is not something that actors can delay or avoid.

      .. js::method:: void org.simgrid.s4u.Actor.set_kill_time(double time)

         Sets the time at which that actor should be killed.

      .. js::method:: double org.simgrid.s4u.Actor.set_kill_time()

         Retrieves the time at which that actor will be killed (or -1 if not set)

      .. js:method:: Actor org.simgrid.s4u.Actor.daemonize()

         Change this actor into a daemon. Daemons are killed as soon as the last regular actor disappears. If another regular
         actor gets restarted later on by a timer or when its host reboots, the daemons do not get restarted.

      .. js::method:: boolean org.simgrid.s4u.Actor.is_daemon()

         Returns whether or not this actor has been daemonized or not.

      .. js::method:: Actor org.simgrid.s4u.Actor.restart()

         Kill that actor and restart it from start.

.. _API_s4u_Actor_end:

Reacting to the end of actors
-----------------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Actor::on_exit
      .. doxygenfunction:: simgrid::s4u::Actor::join() const
      .. doxygenfunction:: simgrid::s4u::Actor::join(double timeout) const
      .. doxygenfunction:: simgrid::s4u::Actor::set_auto_restart(bool autorestart)
      .. doxygenfunction:: simgrid::s4u::Actor::get_restart_count

   .. group-tab:: Python

      .. automethod:: simgrid.Actor.join

   .. group-tab:: C

      .. doxygenfunction:: sg_actor_on_exit
      .. doxygenfunction:: sg_actor_join(const_sg_actor_t actor, double timeout)
      .. doxygenfunction:: sg_actor_set_auto_restart(sg_actor_t actor, int auto_restart)

Signals
-------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Actor::on_creation_cb
      .. doxygenfunction:: simgrid::s4u::Actor::on_host_change_cb
      .. doxygenfunction:: simgrid::s4u::Actor::on_sleep_cb
      .. doxygenfunction:: simgrid::s4u::Actor::on_suspend_cb
      .. doxygenfunction:: simgrid::s4u::Actor::on_resume_cb
      .. doxygenfunction:: simgrid::s4u::Actor::on_wake_up_cb
      .. doxygenfunction:: simgrid::s4u::Actor::on_termination_cb
      .. doxygenfunction:: simgrid::s4u::Actor::on_destruction_cb
      .. doxygenfunction:: simgrid::s4u::Actor::on_this_host_change_cb
      .. doxygenfunction:: simgrid::s4u::Actor::on_this_sleep_cb
      .. doxygenfunction:: simgrid::s4u::Actor::on_this_suspend_cb
      .. doxygenfunction:: simgrid::s4u::Actor::on_this_resume_cb
      .. doxygenfunction:: simgrid::s4u::Actor::on_this_wake_up_cb
      .. doxygenfunction:: simgrid::s4u::Actor::on_this_termination_cb
      .. doxygenfunction:: simgrid::s4u::Actor::on_this_destruction_cb

.. _API_s4u_this_actor:

====================
⁣  The current actor
====================

These functions can be used in your user code to interact with the actor
currently running (the one retrieved with :cpp:func:`simgrid::s4u::Actor::self`).
Using these functions can greatly improve the code readability.

Querying info
-------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::this_actor::get_cname()
      .. doxygenfunction:: simgrid::s4u::this_actor::get_name()
      .. doxygenfunction:: simgrid::s4u::this_actor::get_pid()
      .. doxygenfunction:: simgrid::s4u::this_actor::get_ppid()
      .. doxygenfunction:: simgrid::s4u::this_actor::is_maestro()

      .. doxygenfunction:: simgrid::s4u::this_actor::get_host()
      .. doxygenfunction:: simgrid::s4u::this_actor::set_host(Host *new_host)

   .. group-tab:: Python

      .. autofunction:: simgrid.this_actor.get_host
      .. autofunction:: simgrid.this_actor.set_host
      .. autofunction:: simgrid.this_actor.get_name

      .. autofunction:: simgrid.this_actor.get_pid
      .. autofunction:: simgrid.this_actor.get_ppid

   .. group-tab:: C

      .. doxygenfunction:: sg_actor_self_get_data()
      .. doxygenfunction:: sg_actor_self_set_data(void *data)
      .. doxygenfunction:: sg_actor_self_get_name()
      .. doxygenfunction:: sg_actor_self_get_pid()
      .. doxygenfunction:: sg_actor_self_get_ppid()
      .. doxygenfunction:: sg_host_self()
      .. doxygenfunction:: sg_host_self_get_name()

Suspending and resuming
-----------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::this_actor::suspend()
      .. doxygenfunction:: simgrid::s4u::this_actor::yield()

   .. group-tab:: Python

      .. autofunction:: simgrid.this_actor.suspend
      .. autofunction:: simgrid.this_actor.yield_

   .. group-tab:: C

      .. doxygenfunction:: sg_actor_yield()

Logging messages
----------------

.. tabs::

   .. group-tab:: C++

      Please refer to :ref:`the relevant documentation <logging_prog>`.

   .. group-tab:: Python

       .. autofunction:: simgrid.this_actor.debug
       .. autofunction:: simgrid.this_actor.info
       .. autofunction:: simgrid.this_actor.warning
       .. autofunction:: simgrid.this_actor.error

Sleeping
--------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::this_actor::sleep_for(double duration)
      .. doxygenfunction:: simgrid::s4u::this_actor::sleep_for(std::chrono::duration< Rep, Period > duration)
      .. doxygenfunction:: simgrid::s4u::this_actor::sleep_until(const SimulationTimePoint< Duration > &wakeup_time)
      .. doxygenfunction:: simgrid::s4u::this_actor::sleep_until(double wakeup_time)

   .. group-tab:: Python

      .. autofunction:: simgrid.this_actor.sleep_for
      .. autofunction:: simgrid.this_actor.sleep_until

   .. group-tab:: C

      .. doxygenfunction:: sg_actor_sleep_for(double duration)

Simulating executions
---------------------

Simulate the execution of some code on this actor. You can either simulate
parallel or sequential code and you can either block upon the termination of
the execution, or start an asynchronous activity.

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::this_actor::exec_async
      .. doxygenfunction:: simgrid::s4u::this_actor::exec_init(const std::vector< s4u::Host * > &hosts, const std::vector< double > &flops_amounts, const std::vector< double > &bytes_amounts)
      .. doxygenfunction:: simgrid::s4u::this_actor::exec_init(double flops_amounts)
      .. doxygenfunction:: simgrid::s4u::this_actor::execute(double flop)
      .. doxygenfunction:: simgrid::s4u::this_actor::execute(double flop, double priority)
      .. doxygenfunction:: simgrid::s4u::this_actor::parallel_execute(const std::vector< s4u::Host * > &hosts, const std::vector< double > &flops_amounts, const std::vector< double > &bytes_amounts)
      .. doxygenfunction:: simgrid::s4u::this_actor::thread_execute

   .. group-tab:: Python

      .. autofunction:: simgrid.this_actor.exec_async
      .. autofunction:: simgrid.this_actor.exec_init
      .. autofunction:: simgrid.this_actor.execute

   .. group-tab:: C

      .. doxygenfunction:: sg_actor_execute(double flops)
      .. doxygenfunction:: sg_actor_execute_with_priority(double flops, double priority)
      .. doxygenfunction:: sg_actor_exec_init(double computation_amount)
      .. doxygenfunction:: sg_actor_exec_async(double computation_amount)
      .. doxygenfunction:: sg_actor_parallel_exec_init(int host_nb, const sg_host_t* host_list, double* flops_amount, double* bytes_amount);

Exiting
-------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::this_actor::exit()
      .. doxygenfunction:: simgrid::s4u::this_actor::on_exit(const std::function< void(bool)> &fun)

   .. group-tab:: Python

      .. autofunction:: simgrid.this_actor.exit
      .. autofunction:: simgrid.this_actor.on_exit

   .. group-tab:: c

      See also :cpp:func:`sg_actor_on_exit`.

      .. doxygenfunction:: sg_actor_exit

.. _API_s4u_Engine:

====================
⁣  Simulation Engine
====================

.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::Engine

   .. group-tab:: Python

      .. autoclass:: simgrid.Engine

Engin initialization
--------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Engine::Engine(int *argc, char **argv)
      .. doxygenfunction:: simgrid::s4u::Engine::is_initialized()
      .. doxygenfunction:: simgrid::s4u::Engine::get_instance()

   .. group-tab:: Python

       .. automethod:: simgrid.Engine.__init__
       .. autoattribute:: simgrid.Engine.instance

   .. group-tab:: C

      .. doxygenfunction:: simgrid_init

Simulation setup
----------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Engine::set_config(const std::string &str)
      .. doxygenfunction:: simgrid::s4u::Engine::set_config(const std::string &name, bool value)
      .. doxygenfunction:: simgrid::s4u::Engine::set_config(const std::string &name, double value)
      .. doxygenfunction:: simgrid::s4u::Engine::set_config(const std::string &name, int value)
      .. doxygenfunction:: simgrid::s4u::Engine::set_config(const std::string &name, const std::string &value)

      .. doxygenfunction:: simgrid::s4u::Engine::load_deployment
      .. doxygenfunction:: simgrid::s4u::Engine::load_platform
      .. doxygenfunction:: simgrid::s4u::Engine::flatify_platform
      .. doxygenfunction:: simgrid::s4u::Engine::register_actor(const std::string &name)
      .. doxygenfunction:: simgrid::s4u::Engine::register_actor(const std::string &name, F code)
      .. doxygenfunction:: simgrid::s4u::Engine::register_default(const std::function< void(int, char **)> &code)
      .. doxygenfunction:: simgrid::s4u::Engine::register_default(const kernel::actor::ActorCodeFactory &factory)

      .. doxygenfunction:: simgrid::s4u::Engine::register_function(const std::string &name, const std::function< void(int, char **)> &code)
      .. doxygenfunction:: simgrid::s4u::Engine::register_function(const std::string &name, const std::function< void(std::vector< std::string >)> &code)
      .. doxygenfunction:: simgrid::s4u::Engine::register_function(const std::string &name, const kernel::actor::ActorCodeFactory &factory)

   .. group-tab:: Python

       .. automethod:: simgrid.Engine.load_deployment
       .. automethod:: simgrid.Engine.load_platform
       .. automethod:: simgrid.Engine.register_actor

   .. group-tab:: C

      .. doxygenfunction:: simgrid_load_deployment
      .. doxygenfunction:: simgrid_load_platform
      .. doxygenfunction:: simgrid_register_default
      .. doxygenfunction:: simgrid_register_function


Run the simulation
------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Engine::get_clock()
      .. doxygenfunction:: simgrid::s4u::Engine::run
      .. doxygenfunction:: simgrid::s4u::Engine::run_until

   .. group-tab:: Python

      .. autoattribute:: simgrid.Engine.clock
      .. automethod:: simgrid.Engine.run
      .. automethod:: simgrid.Engine.run_until

   .. group-tab:: C

      .. doxygenfunction:: simgrid_get_clock
      .. doxygenfunction:: simgrid_run
      .. doxygenfunction:: simgrid_run_until

Retrieving actors
-----------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Engine::get_actor_count
      .. doxygenfunction:: simgrid::s4u::Engine::get_all_actors
      .. doxygenfunction:: simgrid::s4u::Engine::get_filtered_actors

   .. group-tab:: Python

      .. autoattribute:: simgrid.Engine.all_actors

   .. group-tab:: C

      .. doxygenfunction:: sg_actor_count()

Retrieving hosts
----------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Engine::get_all_hosts
      .. doxygenfunction:: simgrid::s4u::Engine::get_host_count
      .. doxygenfunction:: simgrid::s4u::Engine::get_filtered_hosts
      .. doxygenfunction:: simgrid::s4u::Engine::host_by_name
      .. doxygenfunction:: simgrid::s4u::Engine::host_by_name_or_null

   .. group-tab:: Python

      .. autoattribute:: simgrid.Engine.all_hosts
      .. automethod:: simgrid.Engine.host_by_name

   .. group-tab:: C

      See also :cpp:func:`sg_host_list` and :cpp:func:`sg_host_count`.

Retrieving links
----------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Engine::get_all_links
      .. doxygenfunction:: simgrid::s4u::Engine::get_link_count
      .. doxygenfunction:: simgrid::s4u::Engine::get_filtered_links
      .. doxygenfunction:: simgrid::s4u::Engine::link_by_name
      .. doxygenfunction:: simgrid::s4u::Engine::link_by_name_or_null

   .. group-tab:: Python

      .. autoattribute:: simgrid.Engine.all_links

Interacting with the routing
----------------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Engine::get_all_netpoints
      .. doxygenfunction:: simgrid::s4u::Engine::get_filtered_netzones
      .. doxygenfunction:: simgrid::s4u::Engine::get_netzone_root
      .. doxygenfunction:: simgrid::s4u::Engine::netpoint_by_name_or_null
      .. doxygenfunction:: simgrid::s4u::Engine::netzone_by_name_or_null

   .. group-tab:: Python

      .. autoattribute:: simgrid.Engine.all_netpoints
      .. autoattribute:: simgrid.Engine.netzone_root
      .. automethod:: simgrid.Engine.netpoint_by_name
      .. automethod:: simgrid.Engine.netzone_by_name

Signals
-------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Engine::on_platform_created_cb
      .. doxygenfunction:: simgrid::s4u::Engine::on_platform_creation_cb
      .. doxygenfunction:: simgrid::s4u::Engine::on_simulation_start_cb
      .. doxygenfunction:: simgrid::s4u::Engine::on_simulation_end_cb
      .. doxygenfunction:: simgrid::s4u::Engine::on_time_advance_cb
      .. doxygenfunction:: simgrid::s4u::Engine::on_deadlock_cb

.. _API_s4u_Mailbox:

================
⁣  class Mailbox
================

.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::Mailbox

   .. group-tab:: Python

      .. autoclass:: simgrid.Mailbox

Please also refer to the :ref:`full doc on s4u::Mailbox <s4u_mailbox>`.

Basic management
----------------

.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/Mailbox.hpp>

      Note that there is no MailboxPtr type and that you cannot use the RAII
      idiom on mailboxes because they are internal objects to the simulation
      engine. Once created, there is no way to destroy a mailbox before the end
      of the simulation.

      .. doxygenfunction:: simgrid::s4u::Mailbox::by_name(const std::string &name)

   .. group-tab:: Python

      .. code-block:: C++

         #include <simgrid/mailbox.h>

      .. automethod:: simgrid.Mailbox.by_name

   .. group-tab:: C

      .. code-block:: C

         #include <simgrid/s4u/mailbox.h>

      .. doxygentypedef:: sg_mailbox_t
      .. doxygentypedef:: const_sg_mailbox_t

      .. doxygenfunction:: sg_mailbox_by_name(const char *alias)

Querying info
-------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Mailbox::get_cname
      .. doxygenfunction:: simgrid::s4u::Mailbox::get_name

   .. group-tab:: Python

      .. autoattribute:: simgrid.Mailbox.name

   .. group-tab:: C

      .. doxygenfunction:: sg_mailbox_get_name(const_sg_mailbox_t mailbox)

Sending data
------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Mailbox::put(void *payload, uint64_t simulated_size_in_bytes)
      .. doxygenfunction:: simgrid::s4u::Mailbox::put(void *payload, uint64_t simulated_size_in_bytes, double timeout)
      .. doxygenfunction:: simgrid::s4u::Mailbox::put_async(void *data, uint64_t simulated_size_in_bytes)
      .. doxygenfunction:: simgrid::s4u::Mailbox::put_init()
      .. doxygenfunction:: simgrid::s4u::Mailbox::put_init(void *data, uint64_t simulated_size_in_bytes)

   .. group-tab:: Python

      .. automethod:: simgrid.Mailbox.put
      .. automethod:: simgrid.Mailbox.put_async
      .. automethod:: simgrid.Mailbox.put_init

   .. group-tab:: C

      .. doxygenfunction:: sg_mailbox_put(sg_mailbox_t mailbox, void *payload, long simulated_size_in_bytes)
      .. doxygenfunction:: sg_mailbox_put_init(sg_mailbox_t mailbox, void *payload, long simulated_size_in_bytes)
      .. doxygenfunction:: sg_mailbox_put_async(sg_mailbox_t mailbox, void *payload, long simulated_size_in_bytes)


Receiving data
--------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Mailbox::empty
      .. doxygenfunction:: simgrid::s4u::Mailbox::front
      .. doxygenfunction:: simgrid::s4u::Mailbox::get()
      .. doxygenfunction:: simgrid::s4u::Mailbox::get(double timeout)
      .. doxygenfunction:: simgrid::s4u::Mailbox::get_async(T **data)
      .. doxygenfunction:: simgrid::s4u::Mailbox::get_init()
      .. doxygenfunction:: simgrid::s4u::Mailbox::iprobe
      .. doxygenfunction:: simgrid::s4u::Mailbox::listen
      .. doxygenfunction:: simgrid::s4u::Mailbox::ready

   .. group-tab:: Python

       .. automethod:: simgrid.Mailbox.get
       .. automethod:: simgrid.Mailbox.get_async
       .. autoattribute:: simgrid.Mailbox.ready

   .. group-tab:: C

      .. doxygenfunction:: sg_mailbox_get(sg_mailbox_t mailbox)
      .. doxygenfunction:: sg_mailbox_get_async(sg_mailbox_t mailbox, void **data)
      .. doxygenfunction:: sg_mailbox_listen(const char *alias)

Receiving actor
---------------

See :ref:`s4u_receiving_actor`.

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Mailbox::get_receiver
      .. doxygenfunction:: simgrid::s4u::Mailbox::set_receiver(ActorPtr actor)

   .. group-tab:: C

      .. doxygenfunction:: sg_mailbox_set_receiver(const char *alias)

.. _API_s4u_Resource:

=========
Resources
=========

.. _API_s4u_Disk:

=============
⁣  class Disk
=============

.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::Disk

   .. group-tab:: Python

      .. autoclass:: simgrid.Disk

   .. group-tab:: C

      .. doxygentypedef:: sg_disk_t
      .. doxygentypedef:: const_sg_disk_t

Basic management
----------------

.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/Disk.hpp>

      Note that there is no DiskPtr type and that you cannot use the RAII
      idiom on disks because SimGrid does not allow (yet) to create nor
      destroy resources once the simulation is started.

      .. doxygenfunction:: simgrid::s4u::Disk::seal()

   .. group-tab:: Python

      .. code:: Python

         from simgrid import Disk

      .. automethod:: simgrid.Disk.seal


Querying info
-------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Disk::get_cname() const
      .. doxygenfunction:: simgrid::s4u::Disk::get_host() const
      .. doxygenfunction:: simgrid::s4u::Disk::get_name() const


   .. group-tab:: Python

      .. autoattribute:: simgrid.Disk.name


Performance
-----------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Disk::get_read_bandwidth() const
      .. doxygenfunction:: simgrid::s4u::Disk::get_write_bandwidth() const

   .. group-tab:: Python

      .. autoattribute:: simgrid.Disk.read_bandwidth
      .. autoattribute:: simgrid.Disk.write_bandwidth

   .. group-tab:: C

      .. doxygenfunction:: sg_disk_read_bandwidth(const_sg_disk_t disk)
      .. doxygenfunction:: sg_disk_write_bandwidth(const_sg_disk_t disk)

Model policy
------------

.. tabs::

   .. group-tab:: C++

      .. doxygenenum:: simgrid::s4u::Disk::SharingPolicy

      .. doxygenfunction:: simgrid::s4u::Disk::get_sharing_policy
      .. doxygenfunction:: simgrid::s4u::Disk::set_sharing_policy

      .. doxygenfunction:: simgrid::s4u::Disk::get_concurrency_limit() const
      .. doxygenfunction:: simgrid::s4u::Disk::set_concurrency_limit(int limit)

   .. group-tab:: Python

      .. autoattribute:: simgrid.Disk.concurrency_limit
      .. automethod:: simgrid.Disk.set_sharing_policy
      .. autoclass:: simgrid.Disk.SharingPolicy

   .. group-tab:: C

User data and properties
------------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Disk::get_properties() const
      .. doxygenfunction:: simgrid::s4u::Disk::get_property(const std::string &key) const
      .. doxygenfunction:: simgrid::s4u::Disk::set_property(const std::string &key, const std::string &value)

   .. group-tab:: C

      .. doxygenfunction:: sg_disk_get_data(const_sg_disk_t disk)
      .. doxygenfunction:: sg_disk_set_data(sg_disk_t disk, void *data)

I/O operations
--------------

.. tabs::

   .. group-tab:: C++

      .. doxygenenum:: simgrid::s4u::Disk::Operation
      .. doxygenfunction:: simgrid::s4u::Disk::io_init(sg_size_t size, s4u::Io::OpType type) const
      .. doxygenfunction:: simgrid::s4u::Disk::read(sg_size_t size) const
      .. doxygenfunction:: simgrid::s4u::Disk::read_async(sg_size_t size) const
      .. doxygenfunction:: simgrid::s4u::Disk::write(sg_size_t size) const
      .. doxygenfunction:: simgrid::s4u::Disk::write_async(sg_size_t size) const

   .. group-tab:: Python

      .. autoclass:: simgrid.Disk.Operation

      .. automethod:: simgrid.Disk.read
      .. automethod:: simgrid.Disk.read_async
      .. automethod:: simgrid.Disk.write
      .. automethod:: simgrid.Disk.write_async

Signals
-------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Disk::on_creation_cb
      .. doxygenfunction:: simgrid::s4u::Disk::on_onoff_cb
      .. doxygenfunction:: simgrid::s4u::Disk::on_destruction_cb
      .. doxygenfunction:: simgrid::s4u::Disk::on_read_bandwidth_change_cb
      .. doxygenfunction:: simgrid::s4u::Disk::on_write_bandwidth_change_cb
      .. doxygenfunction:: simgrid::s4u::Disk::on_this_onoff_cb
      .. doxygenfunction:: simgrid::s4u::Disk::on_this_destruction_cb
      .. doxygenfunction:: simgrid::s4u::Disk::on_this_read_bandwidth_change_cb
      .. doxygenfunction:: simgrid::s4u::Disk::on_this_write_bandwidth_change_cb
      .. doxygenfunction:: simgrid::s4u::Disk::on_io_state_change_cb
.. _API_s4u_Host:

=============
⁣  class Host
=============

.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::Host

   .. group-tab:: Python

      .. autoclass:: simgrid.Host

Basic management
----------------

.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/Host.hpp>

      Note that there is no HostPtr type, and that you cannot use the RAII
      idiom on hosts because SimGrid does not allow (yet) to create nor
      destroy resources once the simulation is started.

      .. doxygenfunction:: simgrid::s4u::Host::destroy()
      .. doxygenfunction:: simgrid::s4u::Host::seal()

   .. group-tab:: Python

      .. code:: Python

         from simgrid import Host

      .. automethod:: simgrid.Host.seal

   .. group-tab:: C

      .. code:: C

         #include <simgrid/host.h>

      .. doxygentypedef:: sg_host_t
      .. cpp:type:: const s4u_Host* const_sg_host_t

         Pointer to a constant host object.

Retrieving hosts
----------------

.. tabs::

   .. group-tab:: C++

      See also :cpp:func:`simgrid::s4u::Engine::get_all_hosts`.

      .. doxygenfunction:: simgrid::s4u::Host::by_name(const std::string &name)
      .. doxygenfunction:: simgrid::s4u::Host::by_name_or_null(const std::string &name)
      .. doxygenfunction:: simgrid::s4u::Host::current()

   .. group-tab:: Python

      See also :py:attr:`simgrid.Engine.all_hosts`.

      .. automethod:: simgrid.Host.by_name
      .. automethod:: simgrid.Host.by_name_or_null
      .. automethod:: simgrid.Host.current

   .. group-tab:: C

      .. doxygenfunction:: sg_host_by_name(const char *name)
      .. doxygenfunction:: sg_host_count()
      .. doxygenfunction:: sg_host_list()

Modifying characteristics
-------------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Host::set_core_count(int core_count)
      .. doxygenfunction:: simgrid::s4u::Host::set_coordinates(const std::string& coords)
      .. doxygenfunction:: simgrid::s4u::Host::set_sharing_policy
      .. doxygenfunction:: simgrid::s4u::Host::set_concurrency_limit(int limit)

   .. group-tab:: Python

      .. autoattribute:: simgrid.Host.core_count
         :noindex:
      .. automethod:: simgrid.Host.set_coordinates
      .. automethod:: simgrid.Host.set_sharing_policy
      .. autoattribute:: simgrid.Host.concurrency_limit

Querying info
-------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Host::get_cname() const
      .. doxygenfunction:: simgrid::s4u::Host::get_core_count() const
      .. doxygenfunction:: simgrid::s4u::Host::get_name() const
      .. doxygenfunction:: simgrid::s4u::Host::get_available_speed() const
      .. doxygenfunction:: simgrid::s4u::Host::get_load() const
      .. doxygenfunction:: simgrid::s4u::Host::get_speed() const
      .. doxygenfunction:: simgrid::s4u::Host::get_concurrency_limit() const

   .. group-tab:: Python

      .. autoattribute:: simgrid.Host.name
      .. autoattribute:: simgrid.Host.core_count
      .. autoattribute:: simgrid.Host.load
      .. autoattribute:: simgrid.Host.speed
      .. autoattribute:: simgrid.Host.available_speed

   .. group-tab:: C

      .. doxygenfunction:: sg_host_core_count(const_sg_host_t host)
      .. doxygenfunction:: sg_host_get_name(const_sg_host_t host)
      .. doxygenfunction:: sg_host_get_load(const_sg_host_t host)
      .. doxygenfunction:: sg_host_get_speed(const_sg_host_t host)

User data and properties
------------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Host::get_properties() const
      .. doxygenfunction:: simgrid::s4u::Host::get_property(const std::string &key) const
      .. doxygenfunction:: simgrid::s4u::Host::set_properties(const std::unordered_map< std::string, std::string > &properties)
      .. doxygenfunction:: simgrid::s4u::Host::set_property(const std::string &key, const std::string &value)

   .. group-tab:: Python

      .. automethod:: simgrid.Host.get_properties
      .. automethod:: simgrid.Host.get_property
      .. automethod:: simgrid.Host.set_properties
      .. automethod:: simgrid.Host.set_property

   .. group-tab:: C

      .. doxygenfunction:: sg_host_set_property_value(sg_host_t host, const char *name, const char *value)
      .. doxygenfunction:: sg_host_get_property_names(const_sg_host_t host, int* size)
      .. doxygenfunction:: sg_host_get_property_value(const_sg_host_t host, const char *name)
      .. doxygenfunction:: sg_host_extension_create(void(*deleter)(void *))
      .. doxygenfunction:: sg_host_extension_get(const_sg_host_t host, size_t rank)

Retrieving components
---------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Host::get_actor_count() const
      .. doxygenfunction:: simgrid::s4u::Host::get_all_actors() const
      .. doxygenfunction:: simgrid::s4u::Host::get_disks() const
      .. doxygenfunction:: simgrid::s4u::Host::get_disk_by_name(const std::string& name) const

   .. group-tab:: Python

      .. autoattribute:: simgrid.Host.all_actors
      .. autoattribute:: simgrid.Host.actor_count
      .. automethod:: simgrid.Host.get_disks
      .. automethod:: simgrid.Host.get_disk_by_name

   .. group-tab:: C

      .. doxygenfunction:: sg_host_get_actors(const_sg_host_t host, int* size)

On/Off
------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Host::is_on() const
      .. doxygenfunction:: simgrid::s4u::Host::turn_off()
      .. doxygenfunction:: simgrid::s4u::Host::turn_on()

   .. group-tab:: Python

      .. autoattribute:: simgrid.Host.is_on

   .. group-tab:: C

      .. doxygenfunction:: sg_host_is_on(const_sg_host_t host)
      .. doxygenfunction:: sg_host_turn_off(sg_host_t host)
      .. doxygenfunction:: sg_host_turn_on(sg_host_t host)

.. _API_s4u_Host_dvfs:

DVFS
----

See also the :ref:`relevant examples <s4u_ex_dvfs>`.

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Host::get_pstate() const
      .. doxygenfunction:: simgrid::s4u::Host::get_pstate_count() const
      .. doxygenfunction:: simgrid::s4u::Host::get_pstate_speed(unsigned long pstate_index) const
      .. doxygenfunction:: simgrid::s4u::Host::set_pstate(unsigned long pstate_index)

   .. group-tab:: Python

      .. autoattribute:: simgrid.Host.pstate
      .. autoattribute:: simgrid.Host.pstate_count
      .. automethod:: simgrid.Host.pstate_speed

   .. group-tab:: C

      .. doxygenfunction:: sg_host_get_available_speed(const_sg_host_t host)
      .. doxygenfunction:: sg_host_get_nb_pstates(const_sg_host_t host)
      .. doxygenfunction:: sg_host_get_pstate(const_sg_host_t host)
      .. doxygenfunction:: sg_host_get_pstate_speed(const_sg_host_t host, unsigned long pstate_index)
      .. doxygenfunction:: sg_host_set_pstate(sg_host_t host, unsigned long pstate)

Dynamic profiles
----------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Host::set_speed_profile(kernel::profile::Profile *p)
      .. doxygenfunction:: simgrid::s4u::Host::set_state_profile(kernel::profile::Profile *p)

   .. group-tab:: Python

      .. automethod:: simgrid.Host.set_speed_profile
      .. automethod:: simgrid.Host.set_state_profile

Execution
---------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Host::exec_async
      .. doxygenfunction:: simgrid::s4u::Host::execute(double flops) const
      .. doxygenfunction:: simgrid::s4u::Host::execute(double flops, double priority) const

Disks
-----

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Host::add_disk(const std::string &name, const std::string &read_bandwidth, const std::string &write_bandwidth)
      .. doxygenfunction:: simgrid::s4u::Host::add_disk(const std::string &name, double read_bandwidth, double write_bandwidth)
      .. doxygenfunction:: simgrid::s4u::Host::remove_disk(const std::string &disk_name)

   .. group-tab:: Python

      .. automethod:: simgrid.Host.add_disk

Platform and routing
--------------------

You can also start direct communications between two arbitrary hosts
using :cpp:func:`Comm::sendto() <simgrid::s4u::Comm::sendto()>`.

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Host::get_englobing_zone() const
      .. doxygenfunction:: simgrid::s4u::Host::get_netpoint() const
      .. doxygenfunction:: simgrid::s4u::Host::route_to(const Host *dest, std::vector< Link * > &links, double *latency) const
      .. doxygenfunction:: simgrid::s4u::Host::route_to(const Host *dest, std::vector< kernel::resource::StandardLinkImpl * > &links, double *latency) const

   .. group-tab:: Python

      .. autoattribute:: simgrid.Host.netpoint

      .. automethod:: simgrid.Host.route_to

   .. group-tab:: C

      .. doxygenfunction:: sg_host_get_route_links(const_sg_host_t from, const_sg_host_t to, int* size)
      .. doxygenfunction:: sg_host_get_route_bandwidth(const_sg_host_t from, const_sg_host_t to)
      .. doxygenfunction:: sg_host_get_route_latency(const_sg_host_t from, const_sg_host_t to)
      .. doxygenfunction:: sg_host_sendto(sg_host_t from, sg_host_t to, double byte_amount)

Signals
-------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Host::on_creation_cb
      .. doxygenfunction:: simgrid::s4u::Host::on_onoff_cb
      .. doxygenfunction:: simgrid::s4u::Host::on_destruction_cb
      .. doxygenfunction:: simgrid::s4u::Host::on_speed_change_cb
      .. doxygenfunction:: simgrid::s4u::Host::on_this_onoff_cb
      .. doxygenfunction:: simgrid::s4u::Host::on_this_destruction_cb
      .. doxygenfunction:: simgrid::s4u::Host::on_this_speed_change_cb
      .. doxygenfunction:: simgrid::s4u::Host::on_exec_state_change_cb

.. _API_s4u_Link:

=============
⁣  class Link
=============

.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::Link
      .. doxygenclass:: simgrid::s4u::SplitDuplexLink
      .. doxygenclass:: simgrid::s4u::LinkInRoute


   .. group-tab:: Python

      .. autoclass:: simgrid.Link

Basic management
----------------

.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/Link.hpp>

      Note that there is no LinkPtr type and that you cannot use the RAII
      idiom on hosts because SimGrid does not allow (yet) to create nor
      destroy resources once the simulation is started.

      .. doxygenfunction:: simgrid::s4u::Link::seal()

   .. group-tab:: Python

      .. code:: Python

         from simgrid import Link

      .. automethod:: simgrid.Link.seal

   .. group-tab:: C

      .. code:: C

         #include <simgrid/link.h>

      .. doxygentypedef:: sg_link_t
      .. doxygentypedef:: const_sg_link_t

Retrieving links
----------------

.. tabs::

   .. group-tab:: C++

      See also :cpp:func:`simgrid::s4u::Engine::get_all_links`.

      .. doxygenfunction:: simgrid::s4u::Link::by_name(const std::string &name)
      .. doxygenfunction:: simgrid::s4u::Link::by_name_or_null(const std::string &name)

   .. group-tab:: Python

      See also :py:attr:`simgrid.Engine.all_links`.

      .. automethod:: simgrid.Link.by_name
      .. automethod:: simgrid.Link.by_name_or_null

   .. group-tab:: C

      .. doxygenfunction:: sg_link_by_name(const char *name)
      .. doxygenfunction:: sg_link_count()
      .. doxygenfunction:: sg_link_list()

Querying info
--------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Link::get_cname() const
      .. doxygenfunction:: simgrid::s4u::Link::get_name() const
      .. doxygenfunction:: simgrid::s4u::Link::get_load() const
      .. doxygenfunction:: simgrid::s4u::Link::is_used() const

   .. group-tab:: Python

      .. autoattribute:: simgrid.Link.name
      .. autoattribute:: simgrid.Link.load
      .. autoattribute:: simgrid.Link.is_used

   .. group-tab:: C

      .. doxygenfunction:: sg_link_get_name(const_sg_link_t link)
      .. doxygenfunction:: sg_link_is_shared(const_sg_link_t link)

Performance
-----------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Link::get_bandwidth() const
      .. doxygenfunction:: simgrid::s4u::Link::get_latency() const
      .. doxygenfunction:: simgrid::s4u::Link::set_bandwidth(double value)
      .. doxygenfunction:: simgrid::s4u::Link::set_latency(double value)
      .. doxygenfunction:: simgrid::s4u::Link::set_latency(const std::string& value)

   .. group-tab:: Python

      .. autoattribute:: simgrid.Link.bandwidth
      .. autoattribute:: simgrid.Link.latency
      .. automethod:: simgrid.Link.set_bandwidth
      .. automethod:: simgrid.Link.set_latency

   .. group-tab:: C

      .. doxygenfunction:: sg_link_get_bandwidth(const_sg_link_t link)
      .. doxygenfunction:: sg_link_get_latency(const_sg_link_t link)
      .. doxygenfunction:: sg_link_set_bandwidth(sg_link_t link, double value)
      .. doxygenfunction:: sg_link_set_latency(sg_link_t link, double value)

Model policy
------------

.. tabs::

   .. group-tab:: C++

      .. doxygenenum:: simgrid::s4u::Link::SharingPolicy

      .. doxygenfunction:: simgrid::s4u::Link::get_sharing_policy() const
      .. doxygenfunction:: simgrid::s4u::Link::set_sharing_policy

      .. doxygenfunction:: simgrid::s4u::Link::get_concurrency_limit() const
      .. doxygenfunction:: simgrid::s4u::Link::set_concurrency_limit(int limit)

   .. group-tab:: Python

      .. autoattribute:: simgrid.Link.concurrency_limit
      .. automethod:: simgrid.Link.set_concurrency_limit
      .. automethod:: simgrid.Link.get_sharing_policy
      .. automethod:: simgrid.Link.set_sharing_policy

   .. group-tab:: C


User data and properties
------------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Link::get_property(const std::string &key) const
      .. doxygenfunction:: simgrid::s4u::Link::get_properties() const
      .. doxygenfunction:: simgrid::s4u::Link::set_property(const std::string &key, const std::string &value)
      .. doxygenfunction:: simgrid::s4u::Link::set_properties(const std::unordered_map< std::string, std::string > &properties)

   .. group-tab:: Python

      .. automethod:: simgrid.Link.get_property
      .. automethod:: simgrid.Link.get_properties
      .. automethod:: simgrid.Link.set_property
      .. automethod:: simgrid.Link.set_properties

   .. group-tab:: C

      .. doxygenfunction:: sg_link_get_data(const_sg_link_t link)
      .. doxygenfunction:: sg_link_set_data(sg_link_t link, void *data)

On/Off
------

.. tabs::

   .. group-tab:: C++

      See also :cpp:func:`simgrid::s4u::Link::set_state_profile`.

      .. doxygenfunction:: simgrid::s4u::Link::is_on() const
      .. doxygenfunction:: simgrid::s4u::Link::turn_off()
      .. doxygenfunction:: simgrid::s4u::Link::turn_on()

   .. group-tab:: Python

      See also :py:func:`simgrid.Link.set_state_profile`.

      .. automethod:: simgrid.Link.is_on
      .. automethod:: simgrid.Link.turn_off
      .. automethod:: simgrid.Link.turn_on

Dynamic profiles
----------------

See :ref:`howto_churn` for more details.

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Link::set_bandwidth_profile(kernel::profile::Profile *profile)
      .. doxygenfunction:: simgrid::s4u::Link::set_latency_profile(kernel::profile::Profile *profile)
      .. doxygenfunction:: simgrid::s4u::Link::set_state_profile(kernel::profile::Profile *profile)

   .. group-tab:: Python

      .. automethod:: simgrid.Link.set_bandwidth_profile
      .. automethod:: simgrid.Link.set_latency_profile
      .. automethod:: simgrid.Link.set_state_profile

WIFI links
----------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Link::set_host_wifi_rate

   .. group-tab:: Python

      .. automethod:: simgrid.Link.set_host_wifi_rate

Signals
-------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Link::on_creation_cb
      .. doxygenfunction:: simgrid::s4u::Link::on_onoff_cb
      .. doxygenfunction:: simgrid::s4u::Link::on_destruction_cb
      .. doxygenfunction:: simgrid::s4u::Link::on_bandwidth_change_cb
      .. doxygenfunction:: simgrid::s4u::Link::on_this_onoff_cb
      .. doxygenfunction:: simgrid::s4u::Link::on_this_destruction_cb
      .. doxygenfunction:: simgrid::s4u::Link::on_this_bandwidth_change_cb
      .. doxygenfunction:: simgrid::s4u::Link::on_communication_state_change_cb

.. _API_s4u_NetZone:

================
⁣  class NetZone
================

.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::NetZone

   .. group-tab:: Python

      .. autoclass:: simgrid.NetZone

Basic management
----------------

.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/NetZone.hpp>

      Note that there is no NetZonePtr type and that you cannot use the RAII
      idiom on network zones because SimGrid does not allow (yet) to create nor
      destroy resources once the simulation is started.

      .. doxygenfunction:: simgrid::s4u::NetZone::seal

   .. group-tab:: Python

      .. code:: Python

         from simgrid import NetZone

      .. automethod:: simgrid.NetZone.seal

   .. group-tab:: C

      .. code:: C

         #include <simgrid/zone.h>

      .. doxygentypedef:: sg_netzone_t
      .. cpp:type:: const s4u_NetZone* const_sg_netzone_t

         Pointer to a constant network zone object.

Retrieving zones
----------------

.. tabs::

   .. group-tab:: C++

      See :cpp:func:`simgrid::s4u::Engine::get_netzone_root`,
      :cpp:func:`simgrid::s4u::Engine::netzone_by_name_or_null` and
      :cpp:func:`simgrid::s4u::Engine::get_filtered_netzones`.

   .. group-tab:: C

      .. doxygenfunction:: sg_zone_get_by_name(const char *name)
      .. doxygenfunction:: sg_zone_get_root()

Querying info
--------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::NetZone::get_cname() const
      .. doxygenfunction:: simgrid::s4u::NetZone::get_name() const
      .. doxygenfunction:: simgrid::s4u::NetZone::get_netpoint

   .. group-tab:: Python

      .. autoattribute:: simgrid.NetZone.name
      .. autoattribute:: simgrid.NetZone.netpoint

   .. group-tab:: C

      .. doxygenfunction:: sg_zone_get_name(const_sg_netzone_t zone)

User data and properties
------------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::NetZone::get_properties() const
      .. doxygenfunction:: simgrid::s4u::NetZone::get_property(const std::string &key) const
      .. doxygenfunction:: simgrid::s4u::NetZone::set_property(const std::string &key, const std::string &value)

   .. group-tab:: Python

      .. automethod:: simgrid.NetZone.set_property
      .. automethod:: simgrid.NetZone.get_property
      .. automethod:: simgrid.NetZone.get_properties


   .. group-tab:: C

      .. doxygenfunction:: sg_zone_get_property_value(const_sg_netzone_t as, const char *name)
      .. doxygenfunction:: sg_zone_set_property_value(sg_netzone_t netzone, const char *name, const char *value)

Retrieving components
---------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::NetZone::get_all_hosts() const
      .. doxygenfunction:: simgrid::s4u::NetZone::get_host_count() const

   .. group-tab:: Python

      .. autoattribute:: simgrid.NetZone.all_hosts
      .. autoattribute:: simgrid.NetZone.host_count

   .. group-tab:: C

      .. doxygenfunction:: sg_zone_get_all_hosts(const_sg_netzone_t zone, int *size)

Routing data
------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::NetZone::add_component(kernel::routing::NetPoint *elm)
      .. doxygenfunction:: simgrid::s4u::NetZone::add_route(const Host *src, const Host *dst, const std::vector< LinkInRoute > &link_list, bool symmetrical=true)
      .. doxygenfunction:: simgrid::s4u::NetZone::add_route(const Host *src, const Host *dst, const std::vector< const Link * > &links)
      .. doxygenfunction:: simgrid::s4u::NetZone::add_route(const NetZone *src, const NetZone *dst, const std::vector< LinkInRoute > &link_list, bool symmetrical=true)
      .. doxygenfunction:: simgrid::s4u::NetZone::add_route(const NetZone *src, const NetZone *dst, const std::vector< const Link * > &links)
      .. doxygenfunction:: simgrid::s4u::NetZone::add_bypass_route(kernel::routing::NetPoint* src, kernel::routing::NetPoint* dst, kernel::routing::NetPoint* gw_src, kernel::routing::NetPoint* gw_dst, const std::vector<LinkInRoute>& link_list)
      .. doxygenfunction:: simgrid::s4u::NetZone::get_children() const
      .. doxygenfunction:: simgrid::s4u::NetZone::get_parent() const
      .. doxygenfunction:: simgrid::s4u::NetZone::get_gateway() const
      .. doxygenfunction:: simgrid::s4u::NetZone::get_gateway(const std::string& name) const
      .. doxygenfunction:: simgrid::s4u::NetZone::set_gateway(kernel::routing::NetPoint* router)
      .. doxygenfunction:: simgrid::s4u::NetZone::set_gateway(const std::string& name, kernel::routing::NetPoint* router)
      .. doxygenfunction:: simgrid::s4u::NetZone::get_network_model() const

   .. group-tab:: Python

      .. automethod:: simgrid.NetZone.add_component
      .. automethod:: simgrid.NetZone.add_route
      .. automethod:: simgrid.NetZone.add_bypass_route
      .. automethod:: simgrid.NetZone.set_gateway
      .. automethod:: simgrid.NetZone.get_children
      .. autoattribute:: simgrid.NetZone.parent

   .. group-tab:: C

      .. doxygenfunction:: sg_zone_get_childs(const_sg_netzone_t zone, int *size)

Signals
-------

.. tabs::

  .. group-tab:: C++

     .. doxygenfunction:: simgrid::s4u::NetZone::on_creation_cb
     .. doxygenfunction:: simgrid::s4u::NetZone::on_seal_cb

Creating resources
------------------

Zones
^^^^^
.. tabs::

  .. group-tab:: C++

     .. doxygenfunction:: simgrid::s4u::NetZone::add_netzone_full
     .. doxygenfunction:: simgrid::s4u::NetZone::add_netzone_empty
     .. doxygenfunction:: simgrid::s4u::NetZone::add_netzone_star
     .. doxygenfunction:: simgrid::s4u::NetZone::add_netzone_dijkstra
     .. doxygenfunction:: simgrid::s4u::NetZone::add_netzone_floyd
     .. doxygenfunction:: simgrid::s4u::NetZone::add_netzone_vivaldi
     .. doxygenfunction:: simgrid::s4u::NetZone::add_netzone_wifi
     .. doxygenfunction:: simgrid::s4u::NetZone::add_netzone_torus
     .. doxygenfunction:: simgrid::s4u::NetZone::add_netzone_fatTree
     .. doxygenfunction:: simgrid::s4u::NetZone::add_netzone_dragonfly

  .. group-tab:: Python

     .. automethod:: simgrid.NetZone.add_netzone_full
     .. automethod:: simgrid.NetZone.add_netzone_empty
     .. automethod:: simgrid.NetZone.add_netzone_star
     .. automethod:: simgrid.NetZone.add_netzone_dijkstra
     .. automethod:: simgrid.NetZone.add_netzone_floyd
     .. automethod:: simgrid.NetZone.add_netzone_vivaldi
     .. automethod:: simgrid.NetZone.add_netzone_wifi
     .. automethod:: simgrid.NetZone.add_netzone_torus
     .. automethod:: simgrid.NetZone.add_netzone_fatTree
     .. automethod:: simgrid.NetZone.add_netzone_dragonfly

Hosts
^^^^^

.. tabs::

  .. group-tab:: C++

     .. doxygenfunction:: simgrid::s4u::NetZone::add_host(const std::string& name, const std::vector<double>& speed_per_pstate)
     .. doxygenfunction:: simgrid::s4u::NetZone::add_host(const std::string& name, double speed)
     .. doxygenfunction:: simgrid::s4u::NetZone::add_host(const std::string& name, const std::vector<std::string>& speed_per_pstate)
     .. doxygenfunction:: simgrid::s4u::NetZone::add_host(const std::string& name, const std::string& speed)

  .. group-tab:: Python

     .. automethod:: simgrid.NetZone.add_host

Links
^^^^^

.. tabs::

  .. group-tab:: C++

     .. doxygenfunction:: simgrid::s4u::NetZone::add_link(const std::string &name, const std::vector< double > &bandwidths)
     .. doxygenfunction:: simgrid::s4u::NetZone::add_link(const std::string &name, double bandwidth)
     .. doxygenfunction:: simgrid::s4u::NetZone::add_link(const std::string &name, const std::vector< std::string > &bandwidths)
     .. doxygenfunction:: simgrid::s4u::NetZone::add_link(const std::string &name, const std::string &bandwidth)
     .. doxygenfunction:: simgrid::s4u::NetZone::add_split_duplex_link(const std::string &name, const std::string &bw_up, const std::string &bw_down = "")
     .. doxygenfunction:: simgrid::s4u::NetZone::add_split_duplex_link(const std::string &name, double bw_up, double bw_down = -1)

  .. group-tab:: Python

     .. automethod:: simgrid.NetZone.add_link
     .. automethod:: simgrid.NetZone.add_split_duplex_link

Router
^^^^^^

.. tabs::

  .. group-tab:: C++

     .. doxygenfunction:: simgrid::s4u::NetZone::add_router(const std::string& name)

  .. group-tab:: Python

     .. automethod:: simgrid.NetZone.add_router

.. _API_s4u_VirtualMachine:

=======================
⁣  class VirtualMachine
=======================


.. doxygenclass:: simgrid::s4u::VirtualMachine

Basic management
----------------
.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/VirtualMachine.hpp>

      Note that there is no VirtualMachinePtr type, and that you cannot use the RAII
      idiom on virtual machines. There is no good reason for that and should change in the future.

   .. group-tab:: C

      .. code:: C

         #include <simgrid/vm.h>

      .. doxygentypedef:: sg_vm_t
      .. cpp:type:: const s4u_VirtualMachine* const_sg_vm_t

         Pointer to a constant virtual machine object.

Creating VMs
------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Host::create_vm(const std::string &name, int core_amount)
      .. doxygenfunction:: simgrid::s4u::Host::create_vm(const std::string &name, int core_amount, size_t ramsize)
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::destroy

   .. group-tab:: C

      .. doxygenfunction:: sg_vm_create_core
      .. doxygenfunction:: sg_vm_create_multicore
      .. doxygenfunction:: sg_vm_destroy

Querying info
--------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::VirtualMachine::get_pm() const
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::get_ramsize() const
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::get_state() const

      .. doxygenfunction:: simgrid::s4u::VirtualMachine::set_bound(double bound)
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::set_pm(Host *pm)
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::set_ramsize(size_t ramsize)

   .. group-tab:: C

      .. doxygenfunction:: sg_vm_get_ramsize(const_sg_vm_t vm)
      .. doxygenfunction:: sg_vm_set_bound(sg_vm_t vm, double bound)
      .. doxygenfunction:: sg_vm_set_ramsize(sg_vm_t vm, size_t size)

      .. doxygenfunction:: sg_vm_get_name
      .. doxygenfunction:: sg_vm_get_pm
      .. doxygenfunction:: sg_vm_is_created
      .. doxygenfunction:: sg_vm_is_running
      .. doxygenfunction:: sg_vm_is_suspended

Life cycle
----------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::VirtualMachine::resume()
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::shutdown()
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::start()
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::suspend()

   .. group-tab:: C

      .. doxygenfunction:: sg_vm_start
      .. doxygenfunction:: sg_vm_suspend
      .. doxygenfunction:: sg_vm_resume
      .. doxygenfunction:: sg_vm_shutdown

Signals
-------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_creation_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_destruction_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_this_destruction_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_migration_end_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_this_migration_end_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_migration_start_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_this_migration_start_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_resume_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_this_resume_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_shutdown_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_this_shutdown_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_start_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_this_start_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_started_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_this_started_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_suspend_cb
      .. doxygenfunction:: simgrid::s4u::VirtualMachine::on_this_suspend_cb

.. _API_s4u_Activity:

==========
Activities
==========

==============
class Activity
==============

.. doxygenclass:: simgrid::s4u::Activity

**Known subclasses:**
:ref:`Communications <API_s4u_Comm>` (started on Mailboxes and consuming links),
:ref:`Executions <API_s4u_Exec>` (started on Host and consuming CPU resources)
:ref:`I/O <API_s4u_Io>` (started on and consuming disks).
See also the :ref:`section on activities <s4u_Activities>` above.

Basic management
----------------

.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/Activity.hpp>

      .. doxygentypedef:: ActivityPtr

   .. group-tab:: C

      .. doxygentypedef:: sg_activity_t
      .. doxygentypedef:: const_sg_activity_t

Querying info
-------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Activity::get_cname() const
      .. doxygenfunction:: simgrid::s4u::Activity::get_name() const
      .. doxygenfunction:: simgrid::s4u::Activity::get_remaining() const
      .. doxygenfunction:: simgrid::s4u::Activity::get_state() const
      .. doxygenfunction:: simgrid::s4u::Activity::set_remaining(double remains)
      .. doxygenfunction:: simgrid::s4u::Activity::set_state(Activity::State state)


Activities life cycle
---------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Activity::start
      .. doxygenfunction:: simgrid::s4u::Activity::cancel
      .. doxygenfunction:: simgrid::s4u::Activity::test
      .. doxygenfunction:: simgrid::s4u::Activity::wait
      .. doxygenfunction:: simgrid::s4u::Activity::wait_for
      .. doxygenfunction:: simgrid::s4u::Activity::wait_until(double time_limit)

Suspending and resuming an activity
-----------------------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Activity::suspend
      .. doxygenfunction:: simgrid::s4u::Activity::resume
      .. doxygenfunction:: simgrid::s4u::Activity::is_suspended


.. _API_s4u_Comm:

=============
⁣  class Comm
=============

.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::Comm

   .. group-tab:: Python

      .. autoclass:: simgrid.Comm

Basic management
----------------

.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/Comm.hpp>

      .. doxygentypedef:: CommPtr

   .. group-tab:: Python

      .. code:: Python

         from simgrid import Comm

   .. group-tab:: c

      .. code:: c

         #include <simgrid/comm.h>

      .. doxygentypedef:: sg_comm_t

Querying info
-------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Comm::get_dst_data_size() const
      .. doxygenfunction:: simgrid::s4u::Comm::get_mailbox() const
      .. doxygenfunction:: simgrid::s4u::Comm::get_sender() const
      .. doxygenfunction:: simgrid::s4u::Comm::set_dst_data(void **buff)
      .. doxygenfunction:: simgrid::s4u::Comm::set_dst_data(void **buff, size_t size)
      .. doxygenfunction:: simgrid::s4u::Comm::detach()
      .. doxygenfunction:: simgrid::s4u::Comm::detach(const std::function<void(void*)>& clean_function)
      .. doxygenfunction:: simgrid::s4u::Comm::set_payload_size(uint64_t bytes)
      .. doxygenfunction:: simgrid::s4u::Comm::set_rate(double rate)
      .. doxygenfunction:: simgrid::s4u::Comm::set_src_data(void *buff)
      .. doxygenfunction:: simgrid::s4u::Comm::set_src_data(void *buff, size_t size)
      .. doxygenfunction:: simgrid::s4u::Comm::set_src_data_size(size_t size)

   .. group-tab:: Python

      .. autoattribute:: simgrid.Comm.dst_data_size
      .. autoattribute:: simgrid.Comm.mailbox
      .. autoattribute:: simgrid.Comm.sender
      .. autoattribute:: simgrid.Comm.state_str
      .. automethod:: simgrid.Comm.detach
      .. automethod:: simgrid.Comm.set_payload_size
      .. automethod:: simgrid.Comm.set_rate

Direct host-to-host communication
---------------------------------

Most communications are created using :ref:`s4u_mailbox`, but you can
also start direct communications as shown below. See also the
:ref:`relevant examples <s4u_ex_comm_host2host>`.

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Comm::sendto
      .. doxygenfunction:: simgrid::s4u::Comm::sendto_init()
      .. doxygenfunction:: simgrid::s4u::Comm::sendto_init(s4u::Host *from, s4u::Host *to)
      .. doxygenfunction:: simgrid::s4u::Comm::sendto_async

   .. group-tab:: Python

      .. automethod:: simgrid.Comm.sendto
      .. automethod:: simgrid.Comm.sendto_init
      .. automethod:: simgrid.Comm.sendto_async

Life cycle
----------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Comm::cancel
      .. doxygenfunction:: simgrid::s4u::Comm::start
      .. doxygenfunction:: simgrid::s4u::Comm::test
      .. doxygenfunction:: simgrid::s4u::Comm::wait
      .. doxygenfunction:: simgrid::s4u::Comm::wait_for
      .. doxygenfunction:: simgrid::s4u::Comm::wait_until

   .. group-tab:: Python

      .. automethod:: simgrid.Comm.cancel
      .. automethod:: simgrid.Comm.start
      .. automethod:: simgrid.Comm.test
      .. automethod:: simgrid.Comm.wait
      .. automethod:: simgrid.Comm.wait_for
      .. automethod:: simgrid.Comm.wait_until

   .. group-tab:: C

      .. doxygenfunction:: sg_comm_test
      .. doxygenfunction:: sg_comm_wait

Suspending and resuming a communication
---------------------------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Comm::suspend
      .. doxygenfunction:: simgrid::s4u::Comm::resume
      .. doxygenfunction:: simgrid::s4u::Comm::is_suspended

   .. group-tab:: Python

      .. automethod:: simgrid.Comm.suspend
      .. automethod:: simgrid.Comm.resume
      .. autoattribute:: simgrid.Comm.is_suspended

Signals
-------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Comm::on_veto_cb
      .. doxygenfunction:: simgrid::s4u::Comm::on_start_cb
      .. doxygenfunction:: simgrid::s4u::Comm::on_suspend_cb
      .. doxygenfunction:: simgrid::s4u::Comm::on_resume_cb
      .. doxygenfunction:: simgrid::s4u::Comm::on_completion_cb
      .. doxygenfunction:: simgrid::s4u::Comm::on_this_veto_cb
      .. doxygenfunction:: simgrid::s4u::Comm::on_this_start_cb
      .. doxygenfunction:: simgrid::s4u::Comm::on_this_suspend_cb
      .. doxygenfunction:: simgrid::s4u::Comm::on_this_resume_cb
      .. doxygenfunction:: simgrid::s4u::Comm::on_this_completion_cb

      .. doxygenfunction:: simgrid::s4u::Comm::on_recv_cb
      .. doxygenfunction:: simgrid::s4u::Comm::on_send_cb
      .. doxygenfunction:: simgrid::s4u::Comm::on_this_recv_cb
      .. doxygenfunction:: simgrid::s4u::Comm::on_this_send_cb

.. _API_s4u_Exec:

=============
⁣  class Exec
=============

.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::Exec

   .. group-tab:: Python

      .. autoclass:: simgrid.Exec

   .. group-tab:: C

      .. doxygentypedef:: sg_exec_t
      .. doxygentypedef:: const_sg_exec_t

Basic management
----------------

.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/Exec.hpp>

      .. doxygentypedef:: ExecPtr

   .. group-tab:: Python

      .. code:: Python

         from simgrid import Exec

   .. group-tab:: C

      .. code-block:: C

         #include <simgrid/exec.h>

Querying info
-------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Exec::get_cost() const
      .. doxygenfunction:: simgrid::s4u::Exec::get_finish_time() const
      .. doxygenfunction:: simgrid::s4u::Exec::get_host() const
      .. doxygenfunction:: simgrid::s4u::Exec::get_host_number() const
      .. doxygenfunction:: simgrid::s4u::Exec::get_remaining
      .. doxygenfunction:: simgrid::s4u::Exec::get_remaining_ratio
      .. doxygenfunction:: simgrid::s4u::Exec::get_start_time() const
      .. doxygenfunction:: simgrid::s4u::Exec::set_bound(double bound)
      .. doxygenfunction:: simgrid::s4u::Exec::set_host
      .. doxygenfunction:: simgrid::s4u::Exec::set_priority(double priority)

   .. group-tab:: Python

      .. autoattribute:: simgrid.Exec.host
      .. autoattribute:: simgrid.Exec.remaining
      .. autoattribute:: simgrid.Exec.remaining_ratio

   .. group-tab:: C

      .. doxygenfunction:: sg_exec_set_bound(sg_exec_t exec, double bound)
      .. doxygenfunction:: sg_exec_get_name(const_sg_exec_t exec)
      .. doxygenfunction:: sg_exec_set_name(sg_exec_t exec, const char* name)
      .. doxygenfunction:: sg_exec_set_host(sg_exec_t exec, sg_host_t new_host)
      .. doxygenfunction:: sg_exec_get_remaining(const_sg_exec_t exec)
      .. doxygenfunction:: sg_exec_get_remaining_ratio(const_sg_exec_t exec)

Life cycle
----------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Exec::cancel
      .. doxygenfunction:: simgrid::s4u::Exec::start
      .. doxygenfunction:: simgrid::s4u::Exec::test
      .. doxygenfunction:: simgrid::s4u::Exec::wait

   .. group-tab:: Python

       .. automethod:: simgrid.Exec.cancel
       .. automethod:: simgrid.Exec.start
       .. automethod:: simgrid.Exec.test
       .. automethod:: simgrid.Exec.wait

   .. group-tab:: C

       .. doxygenfunction:: sg_exec_start(sg_exec_t exec)
       .. doxygenfunction:: sg_exec_cancel(sg_exec_t exec);
       .. doxygenfunction:: sg_exec_test(sg_exec_t exec);
       .. doxygenfunction:: sg_exec_wait(sg_exec_t exec);

Suspending and resuming an execution
------------------------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Exec::suspend
      .. doxygenfunction:: simgrid::s4u::Exec::resume
      .. doxygenfunction:: simgrid::s4u::Exec::is_suspended

   .. group-tab:: Python

      .. automethod:: simgrid.Exec.suspend
      .. automethod:: simgrid.Exec.resume
      .. autoattribute:: simgrid.Exec.is_suspended

Signals
-------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Exec::on_veto_cb
      .. doxygenfunction:: simgrid::s4u::Exec::on_start_cb
      .. doxygenfunction:: simgrid::s4u::Exec::on_suspend_cb
      .. doxygenfunction:: simgrid::s4u::Exec::on_resume_cb
      .. doxygenfunction:: simgrid::s4u::Exec::on_completion_cb
      .. doxygenfunction:: simgrid::s4u::Exec::on_this_veto_cb
      .. doxygenfunction:: simgrid::s4u::Exec::on_this_start_cb
      .. doxygenfunction:: simgrid::s4u::Exec::on_this_suspend_cb
      .. doxygenfunction:: simgrid::s4u::Exec::on_this_resume_cb
      .. doxygenfunction:: simgrid::s4u::Exec::on_this_completion_cb

.. _API_s4u_Io:

===========
⁣  class Io
===========

.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::Io

   .. group-tab:: Python

      .. autoclass:: simgrid.Io

Basic management
----------------

.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/Io.hpp>

      .. doxygentypedef:: IoPtr

Querying info
-------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Io::get_performed_ioops() const
      .. doxygenfunction:: simgrid::s4u::Io::get_remaining

Life cycle
----------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Io::cancel
      .. doxygenfunction:: simgrid::s4u::Io::start
      .. doxygenfunction:: simgrid::s4u::Io::test
      .. doxygenfunction:: simgrid::s4u::Io::wait

   .. group-tab:: Python

      .. automethod:: simgrid.Io.test
      .. automethod:: simgrid.Io.wait


Signals
-------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Io::on_veto_cb
      .. doxygenfunction:: simgrid::s4u::Io::on_start_cb
      .. doxygenfunction:: simgrid::s4u::Io::on_suspend_cb
      .. doxygenfunction:: simgrid::s4u::Io::on_resume_cb
      .. doxygenfunction:: simgrid::s4u::Io::on_completion_cb
      .. doxygenfunction:: simgrid::s4u::Io::on_this_veto_cb
      .. doxygenfunction:: simgrid::s4u::Io::on_this_start_cb
      .. doxygenfunction:: simgrid::s4u::Io::on_this_suspend_cb
      .. doxygenfunction:: simgrid::s4u::Io::on_this_resume_cb
      .. doxygenfunction:: simgrid::s4u::Io::on_this_completion_cb

.. _API_s4u_ActivitySet:

====================
⁣  class ActivitySet
====================

.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::ActivitySet

   .. group-tab:: Python

      .. autoclass:: simgrid.ActivitySet

   .. group-tab:: C

      .. doxygentypedef:: sg_activity_set_t
      .. doxygentypedef:: const_sg_activity_set_t

Basic management
----------------

.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/ActivitySet.hpp>

      .. doxygentypedef:: ActivitySetPtr

   .. group-tab:: Python

      .. code:: Python

         from simgrid import ActivitySet

   .. group-tab:: C

      .. code-block:: C

         #include <simgrid/activity_set.h>

      .. doxygenfunction:: sg_activity_set_init
      .. doxygenfunction:: sg_activity_set_delete

Managing activities
-------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::ActivitySet::push
      .. doxygenfunction:: simgrid::s4u::ActivitySet::erase
      .. doxygenfunction:: simgrid::s4u::ActivitySet::empty
      .. doxygenfunction:: simgrid::s4u::ActivitySet::size

   .. group-tab:: Python

      .. automethod:: simgrid.ActivitySet.push()
      .. automethod:: simgrid.ActivitySet.erase()
      .. automethod:: simgrid.ActivitySet.empty()
      .. automethod:: simgrid.ActivitySet.size()

   .. group-tab:: c

      .. doxygenfunction:: sg_activity_set_push
      .. doxygenfunction:: sg_activity_set_erase
      .. doxygenfunction:: sg_activity_set_empty
      .. doxygenfunction:: sg_activity_set_size

Interacting with the set
------------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::ActivitySet::test_any
      .. doxygenfunction:: simgrid::s4u::ActivitySet::wait_all
      .. doxygenfunction:: simgrid::s4u::ActivitySet::wait_all_for
      .. doxygenfunction:: simgrid::s4u::ActivitySet::wait_any
      .. doxygenfunction:: simgrid::s4u::ActivitySet::wait_any_for

   .. group-tab:: Python

      .. automethod:: simgrid.ActivitySet.test_any()
      .. automethod:: simgrid.ActivitySet.wait_all()
      .. automethod:: simgrid.ActivitySet.wait_all_for()
      .. automethod:: simgrid.ActivitySet.wait_any()
      .. automethod:: simgrid.ActivitySet.wait_any_for()

   .. group-tab:: c

      .. doxygenfunction:: sg_activity_set_test_any
      .. doxygenfunction:: sg_activity_set_wait_all
      .. doxygenfunction:: sg_activity_set_wait_all_for
      .. doxygenfunction:: sg_activity_set_wait_any
      .. doxygenfunction:: sg_activity_set_wait_any_for
      .. doxygenfunction:: sg_activity_unref

Dealing with failed activities
------------------------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::ActivitySet::get_failed_activity()
      .. doxygenfunction:: simgrid::s4u::ActivitySet::has_failed_activities() const

.. _API_s4u_Tasks:

==========
Tasks
==========

==============
class Task
==============

.. doxygenclass:: simgrid::s4u::Task

**Known subclasses:**
:ref:`Communication Tasks <API_s4u_CommTask>`,
:ref:`Executions Tasks <API_s4u_ExecTask>`,
:ref:`I/O Tasks <API_s4u_IoTask>`.
See also the :ref:`section on activities <s4u_Tasks>` above.

Basic management
----------------

.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/Task.hpp>

      .. doxygentypedef:: TaskPtr

Querying info
-------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::Task::get_cname() const
      .. doxygenfunction:: simgrid::s4u::Task::get_name() const
      .. doxygenfunction:: simgrid::s4u::Task::get_count(const std::string& instance) const
      .. doxygenfunction:: simgrid::s4u::Task::get_amount(const std::string& instance) const
      .. doxygenfunction:: simgrid::s4u::Task::get_queued_firings(const std::string& instance) const
      .. doxygenfunction:: simgrid::s4u::Task::get_running_count(const std::string& instance) const
      .. doxygenfunction:: simgrid::s4u::Task::get_parallelism_degree(const std::string& instance) const
      .. doxygenfunction:: simgrid::s4u::Task::set_name(std::string name)

Life cycle
----------

.. tabs::

   .. group-tab:: C++
      .. doxygenfunction:: simgrid::s4u::Task::enqueue_firings(int n)
      .. doxygenfunction:: simgrid::s4u::Task::set_amount(double amount, std::string instance)
      .. doxygenfunction:: simgrid::s4u::Task::set_parallelism_degree(int n, const std::string & instance = "all")

Managing Dependencies
---------------------

.. tabs::

   .. group-tab:: C++
      .. doxygenfunction:: simgrid::s4u::Task::add_successor(TaskPtr t)
      .. doxygenfunction:: simgrid::s4u::Task::remove_successor(TaskPtr t)
      .. doxygenfunction:: simgrid::s4u::Task::remove_all_successors()
      .. doxygenfunction:: simgrid::s4u::Task::get_successors() const

Managing Tokens
---------------

.. doxygenclass:: simgrid::s4u::Token

.. tabs::

   .. group-tab:: C++
      .. doxygenfunction:: simgrid::s4u::Task::get_token_from(TaskPtr t) const
      .. doxygenfunction:: simgrid::s4u::Task::get_tokens_from(TaskPtr t) const
      .. doxygenfunction:: simgrid::s4u::Task::deque_token_from(TaskPtr t)
      .. doxygenfunction:: simgrid::s4u::Task::set_token(std::shared_ptr<Token> token)

Signals
-------

.. tabs::

   .. group-tab:: C++
      .. doxygenfunction:: simgrid::s4u::Task::on_start_cb
      .. doxygenfunction:: simgrid::s4u::Task::on_this_start_cb
      .. doxygenfunction:: simgrid::s4u::Task::on_completion_cb
      .. doxygenfunction:: simgrid::s4u::Task::on_this_completion_cb

.. _API_s4u_CommTask:

=================
⁣  class CommTask
=================
.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::CommTask

Basic management
----------------

.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/Task.hpp>

      .. doxygentypedef:: CommTaskPtr

Querying info
-------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::CommTask::get_source() const
      .. doxygenfunction:: simgrid::s4u::CommTask::get_destination() const
      .. doxygenfunction:: simgrid::s4u::CommTask::get_bytes() const
      .. doxygenfunction:: simgrid::s4u::CommTask::set_source(Host* source);
      .. doxygenfunction:: simgrid::s4u::CommTask::set_destination(Host* destination);
      .. doxygenfunction:: simgrid::s4u::CommTask::set_bytes(double bytes)


.. _API_s4u_ExecTask:

=================
⁣  class ExecTask
=================
.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::ExecTask

Basic management
----------------

.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/Task.hpp>

      .. doxygentypedef:: ExecTaskPtr

Querying info
-------------

.. tabs::

   .. group-tab:: C++

      .. doxygenfunction:: simgrid::s4u::ExecTask::get_host(std::string instance) const
      .. doxygenfunction:: simgrid::s4u::ExecTask::get_flops(std::string instance) const
      .. doxygenfunction:: simgrid::s4u::ExecTask::set_host(Host* host, std::string instance);
      .. doxygenfunction:: simgrid::s4u::ExecTask::set_flops(double flops, std::string instance);
      .. doxygenfunction:: simgrid::s4u::ExecTask::add_instances(int n);
      .. doxygenfunction:: simgrid::s4u::ExecTask::remove_instances(int n);

.. _API_s4u_IoTask:

================
⁣  class IoTask
================
.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::IoTask

Basic management
----------------

.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/Task.hpp>

      .. doxygentypedef:: IoTaskPtr

Querying info
-------------

.. tabs::

   .. group-tab:: C++

     .. doxygenfunction:: simgrid::s4u::IoTask::get_disk() const
     .. doxygenfunction:: simgrid::s4u::IoTask::get_bytes() const
     .. doxygenfunction:: simgrid::s4u::IoTask::get_op_type() const
     .. doxygenfunction:: simgrid::s4u::IoTask::set_disk(Disk* disk);
     .. doxygenfunction:: simgrid::s4u::IoTask::set_bytes(double bytes);
     .. doxygenfunction:: simgrid::s4u::IoTask::set_op_type(Io::OpType type);

.. _API_s4u_Synchronizations:

=======================
Synchronization Objects
=======================

.. _API_s4u_Mutex:

==============
⁣  Mutex
==============

.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::Mutex

   .. group-tab:: Python

      .. autoclass:: simgrid.Mutex

Basic management
----------------

   .. tabs::

      .. group-tab:: C++

         .. code-block:: C++

            #include <simgrid/s4u/Mutex.hpp>

         .. doxygentypedef:: MutexPtr

         .. doxygenfunction:: simgrid::s4u::Mutex::create

      .. group-tab:: Python

         .. code-block:: Python

            from simgrid import Mutex
            mutex = Mutex()

            # Use a context manager to acquire and automatically release the mutex
            # when leaving the scope.
            with mutex:
                # Access shared resource ...
                pass

         .. automethod:: simgrid.Mutex.__init__

      .. group-tab:: C

         .. code-block:: C

            #include <simgrid/mutex.h>

         .. doxygentypedef:: sg_mutex_t
         .. cpp:type:: const s4u_Mutex* const_sg_mutex_t

            Pointer to a constant mutex object.

         .. doxygenfunction:: sg_mutex_init()
         .. doxygenfunction:: sg_mutex_destroy(const_sg_mutex_t mutex)

Locking
-------

   .. tabs::

      .. group-tab:: C++

         .. doxygenfunction:: simgrid::s4u::Mutex::lock()
         .. doxygenfunction:: simgrid::s4u::Mutex::try_lock()
         .. doxygenfunction:: simgrid::s4u::Mutex::unlock()

      .. group-tab:: Python

         .. automethod:: simgrid.Mutex.lock
         .. automethod:: simgrid.Mutex.try_lock
         .. automethod:: simgrid.Mutex.unlock

      .. group-tab:: C

         .. doxygenfunction:: sg_mutex_lock(sg_mutex_t mutex)
         .. doxygenfunction:: sg_mutex_try_lock(sg_mutex_t mutex)
         .. doxygenfunction:: sg_mutex_unlock(sg_mutex_t mutex)

.. _API_s4u_Barrier:

================
⁣  Barrier
================

.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::Barrier

   .. group-tab:: Python

      .. autoclass:: simgrid.Barrier

.. tabs::

   .. group-tab:: C++

      .. code-block:: C++

         #include <simgrid/s4u/Barrier.hpp>

      .. doxygentypedef:: BarrierPtr

      .. doxygenfunction:: simgrid::s4u::Barrier::create(unsigned int expected_actors)
      .. doxygenfunction:: simgrid::s4u::Barrier::wait()
      .. doxygenfunction:: simgrid::s4u::Barrier::to_string() const

   .. group-tab:: Python

      .. code-block:: Python

         from simgrid import Barrier
         barrier = Barrier(2)

      .. automethod:: simgrid.Barrier.__init__
      .. automethod:: simgrid.Barrier.wait

   .. group-tab:: C

      .. code-block:: C

         #include <simgrid/barrier.hpp>

      .. doxygentypedef:: sg_bar_t

      .. doxygenfunction:: sg_barrier_init(unsigned int count)
      .. doxygenfunction:: sg_barrier_destroy(sg_bar_t bar)
      .. doxygenfunction:: sg_barrier_wait(sg_bar_t bar)


.. _API_s4u_ConditionVariable:

==========================
⁣  Condition variable
==========================

.. doxygenclass:: simgrid::s4u::ConditionVariable

Basic management
----------------

   .. tabs::

      .. group-tab:: C++

         .. code-block:: C++

            #include <simgrid/s4u/ConditionVariable.hpp>

         .. doxygentypedef:: ConditionVariablePtr

         .. doxygenfunction:: simgrid::s4u::ConditionVariable::create()

      .. group-tab:: C

         .. code-block:: C

            #include <simgrid/cond.h>

         .. doxygentypedef:: sg_cond_t
         .. doxygentypedef:: const_sg_cond_t
         .. doxygenfunction:: sg_cond_init
         .. doxygenfunction:: sg_cond_destroy

Waiting and notifying
---------------------

   .. tabs::

      .. group-tab:: C++

         .. doxygenfunction:: simgrid::s4u::ConditionVariable::notify_all()
         .. doxygenfunction:: simgrid::s4u::ConditionVariable::notify_one()
         .. doxygenfunction:: simgrid::s4u::ConditionVariable::wait(s4u::MutexPtr lock)
         .. doxygenfunction:: simgrid::s4u::ConditionVariable::wait(const std::unique_lock< s4u::Mutex > &lock)
         .. doxygenfunction:: simgrid::s4u::ConditionVariable::wait(const std::unique_lock< Mutex > &lock, P pred)
         .. doxygenfunction:: simgrid::s4u::ConditionVariable::wait_for(const std::unique_lock< s4u::Mutex > &lock, double duration)
         .. doxygenfunction:: simgrid::s4u::ConditionVariable::wait_for(const std::unique_lock< s4u::Mutex > &lock, std::chrono::duration< Rep, Period > duration)
         .. doxygenfunction:: simgrid::s4u::ConditionVariable::wait_until(const std::unique_lock< s4u::Mutex > &lock, const SimulationTimePoint< Duration > &timeout_time)
         .. doxygenfunction:: simgrid::s4u::ConditionVariable::wait_until(const std::unique_lock< s4u::Mutex > &lock, double timeout_time)

      .. group-tab:: C

         .. doxygenfunction:: sg_cond_notify_all
         .. doxygenfunction:: sg_cond_notify_one
         .. doxygenfunction:: sg_cond_wait
         .. doxygenfunction:: sg_cond_wait_for

.. _API_s4u_Semaphore:

==================
⁣  Semaphore
==================

.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::s4u::Semaphore

   .. group-tab:: Python

      .. autoclass:: simgrid.Semaphore

Basic management
----------------

   .. tabs::

      .. group-tab:: C++

         .. code-block:: C++

            #include <simgrid/s4u/Semaphore.hpp>

         .. doxygentypedef:: SemaphorePtr
         .. doxygenfunction:: simgrid::s4u::Semaphore::create(unsigned int initial_capacity)

      .. group-tab:: Python

         .. code-block:: Python

            from simgrid import Semaphore
            semaphore = Semaphore(1)
            # Automatically acquire the semaphore, and release it after leaving the scope.
            with semaphore:
                # Do something with the shared resource
                pass

         .. automethod:: simgrid.Semaphore.__init__

      .. group-tab:: C

         .. code-block:: C

            #include <simgrid/semaphore.h>

         .. doxygentypedef:: sg_sem_t
         .. cpp:type:: const s4u_Semaphore* const_sg_sem_t

            Pointer to a constant semaphore object.

         .. doxygenfunction:: sg_sem_init(int initial_value)
         .. doxygenfunction:: sg_sem_destroy(const_sg_sem_t sem)

Locking
-------

   .. tabs::

      .. group-tab:: C++

         .. doxygenfunction:: simgrid::s4u::Semaphore::acquire()
         .. doxygenfunction:: simgrid::s4u::Semaphore::acquire_timeout(double timeout)
         .. doxygenfunction:: simgrid::s4u::Semaphore::get_capacity() const
         .. doxygenfunction:: simgrid::s4u::Semaphore::release()
         .. doxygenfunction:: simgrid::s4u::Semaphore::would_block() const

      .. group-tab:: Python

         .. automethod:: simgrid.Semaphore.acquire
         .. automethod:: simgrid.Semaphore.acquire_timeout
         .. autoattribute:: simgrid.Semaphore.capacity
         .. automethod:: simgrid.Semaphore.release
         .. autoattribute:: simgrid.Semaphore.would_block

      .. group-tab:: C

         .. doxygenfunction:: sg_sem_acquire(sg_sem_t sem)
         .. doxygenfunction:: sg_sem_acquire_timeout(sg_sem_t sem, double timeout)
         .. doxygenfunction:: sg_sem_get_capacity(const_sg_sem_t sem)
         .. doxygenfunction:: sg_sem_release(sg_sem_t sem)
         .. doxygenfunction:: sg_sem_would_block(const_sg_sem_t sem)

===============
Error reporting
===============

.. tabs::

   .. group-tab:: C++

      .. doxygenclass:: simgrid::Exception

      The following exceptions denote a problem in the simulated platform, and it is often useful to catch them.

      .. doxygenclass:: simgrid::CancelException
      .. doxygenclass:: simgrid::HostFailureException
      .. doxygenclass:: simgrid::NetworkFailureException
      .. doxygenclass:: simgrid::StorageFailureException
      .. doxygenclass:: simgrid::TimeoutException
      .. doxygenclass:: simgrid::VmFailureException

      The following errors denote a problem in the SimGrid tool itself. Most of the time, you should let these
      exception go, so that the simulation stops. But you may want to catch them, for example when you launch
      SimGrid from a python notebook and want to handle the problem accordingly.

      .. doxygenclass:: simgrid::AssertionError
      .. doxygenclass:: simgrid::ParseError
      .. doxygenclass:: simgrid::TracingError

   .. group-tab:: Python

      The following exceptions denote a problem in the simulated platform, and it is often useful to catch them.

      .. autoclass:: simgrid.CancelException
      .. autoclass:: simgrid.HostFailureException
      .. autoclass:: simgrid.NetworkFailureException
      .. autoclass:: simgrid.StorageFailureException
      .. autoclass:: simgrid.TimeoutException
      .. autoclass:: simgrid.VmFailureException

      The following errors denote a problem in the SimGrid tool itself. Most of the time, you should let these
      exception go, so that the simulation stops. But you may want to catch them, for example when you launch
      SimGrid from a python notebook and want to handle the problem accordingly.

      .. autoclass:: simgrid.AssertionError

   .. group-tab:: C

      .. doxygenenum:: sg_error_t


.. |hr| raw:: html

   <hr />
