"""Module containing network adapters class unit tests."""

import sys
from unittest import TestCase
from unittest.mock import patch
from io import StringIO

from baseline import Baseline

from .. import _network_adapters


# pylint: disable=too-many-public-methods, unused-argument
class TestNic(TestCase):

    """Execute network adapters class unit tests."""

    # pylint: disable=no-self-argument
    def _mock_check_output(args):
        command = ' '.join(args)
        wmic_responses = {
            'wmic nic get Index,Name': 'Index  Name\n0      Ethernet Adapter\n1      Wi-Fi Adapter',
            'wmic nic get Index, Name, NetConnectionID': ('Index  Name                           ' +
                                                          '            NetConnectionID\n0      Et' +
                                                          'hernet Adapter                        ' +
                                                          ' Local Area Connection\n1      Wi-Fi A' +
                                                          'dapter                                ' +
                                                          ' Wireless Area Connection'),
            'wmic nic get Index,NetConnectionID': ('Index  NetConnectionID\n0      Local Area Con' +
                                                   'nection\n1      Wireless Area Connection'),
        }
        return wmic_responses[command]

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def setUp(self, mocked_check_output):  # pylint: disable=arguments-differ
        """Instantiate a network adapters class."""
        self.test_adapters = _network_adapters.NetworkAdapters()

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_dump(self, mocked_check_output):
        """Test dump method of NetworkAdapters."""
        _stdout = sys.stdout
        sys.stdout = StringIO()
        self.test_adapters.dump()
        _printed = sys.stdout.getvalue()
        sys.stdout = _stdout
        self.assertEqual(_printed, Baseline("""
            +-------+------------------+---------------------------+
            | Index |       Name       |       Connection ID       |
            +=======+==================+===========================+
            | 0     | Ethernet Adapter |  Local Area Connection    |
            +-------+------------------+---------------------------+
            | 1     | Wi-Fi Adapter    |  Wireless Area Connection |
            +-------+------------------+---------------------------+

            """))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_nic_name_map(self, mocked_check_output):
        """Test nic_name_map attribute of NetworkAdapters."""
        self.assertEqual(str(sorted(self.test_adapters.nic_name_map,
                                    key=self.test_adapters.nic_name_map.get)),
                         Baseline("""['Ethernet Adapter', 'Wi-Fi Adapter']"""))

    @patch('subprocess.check_output', side_effect=_mock_check_output)
    def test_nic_connection_id_map(self, mocked_check_output):
        """Test nic_connection_id_map attribute of NetworkAdapters."""
        self.assertEqual(str(sorted(self.test_adapters.nic_connection_id_map,
                                    key=self.test_adapters.nic_connection_id_map.get)),
                         Baseline("""['Local Area Connection', 'Wireless Area Connection']"""))
