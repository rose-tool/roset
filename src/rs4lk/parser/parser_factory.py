from antlr4 import ParseTreeListener
from antlr4.Parser import Parser
from antlr4.Lexer import Lexer

from ..foundation.factory.Factory import Factory


class ParserFactory(Factory):

    def __init__(self) -> None:
        self.module_template: str = "rs4lk.parser.%s.antlr4"
        self.name_template: str = "%sParser"

    def get_class_from_os_name(self, os_name: str) -> Parser.__class__:
        return self.get_class((os_name.lower(),), (os_name,))


class LexerFactory(Factory):

    def __init__(self) -> None:
        self.module_template: str = "rs4lk.parser.%s.antlr4"
        self.name_template: str = "%sLexer"

    def get_class_from_os_name(self, os_name: str) -> Lexer.__class__:
        return self.get_class((os_name.lower(),), (os_name,))


class ListenerFactory(Factory):

    def __init__(self) -> None:
        self.module_template: str = "rs4lk.parser.%s"
        self.name_template: str = "%s_custom_listener"

    def get_class_from_os_name(self, os_name: str) -> ParseTreeListener.__class__:
        return self.get_class((os_name.lower(),), (os_name.lower(),))
