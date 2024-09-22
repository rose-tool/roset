# Generated from IosXr.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .IosXrParser import IosXrParser
else:
    from IosXrParser import IosXrParser

# This class defines a complete generic visitor for a parse tree produced by IosXrParser.

class IosXrVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by IosXrParser#config.
    def visitConfig(self, ctx:IosXrParser.ConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#section.
    def visitSection(self, ctx:IosXrParser.SectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#interfaceSection.
    def visitInterfaceSection(self, ctx:IosXrParser.InterfaceSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#interfaceStatement.
    def visitInterfaceStatement(self, ctx:IosXrParser.InterfaceStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#ipv4Config.
    def visitIpv4Config(self, ctx:IosXrParser.Ipv4ConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#ipv6Config.
    def visitIpv6Config(self, ctx:IosXrParser.Ipv6ConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#encapsulationConfig.
    def visitEncapsulationConfig(self, ctx:IosXrParser.EncapsulationConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#shutdownConfig.
    def visitShutdownConfig(self, ctx:IosXrParser.ShutdownConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#bgpSection.
    def visitBgpSection(self, ctx:IosXrParser.BgpSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#bgpStatement.
    def visitBgpStatement(self, ctx:IosXrParser.BgpStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#neighbor.
    def visitNeighbor(self, ctx:IosXrParser.NeighborContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#neighborStatement.
    def visitNeighborStatement(self, ctx:IosXrParser.NeighborStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#remoteAs.
    def visitRemoteAs(self, ctx:IosXrParser.RemoteAsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#updateSource.
    def visitUpdateSource(self, ctx:IosXrParser.UpdateSourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#ipAddress.
    def visitIpAddress(self, ctx:IosXrParser.IpAddressContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#otherConfig.
    def visitOtherConfig(self, ctx:IosXrParser.OtherConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#otherSection.
    def visitOtherSection(self, ctx:IosXrParser.OtherSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#interfaceName.
    def visitInterfaceName(self, ctx:IosXrParser.InterfaceNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#value.
    def visitValue(self, ctx:IosXrParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IosXrParser#list.
    def visitList(self, ctx:IosXrParser.ListContext):
        return self.visitChildren(ctx)



del IosXrParser