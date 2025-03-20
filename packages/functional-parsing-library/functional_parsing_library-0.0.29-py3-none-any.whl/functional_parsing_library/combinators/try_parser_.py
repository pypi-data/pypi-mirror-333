from dataclasses import dataclass
from typing import Any

from functional_parsing_library.parser import Parser, CouldNotParse, ParseResults, TokenStream


@dataclass(frozen=True)
class TrySucceeded:
    pass


def try_parser(parser: Parser[TokenStream, Any]) -> Parser[TokenStream, TrySucceeded]:
    """
    try_parser(parser) succeeds when parser does, but consumes nothing
    >>> from functional_parsing_library.combinators import try_parser
    >>> from functional_parsing_library.strings import char
    >>> try_parser(char('a'))('a')
    ParseResults(result=TrySucceeded(), remainder='a')
    """
    def parser_function(to_parse: TokenStream) -> ParseResults[TokenStream, TrySucceeded] | CouldNotParse:
        parse_result = parser(to_parse)
        if isinstance(parse_result, CouldNotParse):
            return parse_result
        return ParseResults(TrySucceeded(), to_parse)

    return Parser(parser_function)
