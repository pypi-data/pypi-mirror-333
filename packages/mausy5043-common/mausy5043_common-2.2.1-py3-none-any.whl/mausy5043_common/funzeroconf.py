#!/usr/bin/env python3

# wizwtr
# Copyright (C) 2025  Maurice (mausy5043) Hendrix
# AGPL-3.0-or-later  - see LICENSE

"""Discover Multi-cast devices that support Homewizard."""

import json
import logging
import logging.handlers
import os
import platform
import sys
import time
from typing import Any

from zeroconf import ServiceBrowser, ServiceListener, Zeroconf

# initialize logging
__is_macos = platform.system() == "Darwin"
__hndlrs: list = []
if not __is_macos:
    hndlrs = [
        logging.handlers.SysLogHandler(
            address="/dev/log",
            facility=logging.handlers.SysLogHandler.LOG_DAEMON,
        ),
    ]
logging.basicConfig(
    level=logging.INFO,
    format="%(module)s.%(funcName)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=__hndlrs,
)
LOGGER: logging.Logger = logging.getLogger(__name__)

# fmt: off
# constants
DEBUG = False
HERE = os.path.realpath(__file__).split("/")
MYID = HERE[-1]
MYAPP = HERE[-4]
MYROOT = "/".join(HERE[0:-4])
APPROOT = "/".join(HERE[0:-3])
NODE = os.uname()[1]
# fmt: on


