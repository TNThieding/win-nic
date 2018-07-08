

import datetime

import win_nic.utils as utils
from win_nic.enums.nic_adapter_type import NicAdapterType
from win_nic.enums.nic_availability import NicAvailability
from win_nic.enums.nic_config_manager_error_code import NicConfigManagerErrorCode
from win_nic.enums.nic_net_connection_status import NicNetConnectionStatus


# pylint: disable=missing-docstring,too-many-public-methods
class NicProperty(object):

    NULL_ATR_MSG = "NIC does not currently have attribute data for {}!"

    def __init__(self, index):
        self.index = index

    def __repr__(self):
        return "<'win_nic.nic_property.NicProperty(index=" + str(self.index) + ")'>"

    def __str__(self):
        return self.caption + " Property Handler"

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
        return NicAdapterType(int(self._get_atr_win32_networkadapter('AdapterTypeID')))

    @property
    def arp_always_source_route(self):
        return self._get_atr_win32_networkadapterconfiguration('ArpAlwaysSourceRoute') == 'TRUE'

    @property
    def arp_use_ether_snap(self):
        return self._get_atr_win32_networkadapterconfiguration('ArpUseEtherSNAP') == 'TRUE'

    @property
    def availability(self):
        return NicAvailability(int(self._get_atr_win32_networkadapter('Availability')))

    @property
    def caption(self):
        return self._get_atr_win32_networkadapter('Caption')

    @property
    def config_manager_error_code(self):
        return NicConfigManagerErrorCode(
            int(self._get_atr_win32_networkadapter('ConfigManagerErrorCode')))

    @property
    def config_manager_user_config(self):
        return self._get_atr_win32_networkadapter('ConfigManagerUserConfig') == 'TRUE'

    @property
    def database_path(self):
        return self._get_atr_win32_networkadapterconfiguration('DatabasePath')

    @property
    def description(self):
        return self._get_atr_win32_networkadapter('Description')

    @property
    def device_id(self):
        return self._get_atr_win32_networkadapter('DeviceID')

    @property
    def enabled_ctrl_panel(self):
        return self.net_connection_status != NicNetConnectionStatus.DISCONNECTED

    @property
    def error_cleared(self):
        return self._get_atr_win32_networkadapter('ErrorCleared') == 'TRUE'

    @property
    def error_description(self):
        return self._get_atr_win32_networkadapter('ErrorDescription')

    @property
    def guid(self):
        return self._get_atr_win32_networkadapter('GUID')

    @property
    def installed(self):
        return self._get_atr_win32_networkadapter('Installed') == 'TRUE'

    @property
    def interface_index(self):
        return int(self._get_atr_win32_networkadapter('InterfaceIndex'))

    @property
    def ip_addresses(self):
        ip_array = self._get_atr_win32_networkadapterconfiguration('IPAddress')
        return utils.parse_array(ip_array)

    @property
    def last_error_code(self):
        return int(self._get_atr_win32_networkadapter('LastErrorCode'))

    @property
    def mac_address(self):
        return self._get_atr_win32_networkadapter('MACAddress')

    @property
    def manufacturer(self):
        return self._get_atr_win32_networkadapter('Manufacturer')

    @property
    def max_number_controlled(self):
        return int(self._get_atr_win32_networkadapter('MaxNumberControlled'))

    @property
    def name(self):
        return self._get_atr_win32_networkadapter('Name')

    @property
    def net_connection_id(self):
        return self._get_atr_win32_networkadapter('NetConnectionID')

    @property
    def net_connection_status(self):
        return NicNetConnectionStatus(
            int(self._get_atr_win32_networkadapter('NetConnectionStatus')))

    @property
    def physical_adapter(self):
        return self._get_atr_win32_networkadapter('PhysicalAdapter') == 'TRUE'

    @property
    def pnp_device_id(self):
        return self._get_atr_win32_networkadapter('PNPDeviceID')

    @property
    def power_management_supported(self):
        return self._get_atr_win32_networkadapter('PowerManagementSupported') == 'TRUE'

    @property
    def product_name(self):
        return self._get_atr_win32_networkadapter('ProductName')

    @property
    def service_name(self):
        return self._get_atr_win32_networkadapter('ServiceName')

    @property
    def speed(self):
        return int(self._get_atr_win32_networkadapter('Speed'))

    @property
    def system_creation_class_name(self):
        return self._get_atr_win32_networkadapter('SystemCreationClassName')

    @property
    def system_name(self):
        return self._get_atr_win32_networkadapter('SystemName')

    @property
    def time_of_last_reset(self):
		return utils.parse_datetime(raw_datetime = self._get_atr_win32_networkadapter('TimeOfLastReset'))

