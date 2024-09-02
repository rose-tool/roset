# Generated from IosXr.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .IosXrParser import IosXrParser
else:
    from IosXrParser import IosXrParser

# This class defines a complete listener for a parse tree produced by IosXrParser.
class IosXrListener(ParseTreeListener):

    # Enter a parse tree produced by IosXrParser#config.
    def enterConfig(self, ctx:IosXrParser.ConfigContext):
        pass

    # Exit a parse tree produced by IosXrParser#config.
    def exitConfig(self, ctx:IosXrParser.ConfigContext):
        pass


    # Enter a parse tree produced by IosXrParser#section.
    def enterSection(self, ctx:IosXrParser.SectionContext):
        pass

    # Exit a parse tree produced by IosXrParser#section.
    def exitSection(self, ctx:IosXrParser.SectionContext):
        pass


    # Enter a parse tree produced by IosXrParser#interfaceSection.
    def enterInterfaceSection(self, ctx:IosXrParser.InterfaceSectionContext):
        pass

    # Exit a parse tree produced by IosXrParser#interfaceSection.
    def exitInterfaceSection(self, ctx:IosXrParser.InterfaceSectionContext):
        pass


    # Enter a parse tree produced by IosXrParser#interfaceStatement.
    def enterInterfaceStatement(self, ctx:IosXrParser.InterfaceStatementContext):
        pass

    # Exit a parse tree produced by IosXrParser#interfaceStatement.
    def exitInterfaceStatement(self, ctx:IosXrParser.InterfaceStatementContext):
        pass


    # Enter a parse tree produced by IosXrParser#ipv4Config.
    def enterIpv4Config(self, ctx:IosXrParser.Ipv4ConfigContext):
        pass

    # Exit a parse tree produced by IosXrParser#ipv4Config.
    def exitIpv4Config(self, ctx:IosXrParser.Ipv4ConfigContext):
        pass


    # Enter a parse tree produced by IosXrParser#ipv6Config.
    def enterIpv6Config(self, ctx:IosXrParser.Ipv6ConfigContext):
        pass

    # Exit a parse tree produced by IosXrParser#ipv6Config.
    def exitIpv6Config(self, ctx:IosXrParser.Ipv6ConfigContext):
        pass


    # Enter a parse tree produced by IosXrParser#encapsulationConfig.
    def enterEncapsulationConfig(self, ctx:IosXrParser.EncapsulationConfigContext):
        pass

    # Exit a parse tree produced by IosXrParser#encapsulationConfig.
    def exitEncapsulationConfig(self, ctx:IosXrParser.EncapsulationConfigContext):
        pass


    # Enter a parse tree produced by IosXrParser#shutdownConfig.
    def enterShutdownConfig(self, ctx:IosXrParser.ShutdownConfigContext):
        pass

    # Exit a parse tree produced by IosXrParser#shutdownConfig.
    def exitShutdownConfig(self, ctx:IosXrParser.ShutdownConfigContext):
        pass


    # Enter a parse tree produced by IosXrParser#bgpSection.
    def enterBgpSection(self, ctx:IosXrParser.BgpSectionContext):
        pass

    # Exit a parse tree produced by IosXrParser#bgpSection.
    def exitBgpSection(self, ctx:IosXrParser.BgpSectionContext):
        pass


    # Enter a parse tree produced by IosXrParser#bgpStatement.
    def enterBgpStatement(self, ctx:IosXrParser.BgpStatementContext):
        pass

    # Exit a parse tree produced by IosXrParser#bgpStatement.
    def exitBgpStatement(self, ctx:IosXrParser.BgpStatementContext):
        pass


    # Enter a parse tree produced by IosXrParser#neighbor.
    def enterNeighbor(self, ctx:IosXrParser.NeighborContext):
        pass

    # Exit a parse tree produced by IosXrParser#neighbor.
    def exitNeighbor(self, ctx:IosXrParser.NeighborContext):
        pass


    # Enter a parse tree produced by IosXrParser#neighborStatement.
    def enterNeighborStatement(self, ctx:IosXrParser.NeighborStatementContext):
        pass

    # Exit a parse tree produced by IosXrParser#neighborStatement.
    def exitNeighborStatement(self, ctx:IosXrParser.NeighborStatementContext):
        pass


    # Enter a parse tree produced by IosXrParser#remoteAs.
    def enterRemoteAs(self, ctx:IosXrParser.RemoteAsContext):
        pass

    # Exit a parse tree produced by IosXrParser#remoteAs.
    def exitRemoteAs(self, ctx:IosXrParser.RemoteAsContext):
        pass


    # Enter a parse tree produced by IosXrParser#updateSource.
    def enterUpdateSource(self, ctx:IosXrParser.UpdateSourceContext):
        pass

    # Exit a parse tree produced by IosXrParser#updateSource.
    def exitUpdateSource(self, ctx:IosXrParser.UpdateSourceContext):
        pass


    # Enter a parse tree produced by IosXrParser#ipAddress.
    def enterIpAddress(self, ctx:IosXrParser.IpAddressContext):
        pass

    # Exit a parse tree produced by IosXrParser#ipAddress.
    def exitIpAddress(self, ctx:IosXrParser.IpAddressContext):
        pass


    # Enter a parse tree produced by IosXrParser#otherConfig.
    def enterOtherConfig(self, ctx:IosXrParser.OtherConfigContext):
        pass

    # Exit a parse tree produced by IosXrParser#otherConfig.
    def exitOtherConfig(self, ctx:IosXrParser.OtherConfigContext):
        pass


    # Enter a parse tree produced by IosXrParser#otherSection.
    def enterOtherSection(self, ctx:IosXrParser.OtherSectionContext):
        pass

    # Exit a parse tree produced by IosXrParser#otherSection.
    def exitOtherSection(self, ctx:IosXrParser.OtherSectionContext):
        pass


    # Enter a parse tree produced by IosXrParser#interfaceName.
    def enterInterfaceName(self, ctx:IosXrParser.InterfaceNameContext):
        pass

    # Exit a parse tree produced by IosXrParser#interfaceName.
    def exitInterfaceName(self, ctx:IosXrParser.InterfaceNameContext):
        pass


    # Enter a parse tree produced by IosXrParser#value.
    def enterValue(self, ctx:IosXrParser.ValueContext):
        pass

    # Exit a parse tree produced by IosXrParser#value.
    def exitValue(self, ctx:IosXrParser.ValueContext):
        pass


    # Enter a parse tree produced by IosXrParser#list.
    def enterList(self, ctx:IosXrParser.ListContext):
        pass

    # Exit a parse tree produced by IosXrParser#list.
    def exitList(self, ctx:IosXrParser.ListContext):
        pass



del IosXrParser