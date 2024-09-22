import logging

from .vendor_configuration import VendorConfiguration
from ..exceptions import ConfigError
from ..factory.Factory import Factory


class VendorConfigurationFactory(Factory):
    def __init__(self) -> None:
        self.module_template: str = "rs4lk.configuration.vendor"
        self.name_template: str = "%s_configuration"

    def create_from_name(self, name: str) -> VendorConfiguration:
        try:
            vendor_config = self.create_instance((), (name.lower(),))
            # vendor_config.load()
        except ImportError:
            raise ConfigError(f"Unsupported format type: {name}")

        return vendor_config
