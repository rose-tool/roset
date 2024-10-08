grammar Junos;

import common;

config : (line | NEWLINE)* EOF;

line : ('set' | 'deactivate') entity;

entity
    : interfaceEntity
    | localAsEntity
    | bgpEntity
    | otherEntity
    ;

localAsEntity : 'routing-options autonomous-system' WORD;

interfaceEntity : 'interfaces' interfaceName (interfaceIp | vlanId | otherInterfaceConfig) NEWLINE;
interfaceIp : unit family 'address' ipNetwork value*;
otherInterfaceConfig : (unit family)? value*;
vlanId : unit 'vlan-id' WORD;
interfaceName : WORD;
unit : 'unit ' WORD;
family : 'family' ('inet' | 'inet6');

bgpEntity : 'protocols bgp group' groupName (localAddress | neighbor | otherBgpConf | remoteAs)? ((family (WORD+) | family)? | (WORD | STRING)+?);
localAddress : 'local-address' ipNetwork;
neighbor : 'neighbor' ipNetwork;
remoteAs : 'peer-as' asNum;
asNum : WORD;
otherBgpConf : WORD (WS WORD)+;
groupName : WORD;

otherEntity : (family | value)+;

ipNetwork : (IPV4_NETWORK | IPV6_NETWORK | WORD | IPV6_ADDRESS);

WORD : [/*.a-zA-Z0-9_-][/*.a-zA-Z0-9_-]*;