class MyListener(ServiceListener):
    r"""Overloaded class of zeroconf.ServiceListener.

    Examples of output:
    Service DABMAN i205 CDCCai6fu6g4c4ZZ._http._tcp.local. discovered
    ServiceInfo(type='_http._tcp.local.',
                name='DABMAN i205 CDCCai6fu6g4c4ZZ._http._tcp.local.',
                addresses=[b'\xc0\xa8\x02\x95'],
                port=80,
                weight=0,
                priority=0,
                server='http-DABMAN i205 CDCCai6fu6g4c4ZZ.local.',
                properties={b'path': b'/irdevice.xml,CUST_APP=0,BRAND=IMPERIAL,MAC=____________'},
                interface_index=None)
    ip = 192:168:2:149

    Service RBFILE._smb._tcp.local. discovered
    ServiceInfo(type='_smb._tcp.local.',
                name='RBFILE._smb._tcp.local.',
                addresses=[b'\xc0\xa8\x02\x12'],
                port=445,
                weight=0,
                priority=0,
                server='rbfile.local.',
                properties={b'': None},
                interface_index=None)
    ip = 192:168:2:18

    Service Canon_TS6251._http._tcp.local. discovered
    ServiceInfo(type='_http._tcp.local.',
                name='Canon_TS6251._http._tcp.local.',
                addresses=[b'\xc0\xa8\x02\xf0'],
                port=80,
                weight=0,
                priority=0,
                server='proton3.local.',
                properties={b'txtvers': b'1'},
                interface_index=None)
    ip = 192:168:2:240
    """

    def __init__(self) -> None:
        """Initialise the listener."""
        self.discovered: dict = {}

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Forget services that disappear during the discovery scan."""
        _name = name.replace(" ", "_")
        __name = _name.split(".")[0]
        LOGGER.debug(f"(  -) Service {__name} {type_} disappeared.")
        if __name in self.discovered:
            del self.discovered[__name]

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Update information for services that send updates.

        Overridden but not used.
        """
        _name = name.replace(" ", "_")
        __name = _name.split(".")[0]
        __type = type_.split(".")[0]
        LOGGER.debug(f"( * ) Service {__name} updated. ( {__type} )")
        # find out updated info about this device
        info = zc.get_service_info(type_, name)
        svc: str = ""
        prop: dict = {}
        if info:
            try:
                prop = self.debyte(info.properties)
                if info.addresses:
                    svc = ".".join(list(map(str, list(info.addresses[0]))))
            except BaseException:
                LOGGER.debug(
                    f"Exception for device info: {info}\n {info.properties}\n {info.addresses}\n"
                )
                raise
        if (__name in self.discovered) and (__type in self.discovered[__name]):
            self.discovered[__name][__type] = {
                "ip": svc,
                "name": name,
                "type": type_,
                "properties": prop,
            }

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Remember services that are discovered during the scan."""
        _name = name.replace(" ", "_")
        __name = _name.split(".")[0]
        __type = type_.split(".")[0]
        # find out more about this device
        info = zc.get_service_info(type_, name)
        svc: str = ""
        prop: dict = {}
        if info:
            try:
                prop = self.debyte(info.properties)
                if info.addresses:
                    svc = ".".join(list(map(str, list(info.addresses[0]))))
            except BaseException:
                LOGGER.debug(
                    f"Exception for device info: {info}\n {info.properties}\n {info.addresses}\n"
                )
                raise
        LOGGER.debug(f"(+  ) Service {__name} discovered ( {__type} ) on {svc}")
        # register the device
        if __name not in self.discovered:
            self.discovered[__name] = {
                f"{__type}": {
                    "ip": svc,
                    "name": name,
                    "type": type_,
                    "service": prop["product_type"],
                    "properties": prop,
                }
            }
        # additional services discovered for an already discovered device
        if __type not in self.discovered[__name]:
            self.discovered[__name][__type] = {
                "ip": svc,
                "name": name,
                "type": type_,
                "service": prop["product_type"],
                "properties": prop,
            }

    @staticmethod
    def debyte(bytedict: Any) -> dict[str, str]:
        """Transform a dictionary with byte keys and values to a dictionary with string keys and values.

        Args:
            bytedict (Any): A dictionary where both keys and values are bytes. It may also be empty or None.

        Returns:
            dict[str, str]: A dictionary where both keys and values are strings. If a value in the input dictionary is None,
                            the corresponding value in the output dictionary will also be None. Empty keys are ignored.
        """
        normdict = {}
        if bytedict:
            # bytedict may be empty or None
            for _y in bytedict:
                _x = bytedict[_y]
                # value None can't be decoded
                if _x:
                    normdict[_y.decode("ascii")] = _x.decode("ascii")
                else:
                    # protect against empty keys
                    if _y:
                        normdict[_y.decode("ascii")] = None
        return normdict


def get_ip(service: str, filtr: str = '', timeout: float = 30.0) -> list[str]:
    """Discover and retrieve IP addresses for a given service.

    Args:
        service (str): The name of the service to discover.
        filtr (str): A filter string to match specific services.
        timeout (float): The maximum time in seconds to wait for the discovery to complete.

    Returns:
        list[str]: A list of IP addresses that match the given service and filter.
    """
    _ip: list[str] = []
    _zc = Zeroconf()
    _ls = MyListener()
    _service = service
    if "_tcp.local." not in _service:
        _service = "".join([service, "._tcp.local."])
    # find the service:
    _ = ServiceBrowser(_zc, _service, _ls)

    t0: float = time.time()
    dt: float = 0.0
    while dt < timeout:  # and not _ls.discovered:
        dt = time.time() - t0
    _zc.close()
    LOGGER.debug("Discovery done.")
    LOGGER.debug(json.dumps(_ls.discovered, indent=4))
    if _ls.discovered:
        for _i in _ls.discovered:  # pylint: disable=consider-using-dict-items
            if filtr and filtr == _ls.discovered[_i][service]['service']:
                _ip.append(_ls.discovered[_i][service]["ip"])
            if not filtr:
                _ip.append(_ls.discovered[_i][service]["ip"])
    return _ip


if __name__ == "__main__":
    # initialise logging to console
    LOGGER.addHandler(logging.StreamHandler(sys.stdout))
    LOGGER.level = logging.DEBUG

    LOGGER.debug("Debug-mode started.")
    LOGGER.debug(f"IP = {get_ip(service='_hwenergy', filtr='HWE-WTR')}")
    LOGGER.debug("...done")
