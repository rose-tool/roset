from __future__ import annotations

import ipaddress
from abc import ABC, abstractmethod


class CommandsMixin(ABC):
    @abstractmethod
    def command_get_bgp_summary(self) -> str:
        raise NotImplementedError("You must implement `command_get_bgp_summary` method.")

    @abstractmethod
    def command_get_neighbour_bgp_networks(self, neighbour_ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> str:
        raise NotImplementedError("You must implement `command_get_neighbour_bgp_networks` method.")

    @abstractmethod
    def command_set_iface_ip(self, num: int, ip: ipaddress.IPv4Interface | ipaddress.IPv6Interface) -> str:
        raise NotImplementedError("You must implement `command_set_iface_ip` method.")

    @abstractmethod
    def command_unset_iface_ip(self, num: int, ip: ipaddress.IPv4Interface | ipaddress.IPv6Interface) -> str:
        raise NotImplementedError("You must implement `command_unset_iface_ip` method.")
