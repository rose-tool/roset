from abc import ABC, abstractmethod

from Kathara.model.Lab import Lab

from ..configuration.vendor_configuration import VendorConfiguration
from ...model.topology import Topology


class Action(ABC):
    @abstractmethod
    def verify(self, config: VendorConfiguration, topology: Topology, net_scenario: Lab) -> bool:
        raise NotImplementedError("You must implement `verify` method.")

    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError("You must implement `name` method.")

    @abstractmethod
    def display_name(self) -> str:
        raise NotImplementedError("You must implement `display_name` method.")
