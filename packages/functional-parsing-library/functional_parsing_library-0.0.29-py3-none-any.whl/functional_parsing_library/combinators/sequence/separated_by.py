from typing import Any

from functional_parsing_library.combinators.sequence.many import some
from functional_parsing_library.parser import Parser, T, TokenStream, ParseResults


def separated_by(parser: Parser[TokenStream, T], separator: Parser[TokenStream, Any]) -> Parser[TokenStream, list[T]]:
    """
    Matches one or more (and as many as possible) matches of parser, separated by matches for separator.
    For example,
    >>> from functional_parsing_library.strings import char
    >>> parser = separated_by(char('a'), char(','))
    >>> parser('a,a,a').result
    ['a', 'a', 'a']
    """
    return (lambda t, ts: [t, *ts]) * parser & some(separator > parser)


def _nothing_parser(to_parse: TokenStream) -> ParseResults[TokenStream, None]:
    return ParseResults(
        result=None,
        remainder=to_parse,
    )


nothing: Parser[Any, None] = Parser(_nothing_parser)


def some_separated_by(parser: Parser[TokenStream, T], separator: Parser[TokenStream, Any]) -> Parser[TokenStream, list[T]]:
    """
    Matches zero or more (and as many as possible) matches of parser, separated by matches for separator.
    For example,
    >>> from functional_parsing_library.strings import char
    >>> parser = some_separated_by(char('a'), char(','))
    >>> parser('a,a,a').result
    ['a', 'a', 'a']
    >>> parser('shibby').result
    []
    """
    return separated_by(parser, separator) | ((lambda x: []) * nothing)
