grammar common;

keyValuePair
    : key '=' value
    ;

key: (WORD | COMPLEX_WORD | COMPLEX_WORD2 | COMPLEX_WORD3);

INTERFACE_NAME : 'ether' NUMBER | 'sfp' NUMBER ('-' NUMBER)* | 'qsfp' NUMBER ('-' NUMBER)*;

value
    : STRING
    | WORD
    | NUMBER
    | IP_ADDRESS
    | IPV6_ADDRESS
    | NETWORK
    | IPV6_NETWORK
    | BOOLEAN
    | COMPLEX_WORD
    | COMPLEX_WORD2
    | COMPLEX_WORD3
    | INTERFACE_NAME
    | COMMUNITY
    | list
    ;

list: WORD (',' WORD)*;

COMMUNITY: ('0x' NUMBER ':')? NUMBER ':' NUMBER;

WORD : [a-zA-Z0-9*_-]+;
COMPLEX_WORD : '.'? WORD (('.' | '-' | '/') | WORD)*;
COMPLEX_WORD2 : '.' WORD;
COMPLEX_WORD3: WORD ('.' | '-') WORD;
STRING : '"' .*? '"';
NUMBER : [0-9]+;
IP_ADDRESS : NUMBER '.' NUMBER '.' NUMBER '.' NUMBER;
IPV6_ADDRESS : HEX_QUAD (':' HEX_QUAD)* | IPV6_SHORTHAND;
IPV6_SHORTHAND : HEX_QUAD (':' HEX_QUAD)* ('::' HEX_QUAD | '::') (':' HEX_QUAD)* | '::';
NETWORK : IP_ADDRESS '/' NUMBER;
IPV6_NETWORK : IPV6_ADDRESS '/' NUMBER;
BOOLEAN : 'yes' | 'no';

HEX_QUAD : HEX_DIGIT HEX_DIGIT? HEX_DIGIT? HEX_DIGIT?;

HEX_DIGIT : [0-9a-fA-F];

COMMENT : '#' .*? '\r'? '\n' -> skip;
WS: [ \t\r\n]+ -> skip;
CONTINUED_LINE: '\\' NEWLINE -> skip;
NEWLINE : '\r'? '\n';
ID: [a-zA-Z][a-zA-Z0-9_-]*;
