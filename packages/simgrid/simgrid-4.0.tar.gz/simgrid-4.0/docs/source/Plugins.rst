.. _plugins:

SimGrid Plugins
###############

.. raw:: html

   <object id="TOC" data="graphical-toc.svg" type="image/svg+xml"></object>
   <script>
   window.onload=function() { // Wait for the SVG to be loaded before changing it
     var elem=document.querySelector("#TOC").contentDocument.getElementById("PluginsBox")
     elem.style="opacity:0.93999999;fill:#ff0000;fill-opacity:0.1;stroke:#000000;stroke-width:0.35277778;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1";
   }
   </script>
   <br>
   <br>

You can extend SimGrid without modifying it, thanks to our plugin
mechanism. This page describes how to write your own plugin, and
documents some of the plugins distributed with SimGrid:

  - :ref:`Host Load <plugin_host_load>`: monitors the load of the compute units.
  - :ref:`Host Energy <plugin_host_energy>`: models the energy dissipation of the compute units.
  - :ref:`Link Energy <plugin_link_energy>`: models the energy dissipation of the network.
  - :ref:`WiFi Energy <plugin_link_energy_wifi>`: models the energy dissipation of wifi links.
  - :ref:`Battery <plugin_battery>`: models batteries that get discharged by the energy consumption of a given host.
  - :ref:`Solar Panel <plugin_solar_panel>`: models solar panels which energy production depends on the solar irradiance.
  - :ref:`Chiller <plugin_chiller>`: models chillers which dissipate heat by consuming energy.

You can activate these plugins with the :ref:`--cfg=plugin <cfg=plugin>` command
line option, for example with ``--cfg=plugin:host_energy``. You can get the full
list of existing plugins with ``--cfg=plugin:help``.

Defining a Plugin
*****************

A plugin can get some additional code executed within the SimGrid
kernel, and attach the data needed by that code to the SimGrid
objects.

The host load plugin in
`src/plugins/host_load.cpp <https://framagit.org/simgrid/simgrid/tree/master/src/plugins/host_load.cpp>`_
constitutes a good introductory example. It defines a class
``HostLoad`` that is meant to be attached to each host. This class
contains a ``EXTENSION_ID`` field that is mandatory to our extension
mechanism. Then, the function ``sg_host_load_plugin_init``
initializes the plugin. It first calls
:cpp:func:`simgrid::s4u::Host::extension_create()` to register its
extension to the ``s4u::Host`` objects, and then attaches some
callbacks to signals.

You can attach your own extension to most kinds of s4u object:
:cpp:class:`Actors <simgrid::s4u::Actor>`,
:cpp:class:`Disks <simgrid::s4u::Disk>`,
:cpp:class:`Hosts <simgrid::s4u::Host>` and
:cpp:class:`Links <simgrid::s4u::Link>`. If you need to extend another
kind of objects, please let us now.

.. cpp:class:: template<class R, class... P> simgrid::xbt::signal<R(P...)>

  A signal/slot mechanism, where you can attach callbacks to a given signal, and then fire the signal.

  The template parameter is the function signature of the signal (the return value currently ignored).

.. cpp:function::: template<class R, class... P, class U>  unsigned int simgrid::xbt::signal<R(P...)>::connect(U slot)

  Add a new callback to this signal.

.. cpp:function:: template<class R, class... P> simgrid::xbt::signal<R(P...)>::operator()(P... args)

  Fire that signal, invoking all callbacks.

.. _s4u_API_signals:

Existing signals
================

