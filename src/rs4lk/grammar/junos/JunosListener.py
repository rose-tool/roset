# Generated from Junos.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .JunosParser import JunosParser
else:
    from JunosParser import JunosParser

# This class defines a complete listener for a parse tree produced by JunosParser.
class JunosListener(ParseTreeListener):

    # Enter a parse tree produced by JunosParser#config.
    def enterConfig(self, ctx:JunosParser.ConfigContext):
        pass

    # Exit a parse tree produced by JunosParser#config.
    def exitConfig(self, ctx:JunosParser.ConfigContext):
        pass


    # Enter a parse tree produced by JunosParser#line.
    def enterLine(self, ctx:JunosParser.LineContext):
        pass

    # Exit a parse tree produced by JunosParser#line.
    def exitLine(self, ctx:JunosParser.LineContext):
        pass


    # Enter a parse tree produced by JunosParser#entity.
    def enterEntity(self, ctx:JunosParser.EntityContext):
        pass

    # Exit a parse tree produced by JunosParser#entity.
    def exitEntity(self, ctx:JunosParser.EntityContext):
        pass


    # Enter a parse tree produced by JunosParser#localAsEntity.
    def enterLocalAsEntity(self, ctx:JunosParser.LocalAsEntityContext):
        pass

    # Exit a parse tree produced by JunosParser#localAsEntity.
    def exitLocalAsEntity(self, ctx:JunosParser.LocalAsEntityContext):
        pass


    # Enter a parse tree produced by JunosParser#interfaceEntity.
    def enterInterfaceEntity(self, ctx:JunosParser.InterfaceEntityContext):
        pass

    # Exit a parse tree produced by JunosParser#interfaceEntity.
    def exitInterfaceEntity(self, ctx:JunosParser.InterfaceEntityContext):
        pass


    # Enter a parse tree produced by JunosParser#interfaceIp.
    def enterInterfaceIp(self, ctx:JunosParser.InterfaceIpContext):
        pass

    # Exit a parse tree produced by JunosParser#interfaceIp.
    def exitInterfaceIp(self, ctx:JunosParser.InterfaceIpContext):
        pass


    # Enter a parse tree produced by JunosParser#otherInterfaceConfig.
    def enterOtherInterfaceConfig(self, ctx:JunosParser.OtherInterfaceConfigContext):
        pass

    # Exit a parse tree produced by JunosParser#otherInterfaceConfig.
    def exitOtherInterfaceConfig(self, ctx:JunosParser.OtherInterfaceConfigContext):
        pass


    # Enter a parse tree produced by JunosParser#vlanId.
    def enterVlanId(self, ctx:JunosParser.VlanIdContext):
        pass

    # Exit a parse tree produced by JunosParser#vlanId.
    def exitVlanId(self, ctx:JunosParser.VlanIdContext):
        pass


    # Enter a parse tree produced by JunosParser#interfaceName.
    def enterInterfaceName(self, ctx:JunosParser.InterfaceNameContext):
        pass

    # Exit a parse tree produced by JunosParser#interfaceName.
    def exitInterfaceName(self, ctx:JunosParser.InterfaceNameContext):
        pass


    # Enter a parse tree produced by JunosParser#unit.
    def enterUnit(self, ctx:JunosParser.UnitContext):
        pass

    # Exit a parse tree produced by JunosParser#unit.
    def exitUnit(self, ctx:JunosParser.UnitContext):
        pass


    # Enter a parse tree produced by JunosParser#family.
    def enterFamily(self, ctx:JunosParser.FamilyContext):
        pass

    # Exit a parse tree produced by JunosParser#family.
    def exitFamily(self, ctx:JunosParser.FamilyContext):
        pass


    # Enter a parse tree produced by JunosParser#bgpEntity.
    def enterBgpEntity(self, ctx:JunosParser.BgpEntityContext):
        pass

    # Exit a parse tree produced by JunosParser#bgpEntity.
    def exitBgpEntity(self, ctx:JunosParser.BgpEntityContext):
        pass


    # Enter a parse tree produced by JunosParser#localAddress.
    def enterLocalAddress(self, ctx:JunosParser.LocalAddressContext):
        pass

    # Exit a parse tree produced by JunosParser#localAddress.
    def exitLocalAddress(self, ctx:JunosParser.LocalAddressContext):
        pass


    # Enter a parse tree produced by JunosParser#neighbor.
    def enterNeighbor(self, ctx:JunosParser.NeighborContext):
        pass

    # Exit a parse tree produced by JunosParser#neighbor.
    def exitNeighbor(self, ctx:JunosParser.NeighborContext):
        pass


    # Enter a parse tree produced by JunosParser#remoteAs.
    def enterRemoteAs(self, ctx:JunosParser.RemoteAsContext):
        pass

    # Exit a parse tree produced by JunosParser#remoteAs.
    def exitRemoteAs(self, ctx:JunosParser.RemoteAsContext):
        pass


    # Enter a parse tree produced by JunosParser#asNum.
    def enterAsNum(self, ctx:JunosParser.AsNumContext):
        pass

    # Exit a parse tree produced by JunosParser#asNum.
    def exitAsNum(self, ctx:JunosParser.AsNumContext):
        pass


    # Enter a parse tree produced by JunosParser#otherBgpConf.
    def enterOtherBgpConf(self, ctx:JunosParser.OtherBgpConfContext):
        pass

    # Exit a parse tree produced by JunosParser#otherBgpConf.
    def exitOtherBgpConf(self, ctx:JunosParser.OtherBgpConfContext):
        pass


    # Enter a parse tree produced by JunosParser#groupName.
    def enterGroupName(self, ctx:JunosParser.GroupNameContext):
        pass

    # Exit a parse tree produced by JunosParser#groupName.
    def exitGroupName(self, ctx:JunosParser.GroupNameContext):
        pass


    # Enter a parse tree produced by JunosParser#otherEntity.
    def enterOtherEntity(self, ctx:JunosParser.OtherEntityContext):
        pass

    # Exit a parse tree produced by JunosParser#otherEntity.
    def exitOtherEntity(self, ctx:JunosParser.OtherEntityContext):
        pass


    # Enter a parse tree produced by JunosParser#ipNetwork.
    def enterIpNetwork(self, ctx:JunosParser.IpNetworkContext):
        pass

    # Exit a parse tree produced by JunosParser#ipNetwork.
    def exitIpNetwork(self, ctx:JunosParser.IpNetworkContext):
        pass


    # Enter a parse tree produced by JunosParser#value.
    def enterValue(self, ctx:JunosParser.ValueContext):
        pass

    # Exit a parse tree produced by JunosParser#value.
    def exitValue(self, ctx:JunosParser.ValueContext):
        pass


    # Enter a parse tree produced by JunosParser#list.
    def enterList(self, ctx:JunosParser.ListContext):
        pass

    # Exit a parse tree produced by JunosParser#list.
    def exitList(self, ctx:JunosParser.ListContext):
        pass



del JunosParser