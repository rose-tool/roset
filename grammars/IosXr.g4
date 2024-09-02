grammar IosXr;

import common;

config : (section | NEWLINE)* EOF;

section
    : interfaceSection
    | bgpSection
    | otherSection
    ;

interfaceSection : 'interface' 'preconfigure'? interfaceName otherConfig NEWLINE interfaceStatement*;
interfaceStatement
    : ipv4Config NEWLINE
    | ipv6Config NEWLINE
    | encapsulationConfig NEWLINE
    | shutdownConfig NEWLINE
    | otherConfig NEWLINE
    ;
ipv4Config : 'ipv4 address' WORD WORD;
ipv6Config : 'ipv6 address' IPV6_NETWORK;
encapsulationConfig : 'encapsulation dot1q' WORD ('second-dot1q' WORD)?;
shutdownConfig : 'shutdown';

bgpSection : 'router bgp' WORD NEWLINE bgpStatement*;
bgpStatement
    : neighbor
    | otherConfig NEWLINE
    ;
neighbor : 'neighbor' ipAddress NEWLINE neighborStatement*;
neighborStatement
    : remoteAs
    | updateSource
    | otherConfig NEWLINE
    ;
remoteAs : 'remote-as' WORD NEWLINE;
updateSource : 'update-source' interfaceName NEWLINE;

ipAddress : (WORD | IPV4_ADDRESS | IPV6_ADDRESS);

otherConfig : value*;

otherSection : value+;

WORD : [/*.a-zA-Z0-9_-][/*.a-zA-Z0-9_-]*;
COMMENT : ('#' | '!') .*? '\r'? '\n' -> skip;

interfaceName : WORD;