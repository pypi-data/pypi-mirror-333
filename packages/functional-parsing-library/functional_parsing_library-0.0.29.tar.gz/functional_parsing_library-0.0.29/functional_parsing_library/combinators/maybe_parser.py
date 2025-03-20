from functional_parsing_library.parser import Parser, U, ParseResults, CouldNotParse, TokenStream


def maybe(parser: Parser[TokenStream, U]) -> Parser[TokenStream, U | None]:
    """
    Transforms a failure to parse by the wrapped parser to a successful parse, with None as its result. For example,
    >>> from functional_parsing_library.strings import char
    >>> maybe(char('a'))('b').result is None
    True
    """
    def maybe_parser(to_parse: TokenStream) -> ParseResults[TokenStream, U | None]:
        result = parser(to_parse)
        if isinstance(result, CouldNotParse):
            return ParseResults(None, to_parse)
        return result

    return Parser(maybe_parser)
