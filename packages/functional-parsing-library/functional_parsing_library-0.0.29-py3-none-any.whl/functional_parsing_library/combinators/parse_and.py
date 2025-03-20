from typing import TypeVarTuple, Callable, overload, TypeVar, cast

from functional_parsing_library.parser import Parser, S, T, ParseResults, CouldNotParse, MappedParser, TokenStream

Ts = TypeVarTuple('Ts')


U = TypeVar('U')


@overload
def parse_and(left: MappedParser[TokenStream, S, T], right: Parser[TokenStream, T]) -> Parser[TokenStream, S]:
    pass


@overload
def parse_and(left: MappedParser[TokenStream, S, T, U, *Ts], right: Parser[TokenStream, T]) -> MappedParser[TokenStream, S, U, *Ts]:
    pass


def parse_and(
    left: MappedParser[TokenStream, S, T] | MappedParser[TokenStream, S, T, U, *Ts],
    right: Parser[TokenStream, T],
) -> Parser[TokenStream, S] | MappedParser[TokenStream, S, U, *Ts]:
    """
    Is used to combine parsers p and q to a parser which first parses using p and then the remainder using q. The `&`
    operator is overloaded to make use of this function.

    If p is of type Parser[TokenStream, T] and q is of type Parser[S], then it is not obvious what type p & q should have. For example,
    it could be of type Parser[TokenStream, tuple[T, S]], it could be of type Parser[list[T | S]], and so on. Therefore, `&` can only
    be used in combination with a callable f of type `Callable[[T, S], U]` which specifies how to combine the result of
    p with the result of q. Writing `p & q` without applying such a function will raise a TypeError.

    For example,
    >>> from functional_parsing_library.strings import char
    >>> a, b = char('a'), char('b')
    >>> plus = lambda x, y: x + ' and ' + y
    >>> parser = plus * a & b
    >>> parser('ab').result
    'a and b'

    This works with callables of more than two arguments as well:
    >>> c = char('c')
    >>> triple_plus = lambda x, y, z: x + y + z
    >>> parser = triple_plus * a & b & c
    >>> parser('abc').result
    'abc'
    """
    if left.is_multi_arg:
        multi_arg_left = cast(MappedParser[TokenStream, S, T, U, *Ts], left)
        return _parse_and_for_multiple_arguments(multi_arg_left, right)

    single_arg_left = cast(MappedParser[TokenStream, S, T], left)
    return _parse_and_for_single_argument(single_arg_left, right)


def _parse_and_for_multiple_arguments(
    left: MappedParser[TokenStream, S, T, U, *Ts],
    right: Parser[TokenStream, T],
) -> MappedParser[TokenStream, S, U, *Ts]:
    def parser_(to_parse: TokenStream) -> ParseResults[TokenStream, Callable[[U, *Ts], S]] | CouldNotParse:
        result = _parse_left_and_then_right(left, right, to_parse)
        if isinstance(result, CouldNotParse):
            return result
        right_result, parsed_function = result

        return ParseResults(
            result=lambda *ts: parsed_function(right_result.result, *ts),
            remainder=right_result.remainder
        )

    return MappedParser(parser_)


def _parse_and_for_single_argument(
    left: MappedParser[TokenStream, S, T],
    right: Parser[TokenStream, T],
) -> Parser[TokenStream, S]:
    def parser(to_parse: TokenStream) -> ParseResults[TokenStream, S] | CouldNotParse:
        result = _parse_left_and_then_right(left, right, to_parse)
        if isinstance(result, CouldNotParse):
            return result
        right_result, parsed_function = result

        return ParseResults(
            result=parsed_function(right_result.result),
            remainder=right_result.remainder
        )

    return Parser(parser)


def _parse_left_and_then_right(
    left: MappedParser[TokenStream, S, T, *Ts],
    right: Parser[TokenStream, T],
    to_parse: TokenStream,
) -> tuple[ParseResults[TokenStream, T], Callable[[T, *Ts], S]] | CouldNotParse:
    left_result = left(to_parse)
    if isinstance(left_result, CouldNotParse):
        return left_result

    right_result = right(left_result.remainder)
    if isinstance(right_result, CouldNotParse):
        return right_result

    return right_result, left_result.result
