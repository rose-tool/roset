grammar Routeros;
// The entry point for the parser
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

interfaceName : INTERFACE_NAME;

keyValuePair
    : key '=' value
    ;

key: (WORD | COMPLEX_WORD | COMPLEX_WORD2 | COMPLEX_WORD3 | 'local.address');

value
    : STRING
    | NUMBER
    | IP_ADDRESS
    | IPV6_ADDRESS
    | NETWORK
    | IPV6_NETWORK
    | BOOLEAN
    | WORD
    | COMPLEX_WORD
    | COMPLEX_WORD2
    | COMPLEX_WORD3
    | INTERFACE_NAME
    ;

list
    : value (',' value)*
    ;

INTERFACE_NAME : 'ether' NUMBER | 'sfp' NUMBER ('-' NUMBER)* | 'qsfp' NUMBER ('-' NUMBER)*;

WORD : [a-zA-Z0-9_-]+;
COMPLEX_WORD : '.'? WORD (('.' | '-' | '/') | WORD)*;
COMPLEX_WORD2 : '.' WORD;
COMPLEX_WORD3: WORD '.' WORD;
STRING : '"' .*? '"';
NUMBER : [0-9]+;
IP_ADDRESS : [0-9]+ '.' [0-9]+ '.' [0-9]+ '.' [0-9]+;
IPV6_ADDRESS : HEX_QUAD (':' HEX_QUAD){7} | IPV6_SHORTHAND;
IPV6_SHORTHAND : HEX_QUAD (':' HEX_QUAD)* ('::' HEX_QUAD | '::') (':' HEX_QUAD)*;
NETWORK : IP_ADDRESS '/' [0-9]+;
IPV6_NETWORK : IPV6_ADDRESS '/' [0-9]+;
BOOLEAN : 'yes' | 'no';

fragment HEX_QUAD : HEX_4 | HEX_3 | HEX_2 | HEX_1;
fragment HEX_4 : HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT;
fragment HEX_3 : HEX_DIGIT HEX_DIGIT HEX_DIGIT;
fragment HEX_2 : HEX_DIGIT HEX_DIGIT;
fragment HEX_1 : HEX_DIGIT;

fragment HEX_DIGIT : [0-9a-fA-F];

COMMENT : '#' .*? '\r'? '\n' -> skip;
WS : [ \t]+ -> skip;
CONTINUED_LINE: '\\' NEWLINE -> skip;
NEWLINE : '\r'? '\n';