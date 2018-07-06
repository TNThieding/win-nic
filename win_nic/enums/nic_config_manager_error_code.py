"""Module containing NicConfigManagerErrorCode class."""

from enum import IntEnum


class NicConfigManagerErrorCode(IntEnum):
    """Windows Configuration Manager error code."""

    WORKING_PROPERLY = 0
    """This device is working properly."""
    NOT_CONFIGURED_CORRECTLY = 1
    """This device is not configured correctly."""
    CANNOT_LOAD_DRIVER = 2
    """Windows cannot load the driver for this device."""
    DRIVER_CORRUPTED_LOW_MEM = 3
    """The driver for this device might be corrupted, or your system may be running low on
    memory or other resources."""
    DRIVER_REGISTRY_CORRUPTED = 4
    """This device is not working properly. One of its drivers or your registry might be
    corrupted."""
    CANNOT_MANAGE_DRIVER_RESOURCE = 5
    """The driver for this device needs a resource that Windows cannot manage."""
    CONFLICTING_BOOT_CONFIG = 6
    """The boot configuration for this device conflicts with other devices."""
    CANNOT_FILTER = 7
    """Cannot filter."""
    DRIVER_LOADER_MISSING = 8
    """The driver loader for the device is missing."""
    BAD_FIRMWARE_REPORTING = 9
    """This device is not working properly because the controlling firmware is reporting
    the resources for the device incorrectly."""
    CANNOT_START = 10
    """This device cannot start."""
    FAILED = 11
    """This device failed."""
    NO_FREE_RESOURCES = 12
    """This device cannot find enough free resources that it can use."""
    UNVERIFIED_RESOURCES = 13
    """Windows cannot verify this device's resources."""
    RESTART_COMPUTER = 14
    """This device cannot work properly until you restart your computer."""
    REENUMERATION_PROBLEM = 15
    """This device is not working properly because there is probably a re-enumeration
    problem."""
    UNIDENTIFIED_RESOURCES = 16
    """Windows cannot identify all the resources this device uses."""
    UNKNOWN_RESOURCE_TYPE = 17
    """This device is asking for an unknown resource type."""
    REINSTALL_DRIVERS = 18
    """Reinstall the drivers for this device."""
    VXD_FAILURE = 19
    """Failure using the VxD loader."""
    CORRUPTED_REGISTRY = 20
    """Your registry might be corrupted."""
    SYSTEM_FAILURE_REMOVING = 21
    """System failure: Try changing the driver for this device. If that does not work, see
    your hardware documentation. Windows is removing this device."""
    DISABLED = 22
    """This device is disabled."""
    SYSTEM_FAILURE_DOCS = 23
    """System failure: Try changing the driver for this device. If that doesn't work, see
    your hardware documentation."""
    NOT_PRESENT = 24
    """This device is not present, is not working properly, or does not have all its
    drivers installed."""
    SETTING_UP_25 = 25
    """Windows is still setting up the device. (Msg. ID 25)"""
    SETTING_UP_26 = 26
    """Windows is still setting up the device. (Msg. ID 26)"""
    BAD_LOG_CONFIG = 27
    """Device does not have valid log configuration."""
    DRIVER_NOT_INSTALLED = 28
    """The drivers for this device are not installed."""
    BAD_FIRMWARE_RESOURCES = 29
    """This device is disabled because the firmware of the device did not give it the
    required resources."""
    IRQ_IN_USE = 30
    """This device is using an Interrupt Request (IRQ) resource that another device is
    using."""
    WINDOWS_CANNOT_LOAD_DRIVERS = 31
    """This device is not working properly because Windows cannot load the drivers
    required for this device."""
    