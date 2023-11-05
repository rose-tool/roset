import ipaddress
import logging
from abc import ABC, abstractmethod

from .commands_mixin import CommandsMixin
from .configuration_applier import ConfigurationApplier
from .vendor_format_parser import VendorFormatParser
from ..exceptions import ConfigError
from ...configuration.batfish.batfish_configuration import BatfishConfiguration
from ...model.bgp_session import BgpSession


class VendorConfiguration(ConfigurationApplier, CommandsMixin, VendorFormatParser, ABC):
    __slots__ = ['_batfish_config', '_lines', 'iface_to_iface_idx']

    CONFIG_FILE_PATH: str = "/config/startup-config.cfg"

    def __init__(self) -> None:
        self._batfish_config: BatfishConfiguration | None = None
        self._lines: list[str] | None = None
        self.iface_to_iface_idx: dict[str, int] = {}

    @property
    def name(self) -> str:
        return self._batfish_config.name

    @property
    def path(self) -> str:
        return self._batfish_config.path

    @property
    def interfaces(self) -> dict[str, dict]:
        return self._batfish_config.get_interfaces()

    @interfaces.setter
    def interfaces(self, value: dict[str, dict]) -> None:
        self._batfish_config.set_interfaces(value)

    @property
    def bgp_sessions(self) -> dict[int, BgpSession]:
        return self._batfish_config.get_bgp_sessions()

    @bgp_sessions.setter
    def bgp_sessions(self, value: dict[int, BgpSession]) -> None:
        self._batfish_config.set_bgp_sessions(value)

    def load(self, batfish_config: BatfishConfiguration) -> None:
        self._batfish_config = batfish_config

        with open(self._batfish_config.path, 'r') as config_file:
            self._lines = config_file.readlines()

        if not self._lines:
            raise ConfigError("Empty config file")

        self._batfish_config.get_interfaces()
        self._batfish_config.get_bgp_sessions()

        self._init()
        self._infer_bgp_dc_sessions()
        self._on_load_complete()

    @abstractmethod
    def get_image(self) -> str:
        raise NotImplementedError("You must implement `get_image` method.")

    @abstractmethod
    def _init(self) -> None:
        raise NotImplementedError("You must implement `_init` method.")

    def _infer_bgp_dc_sessions(self) -> None:
        logging.info("Inferring directly connected BGP sessions.")

        for session in self.bgp_sessions.values():
            iface = None
            for peering in session.peerings:
                iface, local_ip = self._batfish_config.get_interface_for_peering(peering)
                if not iface:
                    continue

                peering.local_ip = local_ip

            session.iface = iface

        logging.debug(f"Resulting sessions: {self.bgp_sessions}")

    @abstractmethod
    def _on_load_complete(self) -> None:
        raise NotImplementedError("You must implement `_on_load_complete` method.")

    def get_local_as(self) -> int:
        batfish_local_as = self._batfish_config.get_local_as()
        if batfish_local_as > 0:
            return batfish_local_as

        vendor_local_as = self._get_bgp_local_as_vendor()
        self._batfish_config.set_local_as(vendor_local_as)
        return vendor_local_as

    @abstractmethod
    def _get_bgp_local_as_vendor(self) -> int:
        raise NotImplementedError("You must implement `_get_bgp_local_as_vendor` method.")
