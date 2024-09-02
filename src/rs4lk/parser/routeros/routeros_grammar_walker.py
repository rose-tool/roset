import re

from ...foundation.parser.grammar_walker import GrammarWalker
from ...grammar.routeros.RouterosListener import RouterosListener
from ...grammar.routeros.RouterosParser import RouterosParser
from ...model.bgp_session import BgpSession
from ...model.interface import Interface, VlanInterface


class RouterosGrammarWalker(RouterosListener, GrammarWalker):
    def enterInterfaceName(self, ctx: RouterosParser.InterfaceNameContext) -> None:
        if_name = ctx.WORD().getText()
        self._configuration.interfaces[if_name] = Interface(if_name)

    def enterVlanConfig(self, ctx: RouterosParser.VlanConfigContext) -> None:
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
                    vlan_id = int(value)
                if key == "interface":
                    interface = value

        self._configuration.interfaces[vlan_name] = VlanInterface(vlan_name, interface, vlan_id)

    def enterIpv4Config(self, ctx: RouterosParser.Ipv4ConfigContext) -> None:
        self._ip_config(ctx)

    def enterIpv6Config(self, ctx: RouterosParser.Ipv6ConfigContext) -> None:
        self._ip_config(ctx)

    def _ip_config(self, ctx: RouterosParser.Ipv4ConfigContext | RouterosParser.Ipv6ConfigContext) -> None:
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

        if interface not in self._configuration.interfaces:
            self._configuration.interfaces[interface] = Interface(interface)

        self._configuration.interfaces[interface].add_address(address)

    def enterBgpPeeringConfig(self, ctx: RouterosParser.BgpPeeringConfigContext) -> None:
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
                    self._configuration.local_as = value
                if key == ".as":
                    remote_as = value

        if remote_as and remote_address:
            if remote_as not in self._configuration.sessions:
                self._configuration.sessions[remote_as] = BgpSession(self._configuration.local_as, remote_as)

            remote_address = re.sub(r'/\d+$', '', remote_address)
            self._configuration.sessions[remote_as].add_peering(local_address, remote_address)
