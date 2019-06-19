"""Module containing Nic class."""

import re

from enum import EnumMeta

from win_nic.enums.nic_adapter_type import NicAdapterType
from win_nic.enums.nic_availability import NicAvailability
from win_nic.enums.nic_config_manager_error_code import NicConfigManagerErrorCode
from win_nic.enums.nic_net_connection_status import NicNetConnectionStatus

from win_nic._utils import parse_array, run_netsh_command, run_wmic_command


class Nic:

    """Windows network interface card (NIC) class.

    :param int index: index number of the network adapter (as stored in the system registry)

    """

    # Store adapter properties (accessible as attributes) as a dictionary mapping the
    # attribute name to a tuple of Windows name, Windows class, and Python type.
    _wmic_properties = {
        'adapter_type': ('AdapterTypeID', 'win32_networkadapter', NicAdapterType),
        'availability': ('Availability', 'win32_networkadapter', NicAvailability),
        'caption': ('Caption', 'win32_networkadapter', str),
        'config_manager_error_code': ('ConfigManagerErrorCode', 'win32_networkadapter', NicConfigManagerErrorCode),
        'config_manager_user_config': ('ConfigManagerUserConfig', 'win32_networkadapter', bool),
        'description': ('Description', 'win32_networkadapter', str),
        'device_id': ('DeviceID', 'win32_networkadapter', str),
        'error_cleared': ('ErrorCleared', 'win32_networkadapter', bool),
        'error_description': ('ErrorDescription', 'win32_networkadapter', str),
        'guid': ('GUID', 'win32_networkadapter', str),
        'installed': ('Installed', 'win32_networkadapter', bool),
        'interface_index': ('InterfaceIndex', 'win32_networkadapter', int),
        '_ip_address_raw': ('IPAddress', 'win32_networkadapterconfiguration', str),
        'last_error_code': ('LastErrorCode', 'win32_networkadapter', int),
        'mac_address': ('MACAddress', 'win32_networkadapter', str),
        'manufacturer': ('Manufacturer', 'win32_networkadapter', str),
        'name': ('Name', 'win32_networkadapter', str),
        'net_connection_id': ('NetConnectionID', 'win32_networkadapter', str),
        'net_connection_status': ('NetConnectionStatus', 'win32_networkadapter', NicNetConnectionStatus),
        'physical_adapter': ('PhysicalAdapter', 'win32_networkadapter', bool),
        'pnp_device_id': ('PNPDeviceID', 'win32_networkadapter', str),
        'power_management_supported': ('PowerManagementSupported', 'win32_networkadapter', bool),
        'product_name': ('ProductName', 'win32_networkadapter', str),
        'service_name': ('ServiceName', 'win32_networkadapter', str),
        'speed': ('Speed', 'win32_networkadapter', int),
    }

    def __init__(self, index):
        self.index = index

    def __getattr__(self, item):
        if item not in self._wmic_properties:
            raise AttributeError(f"'Nic' object has no attribute '{item}'")

        windows_name = self._wmic_properties[item][0]
        windows_class = self._wmic_properties[item][1]
        python_type = self._wmic_properties[item][2]

        wmic_resp_list = run_wmic_command([
            'path', windows_class, 'where', f'index={self.index}', 'get', windows_name])

        try:
            wmic_resp = wmic_resp_list[0]
        except IndexError:
            raise AttributeError(f"wmic did not return value for attribute '{windows_name}'")

        if isinstance(python_type, EnumMeta):
            # Convert response to integer before casting to enumeration.
            wmic_resp = int(wmic_resp)

        if python_type == bool:
            retval = wmic_resp == 'TRUE'
        else:
            retval = python_type(wmic_resp)

        return retval

    def __setattr__(self, key, value):
        if key in self._wmic_properties:
            raise AttributeError(f"'Nic' attribute '{key}' is not settable")

        object.__setattr__(self, key, value)

    def __dir__(self):
        return list(self.__dict__) + list(self._wmic_properties)

    def __repr__(self):
        return "<'win_nic.Nic(index=" + str(self.index) + ")'>"

    def __str__(self):
        return self.caption

    def _call_win32_networkadapter(self, call):
        wmic_args = ['path', 'win32_networkadapter', 'where',
                     'index={}'.format(self.index), 'call', call]
        raw_response = '\n'.join(run_wmic_command(wmic_args))
        wmic_return_rx = re.compile(r'ReturnValue = (\d+);')
        return int(re.findall(wmic_return_rx, raw_response)[0])

    def add_dns_server(self, dns_server):
        """Add a DNS server entry.

        :param str dns_server: DNS server address

        .. note:: To add a DNS entry, the Python process must be running as administrator.

        """
        return run_netsh_command('add dnsserver name="' + self.net_connection_id + '" ' + dns_server)

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

    @property
    def enabled_ctrl_panel(self):
        """Check if NIC is enabled (as it appears in Control Panel).

        :returns: True if enabled, false if disabled.
        :rtype: bool

        """
        return self.net_connection_status != NicNetConnectionStatus.DISCONNECTED

    @property
    def ip_addresses(self):
        """Get the NetConnectionStatus property of Win32_NetworkAdapter.

        :returns: NetConnectionStatus
        :rtype: str[]

        """
        return parse_array(self._ip_address_raw)

    def set_static_address(self, ip_addr, subnet_mask, gateway):
        """Set a static IP address configuration.

        :param str ip_addr: static IP adress
        :param str subnet_mask: static subnet mask
        :param str gateway: static default gateway

        .. note:: To set a static address, the Python process must be running as administrator.

        """
        netsh_args = ('set address name="' + self.net_connection_id + '" static ' + ip_addr + ' '
                      + subnet_mask + ' ' + gateway)
        return run_netsh_command(netsh_args)

    def use_dhcp(self):
        """Use DHCP for IP address configuration.

        .. note:: To set a static address, the Python process must be running as administrator.

        """
        netsh_args = ('set address name="' + self.net_connection_id + '" source=dhcp')
        return run_netsh_command(netsh_args)
