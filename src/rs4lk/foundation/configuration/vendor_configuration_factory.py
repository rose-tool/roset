import logging

from .vendor_configuration import VendorConfiguration
from ..exceptions import ConfigError
from ..factory.Factory import Factory
from ...configuration.batfish.batfish_configuration import BatfishConfiguration


class VendorConfigurationFactory(Factory):
    format_to_type: dict = {
        'FLAT_JUNIPER': 'vmx',
        'CISCO_IOS_XR': 'ios_xr'
    }

    def __init__(self) -> None:
        self.module_template: str = "rs4lk.configuration.vendor"
        self.name_template: str = "%s_configuration"

    def create_from_batfish_config(self, batfish_config: BatfishConfiguration) -> VendorConfiguration:
        vendor_format = batfish_config.get_format()

        if vendor_format not in self.format_to_type:
            raise ConfigError(f"Unsupported format type: {vendor_format}")

        logging.info(f"Configuration format is `{vendor_format}`, loading vendor configuration...")

        vendor = self.format_to_type[vendor_format]

        vendor_config = self.create_instance((), (vendor,))
        vendor_config.load(batfish_config)

        return vendor_config
