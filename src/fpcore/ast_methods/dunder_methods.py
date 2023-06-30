# Magic methods to integrate FPCore with python

import re
from better_float_cast import better_float_cast
from expect import expect_implemented
from fpcore.ast import ASTNode, Expr, FPCore, Number, Operation, Property
from utils import add_method, Logger

logger = Logger(level=Logger.EXTRA)


def cast_to_astnode(x):
    """Transforms the input to an ASTNode object

    For python's ints and floats the precision is noted
    >>> cast_to_astnode(1337)
    Number('1337').add_properties([Property('precision', 'integer')])
    >>> cast_to_astnode(0.1)
    Number('0.1').add_properties([Property('precision', 'binary64')])

    A top level FPCore object will have its internals scraped out
    >>> fpc = FPCore("empty", list(), list(), Number("42"))
    >>> cast_to_astnode(fpc)
    Number('42')

    Other ASTNodes will just be passed through
    >>> c = Operation("+", Number("40"), Number("2"))
    >>> cast_to_astnode(c)
    Operation('+', Number('40'), Number('2'))

    Anything else is assumed to be numeric and processed with `str`
    >>> import mpmath
    >>> cast_to_astnode(mpmath.mpf("4.000"))
    Number('4.0')
    """
    typ = type(x)
    if typ == FPCore:
        logger.dlog("Extracting body from FPCore: {}", x)
        x = x.body
    elif typ == int:
        x = Number(str(x))
        x.add_properties([Property("precision", "integer")])
    elif typ == float:
        x = Number(str(x))
        x.add_properties([Property("precision", "binary64")])
    elif not issubclass(typ, ASTNode):
        sx = str(x)
        try:
            better_float_cast(sx)
        except ValueError:
            raise ValueError(f"Non-numeric value: {sx}")
        logger.dlog("Casting {} to Number type: {}", typ, sx)
        x = Number(sx)
    return x


def add_unary_dunder(dunder_name, fpcore_name):
    def default(self, *args, **kwargs):
        expect_implemented(dunder_name, self)
    setattr(ASTNode, dunder_name, default)

    if fpcore_name == "":
        def expr(self):
            return self
        def fpc(self):
            return self
    else:
        def expr(self):
            return Operation(fpcore_name, self)
        def fpc(self):
            return FPCore(self.name, self.arguments, self.properties,
                          Operation(fpcore_name, self.body))
    setattr(Expr, dunder_name, expr)
    setattr(FPCore, dunder_name, fpc)


def add_binary_dunder(dunder_name, fpcore_name):
    def default(self, *args, **kwargs):
        expect_implemented("dunder_name", self)
    setattr(ASTNode, dunder_name, default)

    def expr(self, other):
        return Operation(fpcore_name, self, cast_to_astnode(other))
    setattr(Expr, dunder_name, expr)

    def rexpr(self, other):
        return Operation(fpcore_name, cast_to_astnode(other), self)
    setattr(Expr, dunder_name.replace("__", "__r", 1), rexpr)

add_unary_dunder("__pos__", "")
add_unary_dunder("__neg__", "-")
add_unary_dunder("__abs__", "fabs")
add_unary_dunder("__round__", "round")
add_unary_dunder("__floor__", "floor")
add_unary_dunder("__ceil__", "ceil")
add_unary_dunder("__trunc__", "trunc")

add_binary_dunder("__add__", "+")
add_binary_dunder("__sub__", "-")
add_binary_dunder("__mul__", "*")
add_binary_dunder("__truediv__", "/")
add_binary_dunder("__pow__", "pow") # TODO: lacks support for math.pow

# Lack of support due to:
# https://docs.python.org/3/reference/datamodel.html
# Note that __pow__() should be defined to accept an optional third argument if
# the ternary version of the built-in pow() function is to be supported.

# This is not the best design, but just eval comparison operators instead of
#  building an ast
def eager_eval_dunder(dunder_name, op_lambda):
    def default(self, *args, **kwargs):
        expect_implemented(dunder_name, self)
    setattr(ASTNode, dunder_name, default)

    def expr(self, other):
        return op_lambda(float(self), float(other))
    setattr(Expr, dunder_name, expr)

eager_eval_dunder("__lt__", lambda a, b: a < b)
eager_eval_dunder("__le__", lambda a, b: a <= b)
eager_eval_dunder("__gt__", lambda a, b: a > b)
eager_eval_dunder("__ge__", lambda a, b: a >= b)


def dummy():
    """
    This function is here just to allow testing using the doctest system

    >>> import math
    >>> import mpmath
    >>> from fpcore.base_ast import Constant, Variable

    Try all unary dunder methods

    >>> x = Variable("x")
    >>> +x
    Variable('x')
    >>> -x
    Operation('-', Variable('x'))
    >>> abs(x)
    Operation('fabs', Variable('x'))
    >>> round(x)
    Operation('round', Variable('x'))
    >>> math.floor(x)
    Operation('floor', Variable('x'))
    >>> math.ceil(x)
    Operation('ceil', Variable('x'))
    >>> math.trunc(x)
    Operation('trunc', Variable('x'))

    Try all binary dunder methods with an fpcore left hand side

    >>> c = Constant("PI")
    >>> c + 1
    Operation('+', Constant('PI'), Number('1').add_properties([Property('precision', 'integer')]))
    >>> c + 42.0
    Operation('+', Constant('PI'), Number('42.0').add_properties([Property('precision', 'binary64')]))
    >>> c * mpmath.mpf("0")
    Operation('*', Constant('PI'), Number('0.0'))
    >>> c / mpmath.mpf("10")
    Operation('/', Constant('PI'), Number('10.0'))
    >>> str(c ** 2)
    '(pow PI (! :precision integer 2))'

    Try all binary dunder methods with an fpcore right hand side

    >>> n = Number("1337")
    >>> 1 + n
    Operation('+', Number('1').add_properties([Property('precision', 'integer')]), Number('1337'))
    >>> 42.0 + n
    Operation('+', Number('42.0').add_properties([Property('precision', 'binary64')]), Number('1337'))
    >>> mpmath.mpf("0") * n
    Operation('*', Number('0.0'), Number('1337'))
    >>> mpmath.mpf("10") / n
    Operation('/', Number('10.0'), Number('1337'))
    >>> str(2 ** n)
    '(pow (! :precision integer 2) 1337)'
    """
    raise NotImplementedError("'dummy' should never be called")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