- In actors:
  :cpp:func:`Actor::on_creation <simgrid::s4u::Actor::on_creation_cb>`
  :cpp:func:`Actor::on_suspend <simgrid::s4u::Actor::on_suspend_cb>`
  :cpp:func:`Actor::on_this_suspend <simgrid::s4u::Actor::on_this_suspend_cb>`
  :cpp:func:`Actor::on_resume <simgrid::s4u::Actor::on_resume_cb>`
  :cpp:func:`Actor::on_this_resume <simgrid::s4u::Actor::on_this_resume_cb>`
  :cpp:func:`Actor::on_sleep <simgrid::s4u::Actor::on_sleep_cb>`
  :cpp:func:`Actor::on_this_sleep <simgrid::s4u::Actor::on_this_sleep_cb>`
  :cpp:func:`Actor::on_wake_up <simgrid::s4u::Actor::on_wake_up_cb>`
  :cpp:func:`Actor::on_this_wake_up <simgrid::s4u::Actor::on_this_wake_up_cb>`
  :cpp:func:`Actor::on_host_change <simgrid::s4u::Actor::on_host_change_cb>`
  :cpp:func:`Actor::on_this_host_change <simgrid::s4u::Actor::on_this_host_change_cb>`
  :cpp:func:`Actor::on_termination <simgrid::s4u::Actor::on_termination_cb>`
  :cpp:func:`Actor::on_this_termination <simgrid::s4u::Actor::on_this_termination_cb>`
  :cpp:func:`Actor::on_destruction <simgrid::s4u::Actor::on_destruction_cb>`
- In the engine:
  :cpp:func:`Engine::on_platform_creation <simgrid::s4u::Engine::on_platform_creation_cb>`
  :cpp:func:`Engine::on_platform_created <simgrid::s4u::Engine::on_platform_created_cb>`
  :cpp:func:`Engine::on_time_advance <simgrid::s4u::Engine::on_time_advance_cb>`
  :cpp:func:`Engine::on_simulation_end <simgrid::s4u::Engine::on_simulation_end_cb>`
  :cpp:func:`Engine::on_deadlock <simgrid::s4u::Engine::on_deadlock_cb>`

- In resources:

  - :cpp:func:`Disk::on_creation <simgrid::s4u::Disk::on_creation_cb>`
    :cpp:func:`Disk::on_destruction <simgrid::s4u::Disk::on_destruction_cb>`
    :cpp:func:`Disk::on_this_destruction <simgrid::s4u::Disk::on_this_destruction_cb>`
    :cpp:func:`Disk::on_onoff <simgrid::s4u::Disk::on_onoff_cb>`
    :cpp:func:`Disk::on_this_onoff <simgrid::s4u::Disk::on_this_onoff_cb>`
    :cpp:func:`Disk::on_read_bandwidth_change <simgrid::s4u::Disk::on_read_bandwidth_change_cb>`
    :cpp:func:`Disk::on_this_read_bandwidth_change <simgrid::s4u::Disk::on_this_read_bandwidth_change_cb>`
    :cpp:func:`Disk::on_write_bandwidth_change <simgrid::s4u::Disk::on_write_bandwidth_change_cb>`
    :cpp:func:`Disk::on_this_write_bandwidth_change <simgrid::s4u::Disk::on_this_write_bandwidth_change_cb>`
    :cpp:func:`Disk::on_io_state_change <simgrid::s4u::Disk::on_io_state_change_cb>`
  - :cpp:func:`Host::on_creation <simgrid::s4u::Host::on_creation_cb>`
    :cpp:func:`Host::on_destruction <simgrid::s4u::Host::on_destruction_cb>`
    :cpp:func:`Host::on_this_destruction <simgrid::s4u::Host::on_this_destruction_cb>`
    :cpp:func:`Host::on_onoff <simgrid::s4u::Host::on_onoff_cb>`
    :cpp:func:`Host::on_this_onoff <simgrid::s4u::Host::on_this_onoff_cb>`
    :cpp:func:`Host::on_speed_change <simgrid::s4u::Host::on_speed_change_cb>`
    :cpp:func:`Host::on_this_speed_change <simgrid::s4u::Host::on_this_speed_change_cb>`
    :cpp:func:`Host::on_exec_state_change <simgrid::s4u::Host::on_exec_state_change_cb>`
  - :cpp:func:`Link::on_creation <simgrid::s4u::Link::on_creation_cb>`
    :cpp:func:`Link::on_destruction <simgrid::s4u::Link::on_destruction_cb>`
    :cpp:func:`Link::on_this_destruction <simgrid::s4u::Link::on_this_destruction_cb>`
    :cpp:func:`Link::on_onoff <simgrid::s4u::Link::on_onoff_cb>`
    :cpp:func:`Link::on_this_onoff <simgrid::s4u::Link::on_this_onoff_cb>`
    :cpp:func:`Link::on_bandwidth_change <simgrid::s4u::Link::on_bandwidth_change_cb>`
    :cpp:func:`Link::on_this_bandwidth_change <simgrid::s4u::Link::on_this_bandwidth_change_cb>`
    :cpp:func:`Link::on_communication_state_change <simgrid::s4u::Link::on_communication_state_change_cb>`

  - :cpp:func:`NetZone::on_creation <simgrid::s4u::NetZone::on_creation_cb>`
    :cpp:func:`NetZone::on_seal <simgrid::s4u::NetZone::on_seal_cb>`
  - :cpp:func:`VirtualMachine::on_start <simgrid::s4u::VirtualMachine::on_start_cb>`
    :cpp:func:`VirtualMachine::on_this_start <simgrid::s4u::VirtualMachine::on_this_start_cb>`
    :cpp:func:`VirtualMachine::on_started <simgrid::s4u::VirtualMachine::on_started_cb>`
    :cpp:func:`VirtualMachine::on_this_started <simgrid::s4u::VirtualMachine::on_this_started_cb>`
    :cpp:func:`VirtualMachine::on_suspend <simgrid::s4u::VirtualMachine::on_suspend_cb>`
    :cpp:func:`VirtualMachine::on_this_suspend <simgrid::s4u::VirtualMachine::on_this_suspend_cb>`
    :cpp:func:`VirtualMachine::on_resume <simgrid::s4u::VirtualMachine::on_resume_cb>`
    :cpp:func:`VirtualMachine::on_this_resume <simgrid::s4u::VirtualMachine::on_this_resume_cb>`
    :cpp:func:`VirtualMachine::on_migration_start <simgrid::s4u::VirtualMachine::on_migration_start_cb>`
    :cpp:func:`VirtualMachine::on_this_migration_start <simgrid::s4u::VirtualMachine::on_this_migration_start_cb>`
    :cpp:func:`VirtualMachine::on_migration_end <simgrid::s4u::VirtualMachine::on_migration_end_cb>`
    :cpp:func:`VirtualMachine::on_this_migration_end <simgrid::s4u::VirtualMachine::on_this_migration_end_cb>`

