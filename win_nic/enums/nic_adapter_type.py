"""Module containing NicAdapterType class."""

from enum import IntEnum


class NicAdapterType(IntEnum):
    """Network medium in use."""

    ETHERNET = 0
    """Ethernet 802.3"""
    TOKEN_RING = 1
    """Token Ring 802.5"""
    FDDI = 2
    """Fiber Distributed Data Interface (FDDI)"""
    WAN = 3
    """Wide Area Network"""
    LOCALTALK = 4
    """LocalTalk"""
    ETHERNET_DIX = 5
    """Ethernet using DIX header format"""
    ARCNET = 6
    """ARCNET"""
    ARCNET_8782 = 7
    """ARCNET (878.2)"""
    ATM = 8
    """ATM"""
    WIRELESS = 9
    """Wireless"""
    INFRARED = 10
    """Infrared Wireless"""
    BPC = 11
    """Bpc"""
    COWAN = 12
    """CoWan"""
    FIREWIRE = 13
    """1394"""
