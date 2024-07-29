grammar Junos;

import common;

// Parser rules
config: block* EOF;

block: key '{' (block | key_value_pair | NEWLINE)* '}';
key_value_pair: key value ';';