grammar common;

value
    : STRING
    | WORD
    | NUMBER
    | IPV4_ADDRESS
    | IPV6_ADDRESS
    | IPV4_NETWORK
    | IPV6_NETWORK
    | BOOLEAN
    | COMPLEX_WORD
    | COMPLEX_WORD2
    | COMPLEX_WORD3
    | COMMUNITY
    | list
    ;

list : WORD (',' WORD)*;

COMMUNITY: ('0x' NUMBER ':')? NUMBER ':' NUMBER;
WORD : [a-zA-Z0-9*_-]+;
COMPLEX_WORD : '.'? WORD (('.' | '-' | '/' | '+' | ',') | WORD)*;
COMPLEX_WORD2 : '.' WORD;
COMPLEX_WORD3 : WORD ('.' | '-') WORD;
STRING : '"' .*? '"';
NUMBER : [0-9]+;
IPV4_ADDRESS : NUMBER '.' NUMBER '.' NUMBER '.' NUMBER;
IPV6_ADDRESS : HEX_QUAD (':' HEX_QUAD)* | IPV6_SHORTHAND;
IPV6_SHORTHAND : HEX_QUAD (':' HEX_QUAD)* ('::' HEX_QUAD | '::') (':' HEX_QUAD)* | '::';
IPV4_NETWORK : IPV4_ADDRESS '/' NUMBER;
IPV6_NETWORK : IPV6_ADDRESS '/' NUMBER;
BOOLEAN : 'yes' | 'no';

HEX_QUAD : HEX_DIGIT HEX_DIGIT? HEX_DIGIT? HEX_DIGIT?;

HEX_DIGIT : [0-9a-fA-F];

COMMENT : '#' .*? '\r'? '\n' -> skip;
WS : [ \t]+ -> skip;
CONTINUED_LINE : '\\' NEWLINE -> skip;
NEWLINE : '\r'? '\n';
ID : [a-zA-Z][a-zA-Z0-9_-]*;
