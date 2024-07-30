import ipaddress

from .antlr4_parser.JunosListener import JunosListener
from .antlr4_parser.JunosParser import JunosParser
from .antlr4_parser.JunosVisitor import JunosVisitor
from ...configuration.router_configuration import RouterConfiguration, Interface, BgpConnection


class JunosCustomListener(JunosListener):

    def __init__(self, configuration):
        super().__init__()
        self.configuration: RouterConfiguration = configuration
        self.visitor: JunosVisitor = JunosVisitor()
        self.bgp_groups={}

    def enterInterfaceIp(self, ctx:JunosParser.InterfaceIpContext):
        if_name = ctx.interfaceName().WORD().getText()
        self.configuration.interfaces[if_name] = Interface(if_name)
        if ctx.ipNetwork():
            self.configuration.interfaces[if_name].add_address(ctx.ipNetwork().getText())

    def enterBgpConfig(self, ctx:JunosParser.BgpConfigContext):
        group_name = ctx.groupName().getText()
        if group_name not in self.bgp_groups:
            self.bgp_groups[group_name] = {}

        if ctx.localAddress():
            self.bgp_groups[group_name]['local_address'] = ctx.localAddress().ipNetwork().getText()
        if ctx.neighbor():
            self.bgp_groups[group_name]['remote_address'] = ctx.neighbor().ipNetwork().getText()
        if ctx.remoteAs():
            self.bgp_groups[group_name]['remote_as'] = ctx.remoteAs().asNum().getText()

    def exitConfig(self, ctx:JunosParser.ConfigContext):
        for _, group in self.bgp_groups.items():
            self.configuration.peerings.append(
                BgpConnection(group['local_address'] if 'local_address' in group else None,
                              group['remote_address'] if 'remote_address' in group else None,
                              group['remote_as'] if 'remote_as' in group else None)
            )





