"""Module containing NicProperty class."""

import win_nic._utils as utils
from win_nic.enums.nic_adapter_type import NicAdapterType
from win_nic.enums.nic_availability import NicAvailability
from win_nic.enums.nic_config_manager_error_code import NicConfigManagerErrorCode
from win_nic.enums.nic_net_connection_status import NicNetConnectionStatus


# pylint: disable=too-many-public-methods
class NicProperty:

    """Windows network interface card (NIC) property class.

    :param int index: index number of the network adapter (as stored in the system registry)

    """

    NULL_ATR_MSG = "undefined NIC attribute {}"

    def __init__(self, index):
        self.index = index

    def _get_atr_win32_networkadapterconfiguration(self, attribute):
        wmic_args = ['path', 'win32_networkadapterconfiguration', 'where',
                     'index={}'.format(self.index), 'get', attribute]
        try:
            return utils.run_wmic_command(wmic_args)[0]
        except IndexError:
            raise AttributeError(self.NULL_ATR_MSG.format(attribute))

    def _get_atr_win32_networkadapter(self, attribute):
        wmic_args = ['path', 'win32_networkadapter', 'where',
                     'index={}'.format(self.index), 'get', attribute]
        try:
            return utils.run_wmic_command(wmic_args)[0]
        except IndexError:
            raise AttributeError(self.NULL_ATR_MSG.format(attribute))

    @property
    def adapter_type(self):
        """Get the AdapterType property of Win32_NetworkAdapter.

        :returns: AdapterType
        :rtype: win_nic.enums.nic_adapter_type.NicAdapterType

        """
        return NicAdapterType(int(self._get_atr_win32_networkadapter('AdapterTypeID')))

    @property
    def availability(self):
        """Get the Availability property of Win32_NetworkAdapter.

        :returns: Availability
        :rtype: win_nic.enums.nic_availability.NicAvailability

        """
        return NicAvailability(int(self._get_atr_win32_networkadapter('Availability')))

    @property
    def caption(self):
        """Get the Caption property of Win32_NetworkAdapter.

        :returns: Caption
        :rtype: str

        """
        return self._get_atr_win32_networkadapter('Caption')

    @property
    def config_manager_error_code(self):
        """Get the ConfigManagerErrorCode property of Win32_NetworkAdapter.

        :returns: ConfigManagerErrorCode
        :rtype: win_nic.enums.nic_config_manager_error_code.NicConfigManagerErrorCode

        """
        return NicConfigManagerErrorCode(
            int(self._get_atr_win32_networkadapter('ConfigManagerErrorCode')))

    @property
    def config_manager_user_config(self):
        """Get the ConfigManagerUserConfig property of Win32_NetworkAdapter.

        :returns: ConfigManagerUserConfig
        :rtype: bool

        """
        return self._get_atr_win32_networkadapter('ConfigManagerUserConfig') == 'TRUE'

    @property
    def description(self):
        """Get the Description property of Win32_NetworkAdapter.

        :returns: Description
        :rtype: str

        """
        return self._get_atr_win32_networkadapter('Description')

    @property
    def device_id(self):
        """Get the DeviceID property of Win32_NetworkAdapter.

        :returns: DeviceID
        :rtype: str

        """
        return self._get_atr_win32_networkadapter('DeviceID')

    @property
    def enabled_ctrl_panel(self):
        """Check if NIC is enabled (as it appears in Control Panel).

        :returns: True if enabled, false if disabled.
        :rtype: bool

        """
        return self.net_connection_status != NicNetConnectionStatus.DISCONNECTED

    @property
    def error_cleared(self):
        """Get the ErrorCleared property of Win32_NetworkAdapter.

        :returns: ErrorCleared
        :rtype: bool

        """
        return self._get_atr_win32_networkadapter('ErrorCleared') == 'TRUE'

    @property
    def error_description(self):
        """Get the ErrorDescription property of Win32_NetworkAdapter.

        :returns: ErrorDescription
        :rtype: str

        """
        return self._get_atr_win32_networkadapter('ErrorDescription')

    @property
    def guid(self):
        """Get the GUID property of Win32_NetworkAdapter.

        :returns: GUID
        :rtype: str

        """
        return self._get_atr_win32_networkadapter('GUID')

    @property
    def installed(self):
        """Get the Installed property of Win32_NetworkAdapter.

        :returns: Installed
        :rtype: bool

        """
        return self._get_atr_win32_networkadapter('Installed') == 'TRUE'

    @property
    def interface_index(self):
        """Get the InterfaceIndex property of Win32_NetworkAdapter.

        :returns: InterfaceIndex
        :rtype: int

        """
        return int(self._get_atr_win32_networkadapter('InterfaceIndex'))

    @property
    def ip_addresses(self):
        """Get the NetConnectionStatus property of Win32_NetworkAdapter.

        :returns: NetConnectionStatus
        :rtype: str[]

        """
        ip_array = self._get_atr_win32_networkadapterconfiguration('IPAddress')
        return utils.parse_array(ip_array)

    @property
    def last_error_code(self):
        """Get the LastErrorCode property of Win32_NetworkAdapter.

        :returns: LastErrorCode
        :rtype: int

        """
        return int(self._get_atr_win32_networkadapter('LastErrorCode'))

    @property
    def mac_address(self):
        """Get the MACAddress property of Win32_NetworkAdapter.

        :returns: MACAddress
        :rtype: str

        """
        return self._get_atr_win32_networkadapter('MACAddress')

    @property
    def manufacturer(self):
        """Get the Manufacturer property of Win32_NetworkAdapter.

        :returns: Manufacturer
        :rtype: str

        """
        return self._get_atr_win32_networkadapter('Manufacturer')

    @property
    def name(self):
        """Get the Name property of Win32_NetworkAdapter.

        :returns: Name
        :rtype: str

        """
        return self._get_atr_win32_networkadapter('Name')

    @property
    def net_connection_id(self):
        """Get the NetConnectionID property of Win32_NetworkAdapter.

        :returns: NetConnectionID
        :rtype: str

        """
        return self._get_atr_win32_networkadapter('NetConnectionID')

    @property
    def net_connection_status(self):
        """Get the NetConnectionStatus property of Win32_NetworkAdapter.

        :returns: NetConnectionStatus
        :rtype: win_nic.enums.nic_net_connection_status.NicNetConnectionStatus

        """
        return NicNetConnectionStatus(
            int(self._get_atr_win32_networkadapter('NetConnectionStatus')))

    @property
    def physical_adapter(self):
        """Get the PhysicalAdapter property of Win32_NetworkAdapter.

        :returns: PhysicalAdapter
        :rtype: bool

        """
        return self._get_atr_win32_networkadapter('PhysicalAdapter') == 'TRUE'

    @property
    def pnp_device_id(self):
        """Get the PNPDeviceID property of Win32_NetworkAdapter.

        :returns: PNPDeviceID
        :rtype: str

        """
        return self._get_atr_win32_networkadapter('PNPDeviceID')

    @property
    def power_management_supported(self):
        """Get the PowerManagementSupported property of Win32_NetworkAdapter.

        :returns: PowerManagementSupported
        :rtype: bool

        """
        return self._get_atr_win32_networkadapter('PowerManagementSupported') == 'TRUE'

    @property
    def product_name(self):
        """Get the ProductName property of Win32_NetworkAdapter.

        :returns: ProductName
        :rtype: str

        """
        return self._get_atr_win32_networkadapter('ProductName')

    @property
    def service_name(self):
        """Get the ServiceName property of Win32_NetworkAdapter.

        :returns: ServiceName
        :rtype: str

        """
        return self._get_atr_win32_networkadapter('ServiceName')

    @property
    def speed(self):
        """Get the Speed property of Win32_NetworkAdapter.

        :returns: Speed
        :rtype: int

        """
        return int(self._get_atr_win32_networkadapter('Speed'))
