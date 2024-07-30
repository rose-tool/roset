# Generated from Junos.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .JunosParser import JunosParser
else:
    from JunosParser import JunosParser

# This class defines a complete generic visitor for a parse tree produced by JunosParser.

class JunosVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by JunosParser#config.
    def visitConfig(self, ctx:JunosParser.ConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#line.
    def visitLine(self, ctx:JunosParser.LineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#entity.
    def visitEntity(self, ctx:JunosParser.EntityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#interface.
    def visitInterface(self, ctx:JunosParser.InterfaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#interfaceIp.
    def visitInterfaceIp(self, ctx:JunosParser.InterfaceIpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#vlanId.
    def visitVlanId(self, ctx:JunosParser.VlanIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#interfaceName.
    def visitInterfaceName(self, ctx:JunosParser.InterfaceNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#family.
    def visitFamily(self, ctx:JunosParser.FamilyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#version.
    def visitVersion(self, ctx:JunosParser.VersionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#bgpConfig.
    def visitBgpConfig(self, ctx:JunosParser.BgpConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#localAddress.
    def visitLocalAddress(self, ctx:JunosParser.LocalAddressContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#neighbor.
    def visitNeighbor(self, ctx:JunosParser.NeighborContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#remoteAs.
    def visitRemoteAs(self, ctx:JunosParser.RemoteAsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#asNum.
    def visitAsNum(self, ctx:JunosParser.AsNumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#otherBgpConf.
    def visitOtherBgpConf(self, ctx:JunosParser.OtherBgpConfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#groupName.
    def visitGroupName(self, ctx:JunosParser.GroupNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#otherConfig.
    def visitOtherConfig(self, ctx:JunosParser.OtherConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#ipNetwork.
    def visitIpNetwork(self, ctx:JunosParser.IpNetworkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#keyValuePair.
    def visitKeyValuePair(self, ctx:JunosParser.KeyValuePairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#key.
    def visitKey(self, ctx:JunosParser.KeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#value.
    def visitValue(self, ctx:JunosParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JunosParser#list.
    def visitList(self, ctx:JunosParser.ListContext):
        return self.visitChildren(ctx)



del JunosParser