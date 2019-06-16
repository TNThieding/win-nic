"""Module containing Nic class."""

from win_nic._nic_method import NicMethod


class Nic(NicMethod):

    """Windows network interface card (NIC) class.

    :param int index: index number of the network adapter (as stored in the system registry)

    """

    def __init__(self, index):
        super().__init__(index)
        self.index = index

    def __repr__(self):
        return "<'win_nic.Nic(index=" + str(self.index) + ")'>"

    def __str__(self):
        return self.caption
