"""Module containing NIC class unit tests."""

from unittest import TestCase
from unittest.mock import patch

from baseline import Baseline

from win_nic import Nic
from win_nic.enums.nic_adapter_type import NicAdapterType
from win_nic.enums.nic_availability import NicAvailability
from win_nic.enums.nic_net_connection_status import NicNetConnectionStatus
from win_nic.enums.nic_config_manager_error_code import NicConfigManagerErrorCode


# pylint: disable=too-many-public-methods, unused-argument, invalid-name
class TestNic(TestCase):

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
            win32_networkadapter_base_attribute_cmd + 'Name': 'Name\nAcme 1234 Gigabit Network Connection',
            win32_networkadapter_base_attribute_cmd + 'NetConnectionID': 'NetConnectionID\nLocal Area Connection 0',
            win32_networkadapter_base_attribute_cmd + 'NetConnectionStatus': 'NetConnectionStatus\n2',
            win32_networkadapter_base_attribute_cmd + 'PhysicalAdapter': 'Speed\nTRUE',
            win32_networkadapter_base_attribute_cmd + 'PNPDeviceID': 'PNPDeviceID\nPCI\\DUMMY_STUFF\\0123456789',
            win32_networkadapter_base_attribute_cmd + 'PowerManagementSupported': 'PowerManagementSupported\nTRUE',
            win32_networkadapter_base_attribute_cmd + 'ProductName': 'ProductName\nDummy Adapter',
            win32_networkadapter_base_attribute_cmd + 'Speed': 'Speed\n1000000000',
            win32_networkadapter_base_attribute_cmd + 'ServiceName': 'ServiceName\ndummyservice',
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

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def setUp(self, mocked_check_output):  # pylint: disable=arguments-differ
        """Instantiate a NIC."""
        self.test_nic = Nic(index=0)

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_adapter_type(self, mocked_check_output):
        """Test adapter_type property of the Nic class."""
        self.assertEqual(self.test_nic.adapter_type, NicAdapterType(0))

    @patch('subprocess.call', side_effect=_mock_call)
    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_add_dns_server(self, mocked_check_output, mocked_call_output):
        """Test add_dns_server method of the Nic class."""
        self.assertEqual(str(self.test_nic.add_dns_server('8.8.8.8')), Baseline("""0"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_availability(self, mocked_check_output):
        """Test availability property of the Nic class."""
        self.assertEqual(self.test_nic.availability, NicAvailability(3))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_caption(self, mocked_check_output):
        """Test caption property of the Nic class."""
        self.assertEqual(self.test_nic.caption,
                         Baseline("""[00000000] Dummy Adapter"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_config_manager_error_code(self, mocked_check_output):
        """Test config_manager_error_code property of the Nic class."""
        self.assertEqual(self.test_nic.config_manager_error_code,
                         NicConfigManagerErrorCode(0))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_config_manager_user_config(self, mocked_check_output):
        """Test config_manager_user_config property of the Nic class."""
        self.assertFalse(self.test_nic.config_manager_user_config)

    def test_dunder_repr(self):
        """Test repr magic method property of the NIC class."""
        self.assertEqual(repr(self.test_nic),
                         Baseline("""<'win_nic.Nic(index=0)'>"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_dunder_str(self, mocked_check_output):
        """Test string magic method property of the Nic class."""
        self.assertEqual(str(self.test_nic), Baseline("""[00000000] Dummy Adapter"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_description(self, mocked_check_output):
        """Test description property of the Nic class."""
        self.assertEqual(self.test_nic.description,
                         Baseline("""Dummy Adapter"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_device_id(self, mocked_check_output):
        """Test device_id property of the Nic class."""
        self.assertEqual(self.test_nic.device_id, Baseline("""0"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_disable(self, mocked_check_output):
        """Test disable method of the Nic class."""
        self.assertEqual(str(self.test_nic.disable()), Baseline("""5"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_enable(self, mocked_check_output):
        """Test enable method of the Nic class."""
        self.assertEqual(str(self.test_nic.enable()), Baseline("""5"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_enabled_ctrl_panel(self, mocked_check_output):
        """Test enabled_ctrl_panel method of the Nic class."""
        self.assertTrue(self.test_nic.enabled_ctrl_panel)

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_error_cleared(self, mocked_check_output):
        """Test error_cleared property of the Nic class."""
        self.assertTrue(self.test_nic.error_cleared)

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_error_description(self, mocked_check_output):
        """Test error_description property of the Nic class."""
        self.assertEqual(self.test_nic.error_description,
                         Baseline("""Dummy Error"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_guid(self, mocked_check_output):
        """Test guid property of the Nic class."""
        self.assertEqual(self.test_nic.guid,
                         Baseline("""{ABCDEFGH-IJKL-MNOP-QRST-UVWXYZ01234}"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_installed(self, mocked_check_output):
        """Test installed property of the Nic class."""
        self.assertTrue(self.test_nic.installed)

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_interface_index(self, mocked_check_output):
        """Test interface_index property of the Nic class."""
        self.assertEqual(str(self.test_nic.interface_index), Baseline("""1"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_last_error_code(self, mocked_check_output):
        """Test last_error_code property of the Nic class."""
        self.assertEqual(str(self.test_nic.last_error_code), Baseline("""0"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_mac_address(self, mocked_check_output):
        """Test mac_address property of the Nic class."""
        self.assertEqual(self.test_nic.mac_address,
                         Baseline("""00:00:00:00:00:00"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_manufacturer(self, mocked_check_output):
        """Test manufacturer property of the Nic class."""
        self.assertEqual(self.test_nic.manufacturer,
                         Baseline("""Acme Corporation"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_name(self, mocked_check_output):
        """Test name property of the Nic class."""
        self.assertEqual(self.test_nic.name,
                         Baseline("""Acme 1234 Gigabit Network Connection"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_net_connection_id(self, mocked_check_output):
        """Test net_connection_id property of the Nic class."""
        self.assertEqual(self.test_nic.net_connection_id,
                         Baseline("""Local Area Connection 0"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_net_connection_status(self, mocked_check_output):
        """Test net_connection_status property of the Nic class."""
        self.assertEqual(self.test_nic.net_connection_status,
                         NicNetConnectionStatus(2))

    @patch('subprocess.check_output', side_effect=_mock_null_atr)
    def test_null_attribute_exception(self, mocked_check_output):
        """Test null attribute exception handling of the Nic class."""
        # pylint: disable=pointless-statement
        with self.assertRaises(AttributeError):
            self.test_nic.name
        with self.assertRaises(AttributeError):
            self.test_nic.ip_addresses

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_ip_addresses(self, mocked_check_output):
        """Test ip_addresses property of the Nic class."""
        self.assertEqual(str(self.test_nic.ip_addresses),
                         Baseline("""['192.168.0.2', '0:0:0:0:0:0:0:1']"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_pnp_device_id(self, mocked_check_output):
        """Test pnp_device_id property of the Nic class."""
        self.assertEqual(self.test_nic.pnp_device_id,
                         Baseline("""PCI\\DUMMY_STUFF\\0123456789"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_physical_adapter(self, mocked_check_output):
        """Test physical_adapter property of the Nic class."""
        self.assertTrue(self.test_nic.physical_adapter)

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_power_management_supported(self, mocked_check_output):
        """Test power_management_supported property of the Nic class."""
        self.assertTrue(self.test_nic.power_management_supported)

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_product_name(self, mocked_check_output):
        """Test product_name property of the Nic class."""
        self.assertEqual(self.test_nic.product_name,
                         Baseline("""Dummy Adapter"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_service_name(self, mocked_check_output):
        """Test service_name property of the Nic class."""
        self.assertEqual(self.test_nic.service_name,
                         Baseline("""dummyservice"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_speed(self, mocked_check_output):
        """Test speed property of the Nic class."""
        self.assertEqual(str(self.test_nic.speed), Baseline("""1000000000"""))

    @patch('subprocess.call', side_effect=_mock_call)
    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_set_static_address(self, mocked_check_output, mocked_call_output):
        """Test set_static_address method of the Nic class."""
        self.assertEqual(str(self.test_nic.set_static_address('192.168.0.2', '255.255.255.0', '192.168.0.1')), Baseline("""0"""))

    @patch('subprocess.call', side_effect=_mock_call)
    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_use_dhcp(self, mocked_check_output, mocked_call_output):
        """Test set_static_address method of the Nic class."""
        self.assertEqual(str(self.test_nic.use_dhcp()), Baseline("""0"""))
