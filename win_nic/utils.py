"""Module containing utilities, such as parsers and executors."""

import datetime
import os
import subprocess


def run_netsh_command(netsh_args):
    """Execute a netsh command and return the output."""
    devnull = open(os.devnull, 'w')
    command_raw = 'netsh interface ipv4 ' + netsh_args
    return int(subprocess.call(command_raw, stdout=devnull))


def run_wmic_command(wmic_args):
    """Execute a WMIC command and return the output."""
    wmic_response = subprocess.check_output(['wmic'] + wmic_args)
    return _strip_wmic_response(wmic_response)


def parse_array(raw_array):
    """Parse a WMIC array."""
    array_strip_brackets = raw_array.replace('{', '').replace('}', '')
    array_strip_spaces = array_strip_brackets.replace('"', '').replace(' ', '')
    return array_strip_spaces.split(',')


def parse_datetime(raw_datetime):
    """Parse a WMIC datetime."""
    stripped_suffix = raw_datetime.split('.')[0]
    year = int(stripped_suffix[0:4])
    month = int(stripped_suffix[4:6])
    day = int(stripped_suffix[6:8])
    hour = int(stripped_suffix[8:10])
    minute = int(stripped_suffix[10:12])
    second = int(stripped_suffix[12:14])
    return datetime.datetime(year, month, day, hour, minute, second)


def _strip_wmic_response(wmic_resp):
    # Strip and remove header row (if attribute) or call log (if method).
    return [line.strip() for line in wmic_resp.split('\n') if line.strip() != ''][1:]
