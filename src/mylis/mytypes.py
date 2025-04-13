
Symbol = str
type Number = int | float
type Atom = int | float | Symbol
type Expression = Atom | list[Expression]


class InterpreterException(Exception):
    """Generic interpreter exception."""

    def __init__(self, value: str = ''):
        self.value = value

    def __str__(self) -> str:
        msg = self.__class__.__doc__ or ''
        if self.value:
            msg = msg.rstrip('.')
            if "'" in self.value:
                value = self.value
            else:
                value = repr(self.value)
            msg += f': {value}'
        return msg


class ParserException(InterpreterException):
    """Generic exception while parsing."""


class UnexpectedCloseBrace(ParserException):
    """Unexpected close brace."""


class BraceNeverClosed(ParserException):
    """Open brace was never closed."""


class EvaluatorException(InterpreterException):
    """Exception while evaluating."""


class InvalidSyntax(EvaluatorException):
    """Invalid syntax."""


class UndefinedSymbol(EvaluatorException):
    """Undefined symbol."""
