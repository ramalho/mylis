"""

Symbols are unique by name, and can be compared with `is`:

```
>>> a = Symbol('a')
>>> a_ = Symbol('a')
>>> a is a_
True

```

You can get individual symbols as attributes of the class:

```
>>> b = Symbol('b')
>>> b is Symbol.b
True
>>> Symbol.x
Traceback (most recent call last):
AttributeError: no Symbol named 'x'.

```

If the `name` is not a valid Python identifier, you can always
retrieve the same symbol instance by using the constructor syntax:

```
>>> bang = Symbol('!')
>>> bang is Symbol('!')
True

```

"""

class SymbolMeta(type):

    def __getattr__(cls, name):
        return cls._get_by_name(name)

class Symbol(metaclass=SymbolMeta):
    __slots__ = __match_args__ = 'name',
    _table = {}

    def __new__(cls, name: str):
        table = cls._table
        # not using table.setdefault to avoid the cost of
        # building a Symbol instance for the default argument
        symbol = table.get(name)
        if symbol is None:
            symbol = super().__new__(cls)
            table[name] = symbol
        return symbol

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'Symbol({self.name!r})'

    @classmethod
    def _get_by_name(cls, name):
        try:
            return cls._table[name]
        except KeyError as e:
            raise AttributeError(f'no Symbol named {name!r}.') from e
