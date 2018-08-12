"""Module containing NIC class unit tests."""

import unittest

import mock
from baseline import Baseline

from .. import nic
from ..enums.nic_adapter_type import NicAdapterType
from ..enums.nic_availability import NicAvailability
from ..enums.nic_net_connection_status import NicNetConnectionStatus
from ..enums.nic_config_manager_error_code import NicConfigManagerErrorCode


# pylint: disable=too-many-public-methods, unused-argument, invalid-name
class TestNic(unittest.TestCase):

    """Execute NIC class unit tests."""

    # pylint: disable=no-self-argument, line-too-long
    def _mock_check_output(args):
        command = ' '.join(args)
        win32_networkadapter_base_attribute_cmd = 'wmic path win32_networkadapter where index=0 get '
        win32_networkadapter_base_method_cmd = 'wmic path win32_networkadapter where index=0 call '
        win32_networkadapterconfiguration_base_attribute_cmd = 'wmic path win32_networkadapterconfiguration where index=0 get '
        wmic_responses = {
            win32_networkadapter_base_attribute_cmd + 'AdapterTypeID': 'AdapterType\n0',
            win32_networkadapter_base_attribute_cmd + 'Availability': 'Availability\n3',
            win32_networkadapter_base_attribute_cmd + 'Caption': 'Caption\n[00000000] Dummy Adapter',
            win32_networkadapter_base_attribute_cmd + 'ConfigManagerErrorCode': 'ConfigManagerErrorCode\n0',
            win32_networkadapter_base_attribute_cmd + 'ConfigManagerUserConfig': 'ConfigManagerUserConfig\nFALSE',
            win32_networkadapter_base_attribute_cmd + 'Description': 'Description\nDummy Adapter',
            win32_networkadapter_base_attribute_cmd + 'DeviceID': 'DeviceID\n0',
            win32_networkadapter_base_attribute_cmd + 'ErrorCleared': 'ErrorCleared\nTRUE',
            win32_networkadapter_base_attribute_cmd + 'ErrorDescription': 'ErrorDescription\nDummy Error',
            win32_networkadapter_base_attribute_cmd + 'GUID': 'GUID\n{ABCDEFGH-IJKL-MNOP-QRST-UVWXYZ01234}',
            win32_networkadapter_base_attribute_cmd + 'Installed': 'Installed\nTRUE',
            win32_networkadapter_base_attribute_cmd + 'InterfaceIndex': 'InterfaceIndex\n1',
            win32_networkadapter_base_attribute_cmd + 'LastErrorCode': 'LastErrorCode\n0',
            win32_networkadapter_base_attribute_cmd + 'MACAddress': 'MACAddress\n00:00:00:00:00:00',
            win32_networkadapter_base_attribute_cmd + 'Manufacturer': 'NetConnectionID\nAcme Corporation',
            win32_networkadapter_base_attribute_cmd + 'MaxNumberControlled': 'MaxNumberControlled\n0',
            win32_networkadapter_base_attribute_cmd + 'Name': 'Name\nAcme 1234 Gigabit Network Connection',
            win32_networkadapter_base_attribute_cmd + 'NetConnectionID': 'NetConnectionID\nLocal Area Connection 0',
            win32_networkadapter_base_attribute_cmd + 'NetConnectionStatus': 'NetConnectionStatus\n2',
            win32_networkadapter_base_attribute_cmd + 'PhysicalAdapter': 'Speed\nTRUE',
            win32_networkadapter_base_attribute_cmd + 'PNPDeviceID': 'PNPDeviceID\nPCI\\DUMMY_STUFF\\0123456789',
            win32_networkadapter_base_attribute_cmd + 'PowerManagementSupported': 'PowerManagementSupported\nTRUE',
            win32_networkadapter_base_attribute_cmd + 'ProductName': 'ProductName\nDummy Adapter',
            win32_networkadapter_base_attribute_cmd + 'ServiceName': 'ServiceName\ndummyservice',
            win32_networkadapter_base_attribute_cmd + 'Speed': 'Speed\n1000000000',
            win32_networkadapter_base_attribute_cmd + 'SystemCreationClassName': 'SystemCreationClassName\nWin32_ComputerSystem',
            win32_networkadapter_base_attribute_cmd + 'SystemName': 'SystemName\nTESTPC',
			win32_networkadapter_base_attribute_cmd + 'TimeOfLastReset': 'TimeOfLastReset\n20180131121234.123456-789',
            win32_networkadapterconfiguration_base_attribute_cmd + 'ArpAlwaysSourceRoute': 'ArpAlwaysSourceRoute\nFALSE',
            win32_networkadapterconfiguration_base_attribute_cmd + 'ArpUseEtherSNAP': 'ArpUseEtherSNAP\nFALSE',
            win32_networkadapterconfiguration_base_attribute_cmd + 'DatabasePath': 'DatabasePath\n%SystemRoot%\\System32\\drivers\\etc',
            win32_networkadapterconfiguration_base_attribute_cmd + 'DHCPEnabled': 'DHCPEnabled\nTRUE',
            win32_networkadapterconfiguration_base_attribute_cmd + 'IPAddress': 'IPAddress\n\n{"192.168.0.2", "0:0:0:0:0:0:0:1"}',
            win32_networkadapter_base_method_cmd + 'Disable': 'Method execution successful.\nOut Parameters:\nInstance of __PARAMETERS\n{\n       ReturnValue = 5;\n};',
            win32_networkadapter_base_method_cmd + 'Enable': 'Method execution successful.\nOut Parameters:\nInstance of __PARAMETERS\n{\n       ReturnValue = 5;\n};',
        }
        return wmic_responses[command]

    # pylint: disable=no-self-argument, line-too-long
    def _mock_null_atr(args):
        command = ' '.join(args)
        win32_networkadapter_base_attribute_cmd = 'wmic path win32_networkadapter where index=0 get '
        win32_networkadapterconfiguration_base_attribute_cmd = 'wmic path win32_networkadapterconfiguration where index=0 get '
        wmic_responses = {
            win32_networkadapter_base_attribute_cmd + 'Name': 'MockNull\n',
            win32_networkadapterconfiguration_base_attribute_cmd + 'IPAddress': 'MockNull\n',
        }
        return wmic_responses[command]

    # pylint: disable=no-self-argument, line-too-long
    def _mock_call(args, stdout):
        netsh_base_cmd = 'netsh interface ipv4 '
        netsh_responses = {
            netsh_base_cmd + 'add dnsserver name="Local Area Connection 0" 8.8.8.8': '0',
            netsh_base_cmd + 'set address name="Local Area Connection 0" source=dhcp': '0',
            netsh_base_cmd + 'set address name="Local Area Connection 0" static 192.168.0.2 255.255.255.0 192.168.0.1': '0',
        }
        return netsh_responses[args]

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def setUp(self, mocked_check_output):  # pylint: disable=arguments-differ
        """Instantiate a NIC."""
        self.test_nic = nic.Nic(index=0)

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_adapter_type(self, mocked_check_output):
        """Test adapter_type property of the Nic class."""
        self.assertEqual(self.test_nic.property.adapter_type, NicAdapterType(0))

    @mock.patch('subprocess.call', side_effect=_mock_call)
    def test_add_dns_server(self, mocked_check_output):
        """Test add_dns_server method of the Nic class."""
        self.assertEqual(str(self.test_nic.method.add_dns_server('8.8.8.8')), Baseline("""0"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_arp_always_source_route(self, mocked_check_output):
        """Test arp_always_source_route property of the Nic class."""
        self.assertFalse(self.test_nic.property.arp_always_source_route)

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_arp_use_ether_snap(self, mocked_check_output):
        """Test arp_use_ether_snap property of the Nic class."""
        self.assertFalse(self.test_nic.property.arp_use_ether_snap)
    
    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_availability(self, mocked_check_output):
        """Test availability property of the Nic class."""
        self.assertEqual(self.test_nic.property.availability, NicAvailability(3))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_caption(self, mocked_check_output):
        """Test caption property of the Nic class."""
        self.assertEqual(self.test_nic.property.caption,
                         Baseline("""[00000000] Dummy Adapter"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_config_manager_error_code(self, mocked_check_output):
        """Test config_manager_error_code property of the Nic class."""
        self.assertEqual(self.test_nic.property.config_manager_error_code,
                         NicConfigManagerErrorCode(0))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_config_manager_user_config(self, mocked_check_output):
        """Test config_manager_user_config property of the Nic class."""
        self.assertFalse(self.test_nic.property.config_manager_user_config)

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_database_path(self, mocked_check_output):
        """Test database_path property of the Nic class."""
        self.assertEqual(self.test_nic.property.database_path,
                         Baseline("""%SystemRoot%\\System32\\drivers\\etc"""))

    def test_dunder_repr(self):
        """Test repr magic method property of the NIC class."""
        self.assertEqual(repr(self.test_nic),
                         Baseline("""<'win_nic.nic.Nic(index=0)'>"""))

    def test_dunder_repr_method(self):
        """Test repr magic method property of the NIC class."""
        self.assertEqual(repr(self.test_nic.method),
                         Baseline("""<'win_nic.nic_method.NicMethod(wmic_index=0)'>"""))

    def test_dunder_repr_property(self):
        """Test repr magic method property of the Nic class."""
        self.assertEqual(repr(self.test_nic.property),
                         Baseline("""<'win_nic.nic_property.NicProperty(index=0)'>"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_dunder_str(self, mocked_check_output):
        """Test string magic method property of the Nic class."""
        self.assertEqual(str(self.test_nic), Baseline("""[00000000] Dummy Adapter"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_dunder_str_method(self, mocked_check_output):
        """Test string magic method property of the Nic class."""
        self.assertEqual(str(self.test_nic.method),
                         Baseline("""[00000000] Dummy Adapter Method Handler"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_dunder_str_property(self, mocked_check_output):
        """Test string magic method property of the Nic class."""
        self.assertEqual(str(self.test_nic.property),
                         Baseline("""[00000000] Dummy Adapter Property Handler"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_description(self, mocked_check_output):
        """Test description property of the Nic class."""
        self.assertEqual(self.test_nic.property.description,
                         Baseline("""Dummy Adapter"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_device_id(self, mocked_check_output):
        """Test device_id property of the Nic class."""
        self.assertEqual(self.test_nic.property.device_id, Baseline("""0"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_dhcp_enabled(self, mocked_check_output):
        """Test installed property of the Nic class."""
        self.assertTrue(self.test_nic.property.dhcp_enabled)

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_disable(self, mocked_check_output):
        """Test disable method of the Nic class."""
        self.assertEqual(str(self.test_nic.method.disable()), Baseline("""5"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_enable(self, mocked_check_output):
        """Test enable method of the Nic class."""
        self.assertEqual(str(self.test_nic.method.enable()), Baseline("""5"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_enabled_ctrl_panel(self, mocked_check_output):
        """Test enabled_ctrl_panel method of the Nic class."""
        self.assertTrue(self.test_nic.property.enabled_ctrl_panel)

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_error_cleared(self, mocked_check_output):
        """Test error_cleared property of the Nic class."""
        self.assertTrue(self.test_nic.property.error_cleared)

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_error_description(self, mocked_check_output):
        """Test error_description property of the Nic class."""
        self.assertEqual(self.test_nic.property.error_description,
                         Baseline("""Dummy Error"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_guid(self, mocked_check_output):
        """Test guid property of the Nic class."""
        self.assertEqual(self.test_nic.property.guid,
                         Baseline("""{ABCDEFGH-IJKL-MNOP-QRST-UVWXYZ01234}"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_installed(self, mocked_check_output):
        """Test installed property of the Nic class."""
        self.assertTrue(self.test_nic.property.installed)

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_interface_index(self, mocked_check_output):
        """Test interface_index property of the Nic class."""
        self.assertEqual(str(self.test_nic.property.interface_index), Baseline("""1"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_last_error_code(self, mocked_check_output):
        """Test last_error_code property of the Nic class."""
        self.assertEqual(str(self.test_nic.property.last_error_code), Baseline("""0"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_mac_address(self, mocked_check_output):
        """Test mac_address property of the Nic class."""
        self.assertEqual(self.test_nic.property.mac_address,
                         Baseline("""00:00:00:00:00:00"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_manufacturer(self, mocked_check_output):
        """Test manufacturer property of the Nic class."""
        self.assertEqual(self.test_nic.property.manufacturer,
                         Baseline("""Acme Corporation"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_max_number_controlled(self, mocked_check_output):
        """Test max_number_controlled property of the Nic class."""
        self.assertEqual(str(self.test_nic.property.max_number_controlled),
                         Baseline("""0"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_name(self, mocked_check_output):
        """Test name property of the Nic class."""
        self.assertEqual(self.test_nic.property.name,
                         Baseline("""Acme 1234 Gigabit Network Connection"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_net_connection_id(self, mocked_check_output):
        """Test net_connection_id property of the Nic class."""
        self.assertEqual(self.test_nic.property.net_connection_id,
                         Baseline("""Local Area Connection 0"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_net_connection_status(self, mocked_check_output):
        """Test net_connection_status property of the Nic class."""
        self.assertEqual(self.test_nic.property.net_connection_status,
                         NicNetConnectionStatus(2))

    @mock.patch('subprocess.check_output', side_effect=_mock_null_atr)
    def test_null_attribute_exception(self, mocked_check_output):
        """Test null attribute exception handling of the Nic class."""
        # pylint: disable=pointless-statement
        with self.assertRaises(AttributeError):
            self.test_nic.property.name
        with self.assertRaises(AttributeError):
            self.test_nic.property.ip_addresses

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_ip_addresses(self, mocked_check_output):
        """Test ip_addresses property of the Nic class."""
        self.assertEqual(str(self.test_nic.property.ip_addresses),
                         Baseline("""['192.168.0.2', '0:0:0:0:0:0:0:1']"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_pnp_device_id(self, mocked_check_output):
        """Test pnp_device_id property of the Nic class."""
        self.assertEqual(self.test_nic.property.pnp_device_id,
                         Baseline("""PCI\\DUMMY_STUFF\\0123456789"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_physical_adapter(self, mocked_check_output):
        """Test physical_adapter property of the Nic class."""
        self.assertTrue(self.test_nic.property.physical_adapter)

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_power_management_supported(self, mocked_check_output):
        """Test power_management_supported property of the Nic class."""
        self.assertTrue(self.test_nic.property.power_management_supported)

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_product_name(self, mocked_check_output):
        """Test product_name property of the Nic class."""
        self.assertEqual(self.test_nic.property.product_name,
                         Baseline("""Dummy Adapter"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_service_name(self, mocked_check_output):
        """Test service_name property of the Nic class."""
        self.assertEqual(self.test_nic.property.service_name,
                         Baseline("""dummyservice"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_speed(self, mocked_check_output):
        """Test speed property of the Nic class."""
        self.assertEqual(str(self.test_nic.property.speed), Baseline("""1000000000"""))

    @mock.patch('subprocess.call', side_effect=_mock_call)
    def test_set_static_address(self, mocked_check_output):
        """Test set_static_address method of the Nic class."""
        self.assertEqual(str(self.test_nic.method.set_static_address('192.168.0.2', '255.255.255.0', '192.168.0.1')), Baseline("""0"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_system_creation_class_name(self, mocked_check_output):
        """Test system_creation_class_name property of the Nic class."""
        self.assertEqual(self.test_nic.property.system_creation_class_name,
                         Baseline("""Win32_ComputerSystem"""))
        
    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_system_name(self, mocked_check_output):
        """Test system_name property of the Nic class."""
        self.assertEqual(self.test_nic.property.system_name,
                         Baseline("""TESTPC"""))

    @mock.patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_time_of_last_reset(self, mocked_check_output):
        """Test time_of_last_reset property of the Nic class."""
        self.assertEqual(str(self.test_nic.property.time_of_last_reset),
                         Baseline("""2018-01-31 12:12:34"""))

    @mock.patch('subprocess.call', side_effect=_mock_call)
    def test_use_dhcp(self, mocked_check_output):
        """Test set_static_address method of the Nic class."""
        self.assertEqual(str(self.test_nic.method.use_dhcp()), Baseline("""0"""))
