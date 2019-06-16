"""Module containing utilities (e.g. parsers and executors)."""

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

    if isinstance(wmic_response, bytes):
        wmic_response = wmic_response.decode('utf-8')

    return _strip_wmic_response(wmic_response)


def parse_array(raw_array):
    """Parse a WMIC array."""
    array_strip_brackets = raw_array.replace('{', '').replace('}', '')
    array_strip_spaces = array_strip_brackets.replace('"', '').replace(' ', '')
    return array_strip_spaces.split(',')


def _strip_wmic_response(wmic_resp):
    """Strip and remove header row (if attribute) or call log (if method)."""
    return [line.strip() for line in wmic_resp.split('\n') if line.strip() != ''][1:]