- In activities:

  - :cpp:func:`Activity::on_veto <simgrid::s4u::Activity::on_veto_cb>`
    :cpp:func:`Activity::on_this_veto <simgrid::s4u::Activity::on_this_veto_cb>`
    :cpp:func:`Activity::on_start <simgrid::s4u::Activity::on_start_cb>`
    :cpp:func:`Activity::on_this_start <simgrid::s4u::Activity::on_this_start_cb>`
    :cpp:func:`Activity::on_suspend <simgrid::s4u::Activity::on_suspend_cb>`
    :cpp:func:`Activity::on_this_suspend <simgrid::s4u::Activity::on_this_suspend_cb>`
    :cpp:func:`Activity::on_resume <simgrid::s4u::Activity::on_resume_cb>`
    :cpp:func:`Activity::on_this_resume <simgrid::s4u::Activity::on_this_resume_cb>`
    :cpp:func:`Activity::on_completion <simgrid::s4u::Activity::on_completion_cb>`
    :cpp:func:`Activity::on_this_completion <simgrid::s4u::Activity::on_this_completion_cb>`
  - :cpp:func:`Comm::on_send <simgrid::s4u::Comm::on_send_cb>`
    :cpp:func:`Comm::on_recv <simgrid::s4u::Comm::on_recv_cb>`

Existing Plugins
****************

Only the major plugins are described here. Please check in src/plugins
to explore the other ones.

.. _plugin_host_energy:

Host Energy
===========

.. doxygengroup:: plugin_host_energy



.. _plugin_link_energy:

Link Energy
===========

.. doxygengroup:: plugin_link_energy

.. _plugin_link_energy_wifi:

WiFi Energy
===========

.. doxygengroup:: plugin_link_energy_wifi



.. _plugin_host_load:

Host Load
=========

.. doxygengroup:: plugin_host_load

.. _plugin_filesystem:

File System
===========

.. doxygengroup:: plugin_filesystem

.. _plugin_battery:

Battery
=======

.. doxygengroup:: plugin_battery

.. _plugin_solar_panel:

Solar Panel
===========

.. doxygengroup:: plugin_solar_panel

.. _plugin_chiller:

Chiller
=======

.. doxygengroup:: plugin_chiller

..  LocalWords:  SimGrid
