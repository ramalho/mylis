from mylis.mytypes import (
    Expression,
    ParserException,
    UnexpectedCloseBrace,
    BraceNeverClosed,
)
from mylis.symbol import Symbol as S
from mylis.parser import tokenize, parse, s_expr

from pytest import mark, raises


@mark.parametrize(
    'source, expected, label',
    [
        ('  7.1 ', ['7.1'], 'number'),
        ('x y', ['x', 'y'], 'symbols'),
        ('(sum 1 2 3)', ['(', 'sum', '1', '2', '3', ')'], 'expression'),
        ('(+ (* 2 100))', ['(', '+', '(', '*', '2', '100', ')', ')'], 'nested expression'),
        ('{if (>= x 0) x 0}', ['{', 'if', '(', '>=', 'x', '0', ')', 'x', '0', '}'], 'alternative brace'),
        ('"a string"', ['"a string"'], 'string'),
        ('"another\\string"', ['"another\\string"'], 'string with escape'),
        (r'"string with \"escaped\" quotes"', [r'"string with \"escaped\" quotes"'], 'escaped quotes'),
    ],
)
def test_tokenize(source: str, expected: Expression, label: str) -> None:
    got = tokenize(source)
    assert got == expected, f'FAILED: {label}'


@mark.parametrize(
    'source, expected',
    [
        ('7', 7),
        ('x', S('x')),
        ('(sum 1 2 3)', [S('sum'), 1, 2, 3]),
        ('(+ (* 2 100) (* 1 10))', [S('+'), [S('*'), 2, 100], [S('*'), 1, 10]]),
        ('99 100', 99),  # parse stops at the first complete expression
        ('(a)(b)', [S('a')]),
    ],
)
def test_parse(source: str, expected: Expression) -> None:
    got = parse(source)
    assert got == expected


@mark.parametrize(
    'source, expected',
    [
        ('(if (< x 0) 0 x)', [S('if'), [S('<'), S('x'), 0], 0, S('x')]),
        ('{if (< x 0) 0 x}', [S('if'), [S('<'), S('x'), 0], 0, S('x')]),
        (
            """ (cond
                    ((> x 0) x)
                    ((= x 0) 0)
                    ((< x 0) (- 0 x)))
            """,
            [
                S('cond'),
                [[S('>'), S('x'), 0], S('x')],
                [[S('='), S('x'), 0], 0],
                [[S('<'), S('x'), 0], [S('-'), 0, S('x')]],
            ],
        ),
        (
            """ {cond
                    [(> x 0) x]
                    [(= x 0) 0]
                    [(< x 0) (- 0 x)]}
            """,
            [
                S('cond'),
                [[S('>'), S('x'), 0], S('x')],
                [[S('='), S('x'), 0], 0],
                [[S('<'), S('x'), 0], [S('-'), 0, S('x')]],
            ],
        ),
    ],
)
def test_parse_mixed_braces(source: str, expected: Expression) -> None:
    got = parse(source)
    assert got == expected


@mark.parametrize(
    'source, expected, match',
    [
        ('', ParserException, 'Empty'),
        ('{', BraceNeverClosed, '{'),
        ('([]', BraceNeverClosed, '('),
        ('(])', UnexpectedCloseBrace, ']'),
        ('([)', UnexpectedCloseBrace, ')'),
    ],
)
def test_parse_malformed(source: str, expected: ParserException, match: str) -> None:
    with raises(expected) as excinfo:  # type: ignore
        parse(source)
    assert match in str(excinfo.value)


@mark.parametrize(
    'obj, expected',
    [
        (0, '0'),
        (1, '1'),
        (False, '#f'),
        (True, '#t'),
        (1.5, '1.5'),
        (S('sin'), 'sin'),
        ('text', '"text"'),
        ([S('+'), 1, 2], '(+ 1 2)'),
        ([S('if'), [S('<'), S('a'), S('b')], 'A', 'B'], '(if (< a b) "A" "B")'),
        ([], '()'),
    ],
)
def test_s_expr(obj: object, expected: str) -> None:
    got = s_expr(obj)
    assert got == expected
    assert parse(expected) == obj
