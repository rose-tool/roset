import ipaddress


class Interface:
    def __init__(self, name: str):
        self.name: str = name
        self.ip_addresses: set[ipaddress.IPv4Interface | ipaddress.IPv6Interface] = set()

    def add_address(self, address: str) -> None:
        ip_address = ipaddress.ip_interface(address)
        self.ip_addresses.add(ip_address)

    def __str__(self) -> str:
        ip_str = ", ".join(str(addr) for addr in self.ip_addresses)
        return f"Interface(name={self.name}, ip_addresses=[{ip_str}])"

    def __repr__(self) -> str:
        return str(self)


class VlanInterface(Interface):
    def __init__(self, name: str, physical_interface: str, vlan_id: str):
        super().__init__(name)
        self.physical_interface: str = physical_interface
        self.vlan_id: str = vlan_id

    def __str__(self) -> str:
        ip_str = ", ".join(str(addr) for addr in self.ip_addresses)
        return (f"VlanInterface(name={self.name}, physical_interface={self.physical_interface}, "
                f"vlan_id={self.vlan_id}, ip_addresses=[{ip_str}])")

    def __repr__(self) -> str:
        return str(self)


class BgpConnection:
    def __init__(self, local_address: str | None, remote_address: str | None, remote_as: str | None):
        self.remote_as: str | None = remote_as
        self.local_address: ipaddress.IPv4Interface | ipaddress.IPv6Interface = ipaddress.ip_interface(
            local_address) if local_address else None
        self.remote_address: ipaddress.IPv4Interface | ipaddress.IPv6Interface = ipaddress.ip_interface(
            remote_address) if remote_address else None

    def __str__(self) -> str:
        return (f"BgpSession(remote_as={self.remote_as}, local_ip='{self.local_address}', "
                f"remote_ip='{self.remote_address}')")

    def __repr__(self) -> str:
        return (f"BgpSession(remote_as={repr(self.remote_as)}, local_ip={repr(self.local_address)}, "
                f"remote_ip={repr(self.remote_address)})")


class RouterConfiguration:
    def __init__(self, config_path: str):
        self.path = config_path
        self.interfaces: dict[str, Interface] = {}
        self.peerings: dict[str, BgpConnection] = {}
        self.local_as = None
        self._rule_names = None
