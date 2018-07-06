"""Module containing NicMethod class."""

import re

import win_nic.utils as utils


class NicMethod(object):

    """Windows network interface card (NIC) method class.

    :param int index: Index number of the network adapter, as stored in the system registry.

    """

    def __init__(self, wmic_index, netsh_name, wmic_caption):
        self.wmic_index = wmic_index
        self.netsh_name = netsh_name
        self.wmic_caption = wmic_caption

    def __repr__(self):
        return "<'win_nic.nic_method.NicMethod(wmic_index=" + str(self.wmic_index) + ")'>"

    def __str__(self):
        return self.wmic_caption + " Method Handler"

    def _call_win32_networkadapter(self, call):
        wmic_args = ['path', 'win32_networkadapter', 'where',
                     'index={}'.format(self.wmic_index), 'call', call]
        raw_response = '\n'.join(utils.run_wmic_command(wmic_args))
        wmic_return_rx = re.compile(r'ReturnValue = (\d+);')
        return int(re.findall(wmic_return_rx, raw_response)[0])

    def add_dns_server(self, dns_server):
        """Add a DNS server entry.

        :param str dns_server: DNS Server Address

        .. note:: To add a DNS entry, the Python process must be running as administrator.
        """
        netsh_args = ('add dnsserver name="' + self.netsh_name + '" ' + dns_server)
        return utils.run_netsh_command(netsh_args)

    def disable(self):
        """Call the Disable method of Win32_NetworkAdapter.

        .. note:: To disable a NIC, the Python process must be running as administrator.
        """
        return self._call_win32_networkadapter('Disable')

    def enable(self):
        """Call the Enable method of Win32_NetworkAdapter.

        .. note:: To enable a NIC, the Python process must be running as administrator.
        """
        return self._call_win32_networkadapter('Enable')

    def set_static_address(self, ip_addr, subnet_mask, gateway):
        """Set a static IP address configuration.

        :param str ip_addr: Static IP Address
        :param str subnet_mask: Static Subnet Mask
        :param str gateway: Static Default Gateway

        .. note:: To set a static address, the Python process must be running as administrator.
        """
        netsh_args = ('set address name="' + self.netsh_name + '" static ' + ip_addr + ' '
                      + subnet_mask + ' ' + gateway)
        return utils.run_netsh_command(netsh_args)

    def use_dhcp(self):
        """Use DHCP for IP address configuration.

        .. note:: To set a static address, the Python process must be running as administrator.
        """
        netsh_args = ('set address name="' + self.netsh_name + '" source=dhcp')
        return utils.run_netsh_command(netsh_args)
