from functional_parsing_library.parser import Parser, T, ParseResults, CouldNotParse, TokenStream


def some(parser: Parser[TokenStream, T]) -> Parser[TokenStream, list[T]]:
    """
    Parse at zero or more, and as many as possible, matches for parser. For example,
    >>> from functional_parsing_library.strings import char
    >>> some(char('a'))('aaab').result
    ['a', 'a', 'a']
    >>> some(char('a'))('b').result
    []
    """
    def parser_(to_parse: TokenStream) -> ParseResults[TokenStream, list[T]]:
        remainder = to_parse
        result: list[T] = []
        while remainder:
            one_parse = parser(remainder)
            if isinstance(one_parse, CouldNotParse):
                break
            result.append(one_parse.result)
            remainder = one_parse.remainder

        return ParseResults(result=result, remainder=remainder)

    return Parser(parser_)


def many(parser: Parser[TokenStream, T]) -> Parser[TokenStream, list[T]]:
    """
    Parse at least one, and as many as possible, matches for parser. For example,
    >>> from functional_parsing_library.strings import char
    >>> many(char('a'))('aaab').result
    ['a', 'a', 'a']
    """
    return (lambda t, ts: [t, *ts]) * parser & some(parser)
