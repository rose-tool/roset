import ipaddress

from .antlr4_parser.JunosListener import JunosListener
from .antlr4_parser.JunosParser import JunosParser
from .antlr4_parser.JunosVisitor import JunosVisitor
from ...configuration.router_configuration import RouterConfiguration, Interface, BgpConnection, VlanInterface


class JunosCustomListener(JunosListener):

    def __init__(self, configuration):
        super().__init__()
        self.configuration: RouterConfiguration = configuration
        self.visitor: JunosVisitor = JunosVisitor()
        self.bgp_groups = {}

    def enterInterface(self, ctx: JunosParser.InterfaceContext):
        if_name = ctx.interfaceName().getText()
        if if_name not in self.configuration.interfaces:
            self.configuration.interfaces[if_name] = Interface(if_name)

    def enterInterfaceIp(self, ctx: JunosParser.InterfaceIpContext):
        unit = int(ctx.unit().WORD().getText())
        if unit == 0:
            if_name = ctx.parentCtx.interfaceName().WORD().getText()
            self.configuration.interfaces[if_name].add_address(ctx.ipNetwork().getText())

        else:
            physical_if = ctx.parentCtx.interfaceName().WORD().getText()
            vlan_id = str(unit)
            iface_name = f"{physical_if}.{vlan_id}"
            if iface_name not in self.configuration.interfaces:
                interface = VlanInterface(iface_name, physical_if, vlan_id)
                self.configuration.interfaces[iface_name] = interface
            else:
                interface = self.configuration.interfaces[iface_name]

            address = ctx.ipNetwork().getText()
            interface.add_address(address)

    def enterBgpConfig(self, ctx: JunosParser.BgpConfigContext):
        group_name = ctx.groupName().getText()
        if group_name not in self.bgp_groups:
            self.bgp_groups[group_name] = {}

        if ctx.localAddress():
            self.bgp_groups[group_name]['local_address'] = ctx.localAddress().ipNetwork().getText()
        if ctx.neighbor():
            self.bgp_groups[group_name]['remote_address'] = ctx.neighbor().ipNetwork().getText()
        if ctx.remoteAs():
            self.bgp_groups[group_name]['remote_as'] = ctx.remoteAs().asNum().getText()

    def enterLocalAs(self, ctx: JunosParser.LocalAsContext):
        self.configuration.local_as = ctx.WORD().getText()

    def exitConfig(self, ctx: JunosParser.ConfigContext):
        for _, group in self.bgp_groups.items():
            if 'remote_address' in group and 'local_address' in group and 'remote_as' in group:
                self.configuration.peerings[group['remote_as']] = BgpConnection(
                    group['local_address'], group['remote_address'], group['remote_as'])
