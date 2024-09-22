from ..configuration.vendor_configuration import VendorConfiguration


class GrammarWalker:
    __slots__ = ['_configuration']

    def __init__(self) -> None:
        self._configuration: VendorConfiguration | None = None

    def set_vendor_config(self, conf: VendorConfiguration) -> None:
        self._configuration = conf
