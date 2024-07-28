grammar common;

keyValuePair
    : key '=' value
    ;

key: (WORD | COMPLEX_WORD | COMPLEX_WORD2 | COMPLEX_WORD3);

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