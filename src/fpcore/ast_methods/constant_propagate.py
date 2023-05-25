
from better_float_cast import better_float_cast
from expect import expect_implemented
from fpcore.ast import ASTNode, Atom, FPCore, Number, Operation
from utils import add_method


def doctester():
    """
    A simple constant propagation pass meant to minimally disturb the ast.
    Currently it:
    * replaces (* 1 x) and (* x 1) with x

    >>> import fpcore
    >>> fpc = fpcore.parse_expr("(* 1 x)")
    >>> str(fpc)
    '(* 1 x)'
    >>> fpc = fpc.constant_propagate()
    >>> str(fpc)
    'x'
    >>> fpc = fpcore.parse_expr("(* 1 1.23)")
    >>> str(fpc)
    '(* 1 1.23)'
    >>> fpc = fpc.constant_propagate()
    >>> str(fpc)
    '1.23'
    >>> fpc = fpcore.parse_expr("(* (- 1) x)")
    >>> str(fpc)
    '(* (- 1) x)'
    >>> fpc = fpc.constant_propagate()
    >>> str(fpc)
    '(- x)'
    """
    # This allows for a docstring that the doctest can find
    raise NotImplementedError("'doctester' should never be called")

@add_method(ASTNode)
def constant_propagate(self, *args, **kwargs):
    expect_implemented("constant_propagate", self)


@add_method(Atom)
def constant_propagate(self):
    return self


@add_method(Operation)
def constant_propagate(self):
    const_args = [a.constant_propagate() for a in self.args]
    match self.op, const_args:
        case "*", [Number(one), other]:
            if better_float_cast(one) == 1.0:
                return other
        case "*", [other, Number(one)]:
            if better_float_cast(one) == 1.0:
                return other
        case "*", [Operation(op="-", args=(Number(one),)), other]:
            if better_float_cast(one) == 1.0:
                return Operation("-", other)
        case "*", [other, Operation(op="-", args=(Number(one),))]:
            if better_float_cast(one) == 1.0:
                return Operation("-", other)
    return Operation(self.op, *tuple(const_args))


@add_method(FPCore)
def constant_propagate(self):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  self.body.constant_propagate())


if __name__ == "__main__":
    import doctest
    doctest.testmod()
