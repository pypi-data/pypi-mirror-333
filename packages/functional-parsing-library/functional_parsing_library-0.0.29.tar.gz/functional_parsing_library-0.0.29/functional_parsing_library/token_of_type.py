from typing import TypeVar, Any

from functional_parsing_library import Parser, CouldNotParse
from functional_parsing_library.parser import ParseResults

Token = TypeVar('Token')


def token_of_type(token: type[Token]) -> Parser[list[Any], Token]:
    def _parse_token(to_parse: list[Token]) -> ParseResults[list[Token], Token] | CouldNotParse:
        if len(to_parse) == 0:
            return CouldNotParse()
        if isinstance(to_parse[0], token):
            return ParseResults(
                result=to_parse[0],
                remainder=to_parse[1:],
            )
        return CouldNotParse()

    return Parser(_parse_token)
