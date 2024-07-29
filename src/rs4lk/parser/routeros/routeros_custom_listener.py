from rs4lk.parser.routeros.antlr4.RouterosListener import RouterosListener
from rs4lk.parser.routeros.antlr4.RouterosParser import RouterosParser
from rs4lk.configuration.router_configuration import RouterConfiguration, VlanInterface, Interface, BgpConnection


class RouterosCustomListener(RouterosListener):

    def __init__(self, configuration):
        super().__init__()
        self.configuration: RouterConfiguration = configuration

    def enterInterfaceName(self, ctx: RouterosParser.InterfaceNameContext):
        if_name = str(ctx.INTERFACE_NAME())
        self.configuration.interfaces[if_name] = Interface(name=if_name)

    def enterVlanConfig(self, ctx: RouterosParser.VlanConfigContext):
        vlan_name = None
        vlan_id = None
        interface = None
        for i in range(0, ctx.getChildCount()):
            key_value: RouterosParser.KeyValuePairContext = ctx.keyValuePair(i)
            if key_value:
                key = key_value.key().getText()
                value = key_value.value().getText()
                if key == "name":
                    vlan_name = value
                if key == "vlan-id":
                    vlan_id = value
                if key == "interface":
                    interface = value
        self.configuration.interfaces[vlan_name] = VlanInterface(vlan_name, interface, vlan_id)

    def enterIpv4Config(self, ctx: RouterosParser.Ipv4ConfigContext):
        interface = None
        address: str = ""
        for i in range(0, ctx.getChildCount()):
            key_value: RouterosParser.KeyValuePairContext = ctx.keyValuePair(i)
            if key_value:
                key = key_value.key().getText()
                value = key_value.value().getText()
                if key == "interface":
                    interface = value
                if key == "address":
                    address = value

        if interface not in self.configuration.interfaces:
            self.configuration.interfaces[interface] = Interface(name=interface)
        self.configuration.interfaces[interface].add_address(address)

    def enterBgpPeeringConfig(self, ctx: RouterosParser.BgpPeeringConfigContext):
        role = None
        remote_as = None
        local_address = None
        remote_address = None

        for i in range(0, ctx.getChildCount()):
            key_value: RouterosParser.KeyValuePairContext = ctx.keyValuePair(i)
            if key_value:
                key = key_value.key().getText()
                value = key_value.value().getText()
                if key == "local.address":
                    local_address = value
                if key == "remote.address":
                    remote_address = value
                if key == "as":
                    self.configuration.local_as = value
                if key == ".as":
                    remote_as = value

        if remote_as and local_address and remote_address:
            self.configuration.peerings.append(BgpConnection(remote_as, local_address, remote_address))
