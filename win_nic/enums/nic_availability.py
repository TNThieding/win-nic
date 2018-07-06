"""Module containing NicAvailability class."""

from enum import IntEnum


class NicAvailability(IntEnum):
    """Availability and status of the device."""

    OTHER = 1
    """Other"""
    UNKNOWN = 2
    """Unknown"""
    RUNNING = 3
    """Running/Full Power"""
    WARNING = 4
    """Warning"""
    IN_TEST = 5
    """In Tesst"""
    NOT_APPLICABLE = 6
    """Not Applicable"""
    POWER_OFF = 7
    """Power Off"""
    OFF_LINE = 8
    """Off Line"""
    OFF_DUTY = 9
    """Odd Duty"""
    DEGRADED = 10
    """Degraded"""
    NOT_INSTALLED = 11
    """Not Installed"""
    INSTALL_ERROR = 12
    """Install Error"""
    POWER_SAVE_UNKNOWN = 13
    """Power Save - Unknown"""
    POWER_SAVE_LOW_POWER = 14
    """Power Save - Low Power"""
    POWER_SAVE_STANDBY = 15
    """Power Save - Standby"""
    POWER_CYCLE = 16
    """Power Cycle"""
    POWER_SAVE_WARNING = 17
    """Power Save - Warning"""
    PAUSED = 18
    """Paused"""
    NOT_READY = 19
    """Not Ready"""
    NOT_CONFIGURED = 20
    """Not Configured"""
    QUIET = 21
    """Quiet"""
