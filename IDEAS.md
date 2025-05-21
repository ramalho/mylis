# Project ideas

## P-expression syntax

Simple syntax inspired by Python and Scheme.

Prefix notation.

Function call syntax is like Scheme:

```
(print x)

(replace text old new)
```

Same prefix syntax for operators:

```
(+ a b c)
(> x y)
(! n)  # user-defined factorial function
```

Every statement has a keyword prefix.

Keywords are recognized in UPPER_CASE or lower_case,
but the canonical form is UPPER_CASE.

Simple statement syntax is:

```
KEYWORD arg1 ...
```

For example:

```
LET x (* y 2)
```

Block statement syntax is:

```
KEYWORD arg1 ...
    PASS  # one or more statements
```

For example:

```
WHILE (> x 0)
    (print x)
    LET x (-- x)  # decrement
```

Other statement examples:

```
LET l list()

LET low (< x 0)

IF low
    (print 'Low fuel')

DEF (resto m n)
    (- m (* n (// m n)))

DEF (mdc m n)
    IF (= n 0)
        m
    ELSE
        (mdc n (resto m n))

(mdc 18 45)

DEF (! n)
    IF (<= n 2)
        2
    ELSE
        (! n (* n (- n 1)))

DEF (clock)
    (print (now))
    (sleep 1)

```