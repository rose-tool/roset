import ipaddress


class Interface:
    __slots__ = ['name', 'original_name', 'addresses']

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.original_name: str | None = None
        self.addresses: set[ipaddress.IPv4Interface | ipaddress.IPv6Interface] = set()

    def add_address(self, address: str) -> None:
        ip_address = ipaddress.ip_interface(address)

        self.addresses.add(ip_address)

    def rename(self, new_name: str) -> None:
        self.original_name = self.name
        self.name = new_name

    def __str__(self) -> str:
        return f"Interface(name={self.name}, original={self.original_name}, ip_addresses={self.addresses})"

    def __repr__(self) -> str:
        return str(self)


class VlanInterface(Interface):
    def __init__(self, name: str, phy_name: str, vlan: int):
        super().__init__(name)
        self.phy_name: str = phy_name
        self.vlan: int = vlan

    def __str__(self) -> str:
        return (f"VlanInterface(name={self.name}, phy_name={self.phy_name}, "
                f"vlan={self.vlan}, ip_addresses={self.addresses})")

    def __repr__(self) -> str:
        return str(self)
