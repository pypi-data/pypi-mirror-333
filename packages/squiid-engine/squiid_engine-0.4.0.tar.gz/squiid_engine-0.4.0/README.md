# Squiid Engine Python Bindings

[![codecov](https://codecov.io/gl/ImaginaryInfinity:squiid-calculator/squiid-bindings/graph/badge.svg?token=2YVK2PWQFF)](https://codecov.io/gl/ImaginaryInfinity:squiid-calculator/squiid-bindings)

Python bindings for the engine portion of [Squiid](https://gitlab.com/ImaginaryInfinity/squiid-calculator/squiid) calculator. The engine is the portion of the calculator that actually does the math. This only understands RPN/postfix notation.

More documentation is coming soon, however the source code is strongly typed and well-documented.

## Simple Demo:

```py
import squiid_engine

e = squiid_engine.SquiidEngine()
# this accepts an RPN array
# if you want to accept algebraic input, you can use squiid-parser to accomplish this
res = e.execute_multiple_rpn(["3", "5", "7", "multiply", "add"])

# this should be called after each full expression is run
_ = e.update_previous_answer()

assert not res.has_error()

stack = e.get_stack()
assert stack[0].value == "38"
assert stack[0].bucket_type == squiid_engine.BucketTypes.FLOAT
```

This demo can also be found in [this directory](https://gitlab.com/ImaginaryInfinity/squiid-calculator/squiid-bindings/-/tree/trunk/bindings/python/squiid_engine)

Also see [squiid-parser](https://pypi.org/project/squiid-parser) for parsing algebraic statements into RPN statements to be used in these bindings.
