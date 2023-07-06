from __future__ import annotations

import ipaddress
import json


class RibEntry:
    __slots__ = ['network', 'peer_as', 'as_path']

    def __init__(self, peer_as: int, network: str, as_path: str) -> None:
        self.peer_as: int = peer_as
        self.network: ipaddress.IPv4Network | ipaddress.IPv6Network = ipaddress.ip_network(network)
        self.as_path: list[int] = json.loads(as_path)

    def __repr__(self) -> str:
        return f"{self.peer_as} => {self.network} | Path={self.as_path}"
