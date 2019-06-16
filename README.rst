#######
win-nic
#######

.. image:: https://gitlab.com/TNThieding/win-nic/badges/master/pipeline.svg
    :target: https://gitlab.com/TNThieding/win-nic/commits/master

.. image:: https://gitlab.com/TNThieding/win-nic/badges/master/coverage.svg
    :target: https://gitlab.com/TNThieding/win-nic/commits/master

.. image:: https://readthedocs.org/projects/win-nic/badge/?version=latest
    :target: https://win-nic.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Interface with network interface cards (NICs) on Windows-based computers. This package heavily
wraps the Windows management instrumentation command-line (WMIC) and the netsh command-line utility
via subprocess calls. No C dependencies or building from source files, just a lightweight and
straightforward wrapper of utilities built into your Windows system.

***********
Quick Start
***********

First, obtain a NIC instance via the ``NetworkAdapters`` class. To do this, instantiate
``NetworkAdapters`` and specify the desired NIC. Specify the target NIC by registry index,
name, or connection ID (control panel name)::

   >>> from win_nic import NetworkAdapters
   >>> this_pc_nics = NetworkAdapters()
   >>> ethernet_nic = this_pc_nics.get_nic(connection_id="Local Area Connection 1")

Now, interface with the NIC instance as needed by getting attributes or calling methods::

   >>> ethernet_nic.property.ip_addresses
   ['192.168.0.2']
   >>> ethernet_nic.net_connection_status
   <NicNetConnectionStatus.CONNECTED: 2>
   >>> ethernet_nic.set_static_address('192.168.0.3', '255.255.255.0', '192.168.0.1')
   0
