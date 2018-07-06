﻿"""Module containing NetworkAdapters class."""

import texttable

from . import utils
from .nic import Nic


# pylint: disable=too-few-public-methods
class NetworkAdapters(object):

    """Network adapter discoverer class."""

    def __init__(self):
        self.nic_connection_id_map = {}
        self.nic_name_map = {}

        # Get the index and name of each NIC.
        nic_rows = utils.run_wmic_command(['nic', 'get', 'Index,' 'Name'])
        for nic in nic_rows:
            index = int(nic.split(' ')[0])
            name = ' '.join(nic.split(' ')[1:]).strip()
            self.nic_name_map[name] = index

        # Get the index and net connection ID of each NIC.
        nic_rows = utils.run_wmic_command(['nic', 'get', 'Index,' 'NetConnectionID'])
        for nic in nic_rows:
            index = int(nic.split(' ')[0])
            name = ' '.join(nic.split(' ')[1:]).strip()
            self.nic_connection_id_map[name] = index

    @staticmethod
    def dump():
        """Print a table of NICs to the console."""
        table_header = ['Index', 'Name', 'Connection ID']
        nic_list_raw = [list(filter(None, row.split('  ')))
                        for row in utils.run_wmic_command(['nic', 'get', 'Index,', 'Name,',
                                                           'NetConnectionID'])]
        nic_list_filled = [entry + [''] if len(entry) == 2 else entry for entry in nic_list_raw]
        nic_list_filled.insert(0, table_header)
        table = texttable.Texttable()
        table.add_rows(nic_list_filled)
        print(table.draw())  # pylint: disable=superfluous-parens

    def get_nic(self, index=None, name=None, connection_id=None):
        """Get the specified NIC instance.

        Note that only one parameter is used to discover the NIC.

        :param int index:
            Index number of the network adapter, as stored in the system registry.

        :param str name:
            Label by which the object is known.

        :param str connection_id:
            Name of the network connection as it appears in the Network Connections
            Control Panel program.

        :returns:
            Windows network interface card (NIC) instance.
        :rtype: win_nic.nic.Nic

        """
        if index:
            return Nic(index)
        elif name:
            return Nic(self.nic_name_map[name])
        elif connection_id:
            return Nic(self.nic_connection_id_map[connection_id])
        else:
            raise NameError("No NIC identifier specified!")
