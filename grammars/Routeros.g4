grammar Routeros;

import common;

config : (section | NEWLINE)* EOF;

section
    : ethInterfaceSection
    | vlanInterfaceSection
    | ipv4AddressSection
    | ipv6AddressSection
    | bgpPeeringSection
    | otherInterfaceSection
    | otherSection
    ;

ethInterfaceSection
    : '/interface ethernet' WORD  (NEWLINE | otherConfig)*
    | '/interface ethernet' (NEWLINE | ethernetConfig)*
    ;

ethernetConfig
    : 'set' ('[' 'find' 'default-name' '=' interfaceName ']' | interfaceName) keyValuePair+
    ;

vlanInterfaceSection
    : '/interface vlan' (NEWLINE | vlanConfig)*
    ;

vlanConfig
    : 'add' (NEWLINE | keyValuePair+)*
    ;

ipv4AddressSection
    :  '/ip address' (NEWLINE | ipv4Config)*
    ;

ipv4Config
    : 'add' (NEWLINE | keyValuePair+)*
    ;

ipv6AddressSection
    :  '/ipv6 address' (NEWLINE | ipv6Config)*
    ;

ipv6Config
    : 'add' (NEWLINE | keyValuePair+)*
    ;

bgpPeeringSection
    :  '/routing bgp connection' (NEWLINE | bgpPeeringConfig)*
    ;

bgpPeeringConfig
    : 'add' (NEWLINE | keyValuePair+)*
    ;

otherInterfaceSection
    : '/interface' WORD+ (NEWLINE | otherConfig)*
    ;

otherSection
    : '/' WORD WORD*? (NEWLINE | otherConfig)*
    ;

otherConfig
    : ('add' | 'set') (keyValuePair+ | WORD | NEWLINE)*
    | 'set' '[' 'find' keyValuePair ']' keyValuePair+
    ;

keyValuePair
    : key '=' value
    ;

key : (WORD | COMPLEX_WORD | COMPLEX_WORD2 | COMPLEX_WORD3);

interfaceName : WORD;
