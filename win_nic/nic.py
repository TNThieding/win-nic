"""Module containing Nic class."""

from win_nic._nic_method import NicMethod
from win_nic._nic_property import NicProperty

class Nic(object):

    """Windows network interface card (NIC) class.

    :param int index: Index number of the network adapter, as stored in the system registry.

    """

    def __init__(self, index):
        self.index = index
        self.property = NicProperty(index)
        self.method = NicMethod(index, self.property.net_connection_id, self.property.caption)

    def __repr__(self):
        return "<'win_nic.nic.Nic(index=" + str(self.index) + ")'>"

    def __str__(self):
        return self.property.caption
