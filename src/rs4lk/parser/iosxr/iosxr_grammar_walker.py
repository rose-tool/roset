import ipaddress

from ...foundation.parser.grammar_walker import GrammarWalker
from ...grammar.iosxr.IosXrListener import IosXrListener
from ...grammar.iosxr.IosXrParser import IosXrParser
from ...model.bgp_session import BgpSession
from ...model.interface import Interface, VlanInterface


class IosxrGrammarWalker(IosXrListener, GrammarWalker):
    __slots__ = ['_bgp_groups', '_vlan_interfaces']

    def __init__(self) -> None:
        super().__init__()

        self._bgp_groups = {}
        self._vlan_interfaces: dict[str, dict] = {}

    def enterInterfaceSection(self, ctx: IosXrParser.InterfaceSectionContext) -> None:
        if_name = ctx.interfaceName().getText()
        if if_name == 'all':
            return

        active = True
        addresses = set()
        vlan_id = None

        for statement in ctx.interfaceStatement():
            if not active:
                break

            statement: IosXrParser.InterfaceStatementContext = statement

            ipv4_conf = statement.ipv4Config()
            if ipv4_conf is not None:
                ipv4_config_words = ipv4_conf.WORD()
                ipv4_address = ipv4_config_words[0].getText()
                ipv4_mask = sum(bin(int(x)).count('1') for x in ipv4_config_words[1].getText().split('.'))

                addresses.add(f"{ipv4_address}/{ipv4_mask}")
            ipv6_conf = statement.ipv6Config()
            if ipv6_conf is not None:
                ipv6_net = ipv6_conf.IPV6_NETWORK().getText()
                addresses.add(ipv6_net)
            encapsulation_conf = statement.encapsulationConfig()
            if encapsulation_conf is not None:
                vlans = encapsulation_conf.WORD()
                vlan_id = int(vlans[0].getText())
            shutdown_conf = statement.shutdownConfig()
            if shutdown_conf is not None:
                active = False

        if active:
            if if_name not in self._configuration.interfaces:
                if vlan_id is not None:
                    (phy, _) = if_name.split('.')
                    self._vlan_interfaces[if_name] = {'name': if_name, 'phy': phy, 'vlan': vlan_id, 'addr': []}
                else:
                    self._configuration.interfaces[if_name] = Interface(if_name)
            for address in addresses:
                if vlan_id is not None:
                    self._vlan_interfaces[if_name]['addr'].append(address)
                else:
                    ip_address = ipaddress.ip_interface(address)
                    self._configuration.interfaces[if_name].add_address(ip_address)
        else:
            if if_name in self._vlan_interfaces:
                del self._vlan_interfaces[if_name]
            elif if_name in self._configuration.interfaces:
                del self._configuration.interfaces[if_name]

    def enterBgpSection(self, ctx: IosXrParser.BgpSectionContext) -> None:
        self._configuration.local_as = int(ctx.WORD().getText())

        remote_ip = None
        remote_as = None
        local_iface = None
        for statement in ctx.bgpStatement():
            statement: IosXrParser.BgpStatementContext = statement
            for i in range(0, statement.getChildCount()):
                if isinstance(statement.getChild(i), IosXrParser.NeighborContext):
                    neighbor: IosXrParser.NeighborContext = statement.getChild(i, IosXrParser.NeighborContext)

                    remote_ip = neighbor.ipAddress().getText()

                    for neigh_statement in neighbor.neighborStatement():
                        neigh_statement: IosXrParser.NeighborStatementContext = neigh_statement

                        remote_as_statement = neigh_statement.remoteAs()
                        if remote_as_statement is not None:
                            remote_as = int(remote_as_statement.WORD().getText())
                        update_source_statement = neigh_statement.updateSource()
                        if update_source_statement is not None:
                            local_iface = update_source_statement.interfaceName().getText()

            if remote_ip and remote_as:
                if remote_as not in self._bgp_groups:
                    self._bgp_groups[remote_as] = {}

                self._bgp_groups[remote_as]['local_iface'] = local_iface

                if 'neighbors' not in self._bgp_groups[remote_as]:
                    self._bgp_groups[remote_as]['neighbors'] = []
                self._bgp_groups[remote_as]['neighbors'].append(remote_ip)

                self._bgp_groups[remote_as]['remote_as'] = remote_as

    def exitConfig(self, ctx: IosXrParser.ConfigContext) -> None:
        for group in self._bgp_groups.values():
            if group['remote_as'] not in self._configuration.sessions:
                self._configuration.sessions[group['remote_as']] = BgpSession(
                    self._configuration.local_as, group['remote_as']
                )

            local_iface = None
            if 'local_iface' in group:
                if group['local_iface'] in self._configuration.interfaces:
                    local_iface = self._configuration.interfaces[group['local_iface']]

            for neighbor in group['neighbors']:
                local_address = None
                if local_iface:
                    neighbor_v = ipaddress.ip_address(neighbor).version
                    v_addresses = [x.ip for x in local_iface.addresses if x.version == neighbor_v]
                    if len(v_addresses) > 0:
                        local_address = v_addresses.pop(0)

                self._configuration.sessions[group['remote_as']].add_peering(local_address, neighbor)

        self._bgp_groups.clear()

        for vlan_iface in self._vlan_interfaces.values():
            self._configuration.interfaces[vlan_iface['name']] = VlanInterface(
                vlan_iface['name'], self._configuration.interfaces[vlan_iface['phy']], vlan_iface['vlan']
            )

            for addr in vlan_iface['addr']:
                ip_address = ipaddress.ip_interface(addr)
                self._configuration.interfaces[vlan_iface['name']].add_address(ip_address)

        self._vlan_interfaces.clear()
