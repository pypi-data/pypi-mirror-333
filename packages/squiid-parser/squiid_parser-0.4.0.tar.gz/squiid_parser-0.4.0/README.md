# Squiid Parser Python Bindings

[![codecov](https://codecov.io/gl/ImaginaryInfinity:squiid-calculator/squiid-bindings/graph/badge.svg?token=2YVK2PWQFF)](https://codecov.io/gl/ImaginaryInfinity:squiid-calculator/squiid-bindings)

Python bindings for the parser portion of [Squiid](https://gitlab.com/ImaginaryInfinity/squiid-calculator/squiid) calculator. The parser is used to convert algebraic/infix notation to postfix notation that the [engine](https://pypi.org/project/squiid-engine) can evaluate.

More documentation is coming soon, however the source code is strongly typed and well-documented.

## Simple Demo:

```py
import squiid_parser

p = squiid_parser.SquiidParser()
result = p.parse("(3+5*7)")

assert result == ["3", "5", "7", "*", "+"]

# squiid currently doesn't support symbols, but rather commands
# iterate through the list and convert symbols to commands
for index, value in enumerate(result):
    if value == "*":
        result[index] = "multiply"
    elif value == "+":
        result[index] = "add"
    elif value == "-":
        result[index] = "subtract"
    elif value == "/":
        result[index] = "divide"
    elif value == "^":
        result[index] = "power"
    elif value == "%":
        result[index] = "mod"

assert result == ["3", "5", "7", "multiply", "add"]

# and now pass this array to the engine...
```

This demo can also be found in [this directory](https://gitlab.com/ImaginaryInfinity/squiid-calculator/squiid-bindings/-/tree/trunk/bindings/python/squiid_parser)

Also see [squiid-engine](https://pypi.org/project/squiid-engine) for evaluating RPN expressions.
