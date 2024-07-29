import ipaddress


class Interface:
    def __init__(self, name: str):
        self.name: str = name
        self.ipv4_addresses: list[ipaddress.IPv4Interface] = []
        self.ipv6_addresses: list[ipaddress.IPv6Interface] = []

    def add_address(self, address: str) -> None:
        ip_address = ipaddress.ip_interface(address)
        if ip_address.version == 4:
            self.ipv4_addresses.append(ip_address)
        else:
            self.ipv6_addresses.append(ip_address)

    def __str__(self) -> str:
        ipv4_str = ", ".join(str(addr) for addr in self.ipv4_addresses)
        ipv6_str = ", ".join(str(addr) for addr in self.ipv6_addresses)
        return f"Interface(name={self.name}, ipv4_addresses=[{ipv4_str}], ipv6_addresses=[{ipv6_str}])"

    def __repr__(self) -> str:
        return str(self)


class VlanInterface(Interface):
    def __init__(self, name, physical_interface: str, vlan_id: str):
        super().__init__(name)
        self.physical_interface: str = physical_interface
        self.vlan_id: str = vlan_id

    def __str__(self) -> str:
        ipv4_str = ", ".join(str(addr) for addr in self.ipv4_addresses)
        ipv6_str = ", ".join(str(addr) for addr in self.ipv6_addresses)
        return (f"VlanInterface(name={self.name}, physical_interface={self.physical_interface}, "
                f"vlan_id={self.vlan_id}, ipv4_addresses=[{ipv4_str}], ipv6_addresses=[{ipv6_str}])")

    def __repr__(self) -> str:
        return str(self)


class BgpConnection:
    def __init__(self, remote_as: str, local_address: str, remote_address: str):
        self.remote_as: str = remote_as
        self.local_address: ipaddress.IPv4Interface | ipaddress.IPv6Interface = ipaddress.ip_interface(local_address)
        self.remote_address = ipaddress.ip_interface(remote_address)

    def __str__(self) -> str:
        return (f"BgpSession(remote_as={self.remote_as}, local_ip='{self.local_address}', "
                f"remote_ip='{self.remote_address}')")

    def __repr__(self) -> str:
        return (f"BgpSession(remote_as={repr(self.remote_as)}, local_ip={repr(self.local_address)}, "
                f"remote_ip={repr(self.remote_address)})")


class RouterConfiguration:
    def __init__(self, config_path: str):
        self._config_path = config_path
        self.interfaces: dict[str, Interface] = {}
        self.peerings: list[BgpConnection] = []
        self.local_as = None
        self.rule_names = None
