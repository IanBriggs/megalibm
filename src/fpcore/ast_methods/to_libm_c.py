from fpcore.ast import ASTNode, Atom, Constant, FPCore, Operation
from utils import add_method

# TODO: currently only double precision code is produced

_CONST_MAPPING = {
    "E": "M_E",
    "INFINITY": "INFINITY",
    "LN10": "M_LN10",
    "LN2": "M_LN2",
    "LOG10E": "M_LOG10E",
    "LOG2E": "M_LOG2E",
    "M_1_PI": "M_1_PI",
    "M_2_PI": "M_2_PI",
    "M_2_SQRTPI": "M_2_SQRTPI",
    "PI_2": "M_PI_2",
    "PI_4": "M_PI_4",
    "PI": "M_PI",
    "SQRT1_2": "M_SQRT1_2",
    "SQRT2": "M_SQRT2",
}


@add_method(ASTNode)
def to_libm_c(self, *args, **kwargs):
    # Make sure calling to_libm_c leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"to_libm_c not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Atom)
def to_libm_c(self):
    return self.source


@add_method(Constant)
def to_libm_c(self):
    try:
        return _CONST_MAPPING[self.source]
    except KeyError:
        raise NotImplementedError(f"Unknown constant '{self.source}'")


@add_method(Operation)
def to_libm_c(self):
    c_args = [arg.to_libm_c() for arg in self.args]

    if len(c_args) == 1 and self.op in {"+", "-"}:
        return "({}{})".format(self.op, c_args[0])

    if len(c_args) == 2 and self.op in {"+", "-", "*", "/"}:
        return "({}{}{})".format(c_args[0], self.op, c_args[1])

    return "{}({})".format(self.op, ", ".join(c_args))


@add_method(FPCore)
def to_libm_c(self):
    # TODO: create a function signature here
    return self.body.to_libm_c()
