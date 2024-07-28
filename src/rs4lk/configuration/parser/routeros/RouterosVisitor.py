# Generated from Routeros.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .RouterosParser import RouterosParser
else:
    from RouterosParser import RouterosParser

# This class defines a complete generic visitor for a parse tree produced by RouterosParser.

class RouterosVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by RouterosParser#config.
    def visitConfig(self, ctx:RouterosParser.ConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#section.
    def visitSection(self, ctx:RouterosParser.SectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#ethInterfaceSection.
    def visitEthInterfaceSection(self, ctx:RouterosParser.EthInterfaceSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#ethernetConfig.
    def visitEthernetConfig(self, ctx:RouterosParser.EthernetConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#vlanInterfaceSection.
    def visitVlanInterfaceSection(self, ctx:RouterosParser.VlanInterfaceSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#vlanConfig.
    def visitVlanConfig(self, ctx:RouterosParser.VlanConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#ipv4AddressSection.
    def visitIpv4AddressSection(self, ctx:RouterosParser.Ipv4AddressSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#ipv4Config.
    def visitIpv4Config(self, ctx:RouterosParser.Ipv4ConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#ipv6AddressSection.
    def visitIpv6AddressSection(self, ctx:RouterosParser.Ipv6AddressSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#ipv6Config.
    def visitIpv6Config(self, ctx:RouterosParser.Ipv6ConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#bgpPeeringSection.
    def visitBgpPeeringSection(self, ctx:RouterosParser.BgpPeeringSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#bgpPeeringConfig.
    def visitBgpPeeringConfig(self, ctx:RouterosParser.BgpPeeringConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#otherInterfaceSection.
    def visitOtherInterfaceSection(self, ctx:RouterosParser.OtherInterfaceSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#otherSection.
    def visitOtherSection(self, ctx:RouterosParser.OtherSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#otherConfig.
    def visitOtherConfig(self, ctx:RouterosParser.OtherConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#interfaceName.
    def visitInterfaceName(self, ctx:RouterosParser.InterfaceNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#keyValuePair.
    def visitKeyValuePair(self, ctx:RouterosParser.KeyValuePairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#key.
    def visitKey(self, ctx:RouterosParser.KeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#value.
    def visitValue(self, ctx:RouterosParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RouterosParser#list.
    def visitList(self, ctx:RouterosParser.ListContext):
        return self.visitChildren(ctx)



del RouterosParser