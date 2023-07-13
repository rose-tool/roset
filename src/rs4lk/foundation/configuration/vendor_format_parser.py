from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class VendorFormatParser(ABC):
    @abstractmethod
    def parse_bgp_routes(self, result: Any) -> set:
        raise NotImplementedError("You must implement `parse_routing_table` method.")
