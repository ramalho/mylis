import io

from dialogue import Dialogue, normalize  # type: ignore

from mylis.mylis import (
    env_from_args,
    run_file,
    multiline_input,
    multiline_repl,
    QuitRequest,
)
from mylis.mytypes import UnexpectedCloseBrace

from pytest import mark, raises

############### command-line integration

@mark.parametrize(
    'args, global_env',
    [
        ([], {}),
        (['x'], {}),
        (['a=2'], {'a': 2}),
        (
            ['=', 'a=.5', 'flavor=banana', 'max=999', '=='],
            {'a': 0.5, 'flavor': 'banana', 'max': 999},
        ),
    ],
)
def test_env_from_args(args, global_env):
    got = env_from_args(args)
    assert got == global_env


def test_run_file(capsys):
    source = """
    (define (! n)
        (if (<= n 1)
            1
            (* n (! (- n 1)))))
    (display (! x))
    """
    file = io.StringIO(source)
    env = env_from_args(['x=5'])
    got = run_file(file, env)
    assert got is None
    captured = capsys.readouterr()
    assert captured.out == '120\n'


############### multi-line REPL


@mark.parametrize(
    'session, result',
    [
        (
            """
     1|3
     """,
            '3',
        ),
        (
            """
     1|(a
     2| b)
     """,
            '(a\n b)',
        ),
    ],
)
def test_multiline_input(capsys, session, result):
    dlg = Dialogue(session)
    got = multiline_input('1|', '2|', input_fn=dlg.fake_input)
    assert result == got
    captured = capsys.readouterr()
    assert dlg.session == normalize(captured.out)


@mark.parametrize(
    'session',
    [
        """
    >Q
    """,
    ],
)
def test_multiline_input_quit(session):
    dlg = Dialogue(session)
    with raises(QuitRequest):
        multiline_input('>', '', quit_cmd='Q', input_fn=dlg.fake_input)


@mark.parametrize(
    'session, error_str',
    [
        (
            """
     )
     """,
            ')',
        ),
        (
            """
     (a
      b))
     """,
            ' b))',
        ),
        (
            """
     (a
      very long line that will be cut))
     """,
            '…t will be cut))',
        ),
    ],
)
def test_multiline_input_unexpected_close_brace(session, error_str):
    dlg = Dialogue(session)
    with raises(UnexpectedCloseBrace) as excinfo:
        multiline_input('', '', input_fn=dlg.fake_input)
    want_msg = f'Unexpected close brace: {error_str!r}'
    assert want_msg == str(excinfo.value)


def test_repl_quit(capsys):
    dlg = Dialogue('> .q\n')
    multiline_repl(input_fn=dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == normalize(captured.out)


@mark.parametrize(
    'session',
    [
        """
    >
    > .q
    """,
        """
    > (
    ... .q
    """,
        """
    > 3
    3
    > .q
    """,
    ],
)
def test_repl_quit_other_cases(capsys, session):
    dlg = Dialogue(session)
    multiline_repl(input_fn=dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == normalize(captured.out)


def test_repl_gcd_example(capsys):
    session = """
    > (define (mod m n) (- m (* n (quotient m n))))
    > (define (gcd a b) (if (= b 0) a (gcd b (mod a b))))
    > (gcd 84 210)
    42
    """
    dlg = Dialogue(session)
    multiline_repl(input_fn=dlg.fake_input)
    captured = capsys.readouterr()
    assert normalize(captured.out) == dlg.session


def test_repl_gcd_example_multiline(capsys):
    session = """
    > (define (mod m n)
    ... (- m (* n (quotient m n))))
    > (define (gcd a b)
    ... (if (= b 0)
    ...   a
    ...   (gcd b (mod a b))))
    > (gcd 84 210)
    42
    """
    dlg = Dialogue(session)
    multiline_repl(input_fn=dlg.fake_input)
    captured = capsys.readouterr()
    assert dlg.session == normalize(captured.out)
