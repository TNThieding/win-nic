"""Module containing NicNetConnectionStatus class."""

from enum import IntEnum


class NicNetConnectionStatus(IntEnum):
    """State of the network adapter connection to the network."""

    DISCONNECTED = 0
    """Disconnected """
    CONNECTING = 1
    """Connecting"""
    CONNECTED = 2
    """Connected"""
    DISCONNECTING = 3
    """Disconnecting """
    HARDWARE_NOT_PRESENT = 4
    """Hardware Not Present"""
    HARDWARE_DISABLED = 5
    """Hardware Disabled"""
    HARDWARE_MALFUNCTION = 6
    """Hardware Malfunciton"""
    MEDIA_DISCONNECTED = 7
    """Media Disconnected"""
    AUTHENTICATING = 8
    """Authenticating"""
    AUTHENTICATION_SUCCEEDED = 9
    """Authentication Succeeded"""
    AUTHENTICATION_FAILED = 10
    """Authentication Failed"""
    INVALID_ADDRESS = 11
    """Invalid Address"""
    CREDENTIALS_REQUIRED = 12
    """Credentials Required"""
