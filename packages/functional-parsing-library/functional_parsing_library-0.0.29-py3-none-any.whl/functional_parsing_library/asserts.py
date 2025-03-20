from __future__ import annotations

from typing import Any, Generic, Self

from functional_parsing_library.parser import Parser, S, CouldNotParse, ParseResults, FailureReason, TokenStream


class _ParsingSuccessTestResult(Generic[S]):
    def __init__(
        self,
        actual: ParseResults[TokenStream, S],
    ) -> None:
        self._actual = actual

    def with_result(self, expected: S) -> _ParsingSuccessTestResult[S]:
        assert self._actual.result == expected
        return self

    def with_remainder(self, expected: TokenStream) -> _ParsingSuccessTestResult[S]:
        assert self._actual.remainder == expected
        return self


def assert_parsing_succeeds(parser: Parser[TokenStream, S], to_parse: TokenStream) -> _ParsingSuccessTestResult[S]:
    result = parser(to_parse)
    assert not isinstance(result, CouldNotParse)
    return _ParsingSuccessTestResult(
        actual=result,
    )


class _ParsingFailureTestResult:
    def __init__(self, result: CouldNotParse) -> None:
        self._result = result

    def with_reason(self, reason: FailureReason) -> Self:
        assert self._result.reason == reason
        return self


def assert_parsing_fails(parser: Parser[TokenStream, Any], to_parse: TokenStream) -> _ParsingFailureTestResult:
    result = parser(to_parse)
    assert isinstance(result, CouldNotParse)
    return _ParsingFailureTestResult(result)
