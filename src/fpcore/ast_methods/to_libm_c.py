from expect import expect_implemented
from fpcore.ast import ASTNode, Atom, Constant, FPCore, Number, Operation
from utils import add_method
from numeric_types import FP64, FP32

_CONST_MAPPING = {
    FP32: {
        "E": "0x1.5bf0a8p+1f",
        "INFINITY": "((float) INFINITY)",  # requires math.h
        "LN10": "0x1.26bb1cp+1f",
        "LN2": "0x1.62e43p-1f",
        "LOG10E": "0x1.bcb7b2p-2f",
        "LOG2E": "0x1.715476p+0f",
        "M_1_PI": "0x1.45f306p-2f",
        "M_2_PI": "0x1.45f306p-1f",
        "M_2_SQRTPI": "0x1.20dd76p+0f",
        "PI_2": "0x1.921fb6p+0f",
        "PI_4": "0x1.921fb6p-1f",
        "PI": "0x1.921fb6p+1f",
        "SQRT1_2": "0x1.6a09e6p-1f",
        "SQRT2": "0x1.6a09e6p+0f",
    },
    FP64: {
        "E": "0x1.5bf0a8b145769p+1",
        "INFINITY": "INFINITY",  # requires math.h
        "LN10": "0x1.26bb1bbb55516p+1",
        "LN2": "0x1.62e42fefa39efp-1",
        "LOG10E": "0x1.bcb7b1526e50ep-2",
        "LOG2E": "0x1.71547652b82fep+0",
        "M_1_PI": "0x1.45f306dc9c883p-2",
        "M_2_PI": "0x1.45f306dc9c883p-1",
        "M_2_SQRTPI": "0x1.20dd750429b6dp+0",
        "PI_2": "0x1.921fb54442d18p+0",
        "PI_4": "0x1.921fb54442d18p-1",
        "PI": "0x1.921fb54442d18p+1",
        "SQRT1_2": "0x1.6a09e667f3bcdp-1",
        "SQRT2": "0x1.6a09e667f3bcdp+0",
    }
}


@add_method(ASTNode)
def to_libm_c(self, *args, **kwargs):
    expect_implemented("to_libm_c", self)


@add_method(Atom)
def to_libm_c(self, numeric_type=FP64):
    return self.source


@add_method(Number)
def to_libm_c(self, numeric_type=FP64):
    return numeric_type.num_to_str(self.source)


@add_method(Constant)
def to_libm_c(self, numeric_type=FP64):
    try:
        return _CONST_MAPPING[numeric_type][self.source]
    except KeyError:
        if numeric_type not in _CONST_MAPPING:
            raise NotImplementedError(f"Unknown numeric type '{numeric_type}'")
        raise NotImplementedError(f"Unknown constant '{self.source}'")


@add_method(Operation)
def to_libm_c(self, numeric_type=FP64):
    c_args = [arg.to_libm_c(numeric_type=numeric_type) for arg in self.args]

    if len(c_args) == 1 and self.op in {"+", "-"}:
        return "({}{})".format(self.op, c_args[0])

    if len(c_args) == 2 and self.op in {"+", "-", "*", "/"}:
        return "({} {} {})".format(c_args[0], self.op, c_args[1])

    if numeric_type == FP64:
        return "{}({})".format(self.op, ", ".join(c_args))
    elif numeric_type == FP32:
        return "{}f({})".format(self.op, ", ".join(c_args))
    else:
        raise NotImplementedError(f"Unknown numeric type '{numeric_type}'")


@add_method(FPCore)
def to_libm_c(self, numeric_type=FP64):
    # TODO: create a function signature here
    return self.body.to_libm_c()
