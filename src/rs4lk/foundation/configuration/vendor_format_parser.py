from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class VendorFormatParser(ABC):
    @abstractmethod
    def check_file_existence(self, result: str) -> bool:
        raise NotImplementedError("You must implement `check_file_existence` method.")

    @abstractmethod
    def check_configuration_validity(self, result: str) -> bool:
        raise NotImplementedError("You must implement `check_configuration_validity` method.")

    @abstractmethod
    def parse_bgp_routes(self, result: Any) -> set:
        raise NotImplementedError("You must implement `parse_routing_table` method.")
