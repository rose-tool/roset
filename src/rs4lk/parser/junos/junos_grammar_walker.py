import ipaddress

from ...foundation.parser.grammar_walker import GrammarWalker
from ...grammar.junos.JunosListener import JunosListener
from ...grammar.junos.JunosParser import JunosParser
from ...model.bgp_session import BgpSession
from ...model.interface import Interface, VlanInterface


class JunosGrammarWalker(JunosListener, GrammarWalker):
    __slots__ = ['_bgp_groups', '_vlan_interfaces']

    def __init__(self) -> None:
        super().__init__()

        self._bgp_groups: dict[str, dict] = {}
        self._vlan_interfaces: dict[str, dict] = {}

    def enterInterfaceEntity(self, ctx: JunosParser.InterfaceEntityContext) -> None:
        if_name = ctx.interfaceName().getText()
        if if_name not in self._configuration.interfaces:
            self._configuration.interfaces[if_name] = Interface(if_name)

    def enterVlanId(self, ctx: JunosParser.VlanIdContext) -> None:
        if_name = ctx.parentCtx.interfaceName().WORD().getText()
        unit = int(ctx.unit().WORD().getText())

        standard_name = f"{if_name}.{unit}"
        self._vlan_interfaces[standard_name] = {'name': standard_name, 'phy': if_name, 'vlan': unit, 'addr': []}

    def enterInterfaceIp(self, ctx: JunosParser.InterfaceIpContext) -> None:
        unit = int(ctx.unit().WORD().getText())
        if_name = ctx.parentCtx.interfaceName().WORD().getText()
        address = ipaddress.ip_interface(ctx.ipNetwork().getText())

        if unit == 0:
            self._configuration.interfaces[if_name].add_address(address)
        else:
            standard_name = f"{if_name}.{unit}"
            self._vlan_interfaces[standard_name]['addr'].append(address)

    def enterLocalAsEntity(self, ctx: JunosParser.LocalAsEntityContext) -> None:
        self._configuration.local_as = int(ctx.WORD().getText())

    def enterBgpEntity(self, ctx: JunosParser.BgpEntityContext):
        group_name = ctx.groupName().getText()
        if group_name not in self._bgp_groups:
            self._bgp_groups[group_name] = {}

        if ctx.localAddress():
            self._bgp_groups[group_name]['local_address'] = ctx.localAddress().ipNetwork().getText()
        if ctx.neighbor():
            if 'neighbors' not in self._bgp_groups[group_name]:
                self._bgp_groups[group_name]['neighbors'] = []
            self._bgp_groups[group_name]['neighbors'].append(ctx.neighbor().ipNetwork().getText())
        if ctx.remoteAs():
            self._bgp_groups[group_name]['remote_as'] = int(ctx.remoteAs().asNum().getText())

    def exitConfig(self, ctx: JunosParser.ConfigContext) -> None:
        for group_name, group in self._bgp_groups.items():
            if 'neighbors' not in group or 'remote_as' not in group:
                continue

            if group['remote_as'] not in self._configuration.sessions:
                self._configuration.sessions[group['remote_as']] = BgpSession(
                    self._configuration.local_as, group['remote_as']
                )

            for neighbor in group['neighbors']:
                self._configuration.sessions[group['remote_as']].add_peering(
                    group['local_address'] if 'local_address' in group else None, neighbor, group_name
                )

        self._bgp_groups.clear()

        for vlan_iface in self._vlan_interfaces.values():
            self._configuration.interfaces[vlan_iface['name']] = VlanInterface(
                vlan_iface['name'], self._configuration.interfaces[vlan_iface['phy']], vlan_iface['vlan']
            )

            for addr in vlan_iface['addr']:
                self._configuration.interfaces[vlan_iface['name']].add_address(addr)

        self._vlan_interfaces.clear()
