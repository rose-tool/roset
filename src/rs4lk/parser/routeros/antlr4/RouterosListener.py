# Generated from Routeros.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .RouterosParser import RouterosParser
else:
    from RouterosParser import RouterosParser

# This class defines a complete listener for a parse tree produced by RouterosParser.
class RouterosListener(ParseTreeListener):

    # Enter a parse tree produced by RouterosParser#config.
    def enterConfig(self, ctx:RouterosParser.ConfigContext):
        pass

    # Exit a parse tree produced by RouterosParser#config.
    def exitConfig(self, ctx:RouterosParser.ConfigContext):
        pass


    # Enter a parse tree produced by RouterosParser#section.
    def enterSection(self, ctx:RouterosParser.SectionContext):
        pass

    # Exit a parse tree produced by RouterosParser#section.
    def exitSection(self, ctx:RouterosParser.SectionContext):
        pass


    # Enter a parse tree produced by RouterosParser#ethInterfaceSection.
    def enterEthInterfaceSection(self, ctx:RouterosParser.EthInterfaceSectionContext):
        pass

    # Exit a parse tree produced by RouterosParser#ethInterfaceSection.
    def exitEthInterfaceSection(self, ctx:RouterosParser.EthInterfaceSectionContext):
        pass


    # Enter a parse tree produced by RouterosParser#ethernetConfig.
    def enterEthernetConfig(self, ctx:RouterosParser.EthernetConfigContext):
        pass

    # Exit a parse tree produced by RouterosParser#ethernetConfig.
    def exitEthernetConfig(self, ctx:RouterosParser.EthernetConfigContext):
        pass


    # Enter a parse tree produced by RouterosParser#vlanInterfaceSection.
    def enterVlanInterfaceSection(self, ctx:RouterosParser.VlanInterfaceSectionContext):
        pass

    # Exit a parse tree produced by RouterosParser#vlanInterfaceSection.
    def exitVlanInterfaceSection(self, ctx:RouterosParser.VlanInterfaceSectionContext):
        pass


    # Enter a parse tree produced by RouterosParser#vlanConfig.
    def enterVlanConfig(self, ctx:RouterosParser.VlanConfigContext):
        pass

    # Exit a parse tree produced by RouterosParser#vlanConfig.
    def exitVlanConfig(self, ctx:RouterosParser.VlanConfigContext):
        pass


    # Enter a parse tree produced by RouterosParser#ipv4AddressSection.
    def enterIpv4AddressSection(self, ctx:RouterosParser.Ipv4AddressSectionContext):
        pass

    # Exit a parse tree produced by RouterosParser#ipv4AddressSection.
    def exitIpv4AddressSection(self, ctx:RouterosParser.Ipv4AddressSectionContext):
        pass


    # Enter a parse tree produced by RouterosParser#ipv4Config.
    def enterIpv4Config(self, ctx:RouterosParser.Ipv4ConfigContext):
        pass

    # Exit a parse tree produced by RouterosParser#ipv4Config.
    def exitIpv4Config(self, ctx:RouterosParser.Ipv4ConfigContext):
        pass


    # Enter a parse tree produced by RouterosParser#ipv6AddressSection.
    def enterIpv6AddressSection(self, ctx:RouterosParser.Ipv6AddressSectionContext):
        pass

    # Exit a parse tree produced by RouterosParser#ipv6AddressSection.
    def exitIpv6AddressSection(self, ctx:RouterosParser.Ipv6AddressSectionContext):
        pass


    # Enter a parse tree produced by RouterosParser#ipv6Config.
    def enterIpv6Config(self, ctx:RouterosParser.Ipv6ConfigContext):
        pass

    # Exit a parse tree produced by RouterosParser#ipv6Config.
    def exitIpv6Config(self, ctx:RouterosParser.Ipv6ConfigContext):
        pass


    # Enter a parse tree produced by RouterosParser#bgpPeeringSection.
    def enterBgpPeeringSection(self, ctx:RouterosParser.BgpPeeringSectionContext):
        pass

    # Exit a parse tree produced by RouterosParser#bgpPeeringSection.
    def exitBgpPeeringSection(self, ctx:RouterosParser.BgpPeeringSectionContext):
        pass


    # Enter a parse tree produced by RouterosParser#bgpPeeringConfig.
    def enterBgpPeeringConfig(self, ctx:RouterosParser.BgpPeeringConfigContext):
        pass

    # Exit a parse tree produced by RouterosParser#bgpPeeringConfig.
    def exitBgpPeeringConfig(self, ctx:RouterosParser.BgpPeeringConfigContext):
        pass


    # Enter a parse tree produced by RouterosParser#otherInterfaceSection.
    def enterOtherInterfaceSection(self, ctx:RouterosParser.OtherInterfaceSectionContext):
        pass

    # Exit a parse tree produced by RouterosParser#otherInterfaceSection.
    def exitOtherInterfaceSection(self, ctx:RouterosParser.OtherInterfaceSectionContext):
        pass


    # Enter a parse tree produced by RouterosParser#otherSection.
    def enterOtherSection(self, ctx:RouterosParser.OtherSectionContext):
        pass

    # Exit a parse tree produced by RouterosParser#otherSection.
    def exitOtherSection(self, ctx:RouterosParser.OtherSectionContext):
        pass


    # Enter a parse tree produced by RouterosParser#otherConfig.
    def enterOtherConfig(self, ctx:RouterosParser.OtherConfigContext):
        pass

    # Exit a parse tree produced by RouterosParser#otherConfig.
    def exitOtherConfig(self, ctx:RouterosParser.OtherConfigContext):
        pass


    # Enter a parse tree produced by RouterosParser#interfaceName.
    def enterInterfaceName(self, ctx:RouterosParser.InterfaceNameContext):
        pass

    # Exit a parse tree produced by RouterosParser#interfaceName.
    def exitInterfaceName(self, ctx:RouterosParser.InterfaceNameContext):
        pass


    # Enter a parse tree produced by RouterosParser#keyValuePair.
    def enterKeyValuePair(self, ctx:RouterosParser.KeyValuePairContext):
        pass

    # Exit a parse tree produced by RouterosParser#keyValuePair.
    def exitKeyValuePair(self, ctx:RouterosParser.KeyValuePairContext):
        pass


    # Enter a parse tree produced by RouterosParser#key.
    def enterKey(self, ctx:RouterosParser.KeyContext):
        pass

    # Exit a parse tree produced by RouterosParser#key.
    def exitKey(self, ctx:RouterosParser.KeyContext):
        pass


    # Enter a parse tree produced by RouterosParser#value.
    def enterValue(self, ctx:RouterosParser.ValueContext):
        pass

    # Exit a parse tree produced by RouterosParser#value.
    def exitValue(self, ctx:RouterosParser.ValueContext):
        pass


    # Enter a parse tree produced by RouterosParser#list.
    def enterList(self, ctx:RouterosParser.ListContext):
        pass

    # Exit a parse tree produced by RouterosParser#list.
    def exitList(self, ctx:RouterosParser.ListContext):
        pass



del RouterosParser