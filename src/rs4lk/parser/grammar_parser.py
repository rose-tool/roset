import logging
import os.path

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker, ParseTreeListener
from antlr4.Lexer import Lexer
from antlr4.Parser import Parser

from ..foundation.configuration.vendor_configuration import VendorConfiguration
from ..foundation.configuration.vendor_configuration_factory import VendorConfigurationFactory
from ..foundation.exceptions import ClassNotFoundError, ConfigError
from ..foundation.parser.parser_factory import LexerFactory, ParserFactory, ListenerFactory


class GrammarParser:
    __slots__ = ['_parsers']

    def __init__(self) -> None:
        self._parsers: dict = {}

    def parse(self, config_path: str, name: str) -> VendorConfiguration:
        full_path = os.path.abspath(config_path)

        logging.info(f"Parsing configuration `{full_path}` with format `{name}`...")

        lexer, parser, listener = self._get_or_new_parser(name)

        input_stream = FileStream(full_path)
        lexer.inputStream = input_stream

        stream = CommonTokenStream(lexer)
        parser.setTokenStream(stream)
        tree = parser.config()

        vendor_config = VendorConfigurationFactory().create_from_name(name)
        vendor_config.path = full_path

        listener.set_vendor_config(vendor_config)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        vendor_config.load()

        return vendor_config

    def _get_or_new_parser(self, name: str) -> (Lexer, Parser, ParseTreeListener):
        if name in self._parsers:
            return self._parsers[name]['lexer'], self._parsers[name]['parsee'], self._parsers[name]['listener']

        try:
            lexer_class = LexerFactory().get_class_from_name(name)
            parser_class = ParserFactory().get_class_from_name(name)
            listener_class = ListenerFactory().get_class_from_name(name)

            lexer = lexer_class(None)
            parser = parser_class(None)
            listener = listener_class()

            self._parsers[name] = {'lexer': lexer, 'parser': parser, 'listener': listener}
        except ClassNotFoundError:
            raise ConfigError(f"Format `{name}` is not supported!")

        return lexer, parser, listener
