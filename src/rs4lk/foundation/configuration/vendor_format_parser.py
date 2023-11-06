from abc import ABC, abstractmethod
from typing import Any


class VendorFormatParser(ABC):
    @abstractmethod
    def check_health(self, result: str) -> bool:
        raise NotImplementedError("You must implement `check_healthcheck` method.")

    @abstractmethod
    def check_file_existence(self, result: str) -> bool:
        raise NotImplementedError("You must implement `check_file_existence` method.")

    @abstractmethod
    def check_configuration_validity(self, result: str) -> bool:
        raise NotImplementedError("You must implement `check_configuration_validity` method.")

    @abstractmethod
    def check_bgp_state(self, result: str) -> bool:
        raise NotImplementedError("You must implement `check_bgp_state` method.")

    @abstractmethod
    def parse_bgp_routes(self, result: str) -> set:
        raise NotImplementedError("You must implement `parse_routing_table` method.")
