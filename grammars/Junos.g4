grammar Junos;

import common;

config: (line | NEWLINE)* EOF;

line: ('set' | 'deactivate') entity;

entity
    : version
    | interface
    | bgpConfig
    | otherConfig
    ;

interface: 'interfaces' (interfaceIp | vlanId | otherConfig);
interfaceIp: interfaceName 'unit' WORD family (WORD+ | 'address' ipNetwork) (value+)?;
vlanId: interfaceName 'unit' WORD 'vlan-id' WORD;

interfaceName: WORD;

family: 'family' ('inet' | 'inet6');

version: 'version' WORD;

bgpConfig: 'protocols bgp group' groupName (localAddress | neighbor | otherBgpConf | remoteAs)? ((family (WORD+) | family)? | (WORD | STRING)+?);

localAddress: 'local-address' ipNetwork;

neighbor: 'neighbor' ipNetwork;

remoteAs: 'peer-as' asNum;

asNum: WORD;

otherBgpConf: WORD+;

groupName: WORD;

otherConfig: (value | family)+;

ipNetwork: (NETWORK | IPV6_NETWORK | WORD | IPV6_ADDRESS);

WORD: [/*.a-zA-Z0-9_-][/*.a-zA-Z0-9_-]*;

