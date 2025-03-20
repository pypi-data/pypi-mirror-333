from typing import Any

from functional_parsing_library.parser import Parser, S, TokenStream


def ignore_left(left: Parser[TokenStream, Any], right: Parser[TokenStream, S]) -> Parser[TokenStream, S]:
    """
    Parses using the left parser, discards the result, and then parses using the right. The `>` operator is overloaded
    to call this function. For example,
    >>> from functional_parsing_library.strings import char
    >>> parser = char('a') > char('b')
    >>> parser('ab').result
    'b'
    """
    return (lambda t, s: s) * left & right
