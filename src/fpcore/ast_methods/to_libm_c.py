from expect import expect_implemented
from fpcore.ast import ASTNode, Atom, Constant, FPCore, Number, Operation
from utils import add_method
from numeric_types import FP64, FP32, FPDD

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
    },
    FPDD: {
        # error ~= -2.1277171080381768e-33
        "E": "((dd){0x1.5bf0a8b145769p+1, 0x1.4d57ee2b1013ap-53})",
        # error ~= -9.984262454465777e-33
        "LN10": "((dd){0x1.26bb1bbb55516p+1, -0x1.f48ad494ea3e9p-53})",
        # error ~= 5.707708438416212e-34
        "LN2": "((dd){0x1.62e42fefa39efp-1, 0x1.abc9e3b39803fp-56})",
        # error ~= 3.717181233110959e-34
        "LOG10E": "((dd){0x1.bcb7b1526e50ep-2, 0x1.95355baaafad3p-57})",
        # error ~= -1.0614659956117258e-33
        "LOG2E": "((dd){0x1.71547652b82fep+0, 0x1.777d0ffda0d24p-56})",
        # error ~= -1.0721436282893004e-33
        "M_1_PI": "((dd){0x1.45f306dc9c883p-2, -0x1.6b01ec5417056p-56})",
        # error ~= -2.1442872565786008e-33
        "M_2_PI": "((dd){0x1.45f306dc9c883p-1, -0x1.6b01ec5417056p-55})",
        # error ~= -4.765684596693686e-34
        "M_2_SQRTPI": "((dd){0x1.20dd750429b6dp+0, 0x1.1ae3a914fed80p-56})",
        # error ~= -1.4973849048591698e-33
        "PI_2": "((dd){0x1.921fb54442d18p+0, 0x1.1a62633145c07p-54})",
        # error ~= -7.486924524295849e-34
        "PI_4": "((dd){0x1.921fb54442d18p-1, 0x1.1a62633145c07p-55})",
        # error ~= -2.9947698097183397e-33
        "PI": "((dd){0x1.921fb54442d18p+1, 0x1.1a62633145c07p-53})",
        # error ~= 2.0693376543497068e-33
        "SQRT1_2": "((dd){0x1.6a09e667f3bcdp-1, -0x1.bdd3413b26456p-55})",
        # error ~= 4.1386753086994136e-33
        "SQRT2": "((dd){0x1.6a09e667f3bcdp+0, -0x1.bdd3413b26456p-54})",
    }
}


@add_method(ASTNode)
def to_libm_c(self, *args, **kwargs):
    expect_implemented("to_libm_c", self)


@add_method(Atom)
def to_libm_c(self, numeric_type=FP64):
    if numeric_type != FPDD:
        return self.source
    else:
        if self.isDD:
            return self.source
        else:
            return "(dd){" + self.source + ", 0.0}"


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
    if numeric_type in (FP32, FP64):
        c_args = [arg.to_libm_c(numeric_type=numeric_type)
                  for arg in self.args]

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
    # FPDD
    else:
        c_args = [arg.to_libm_c(numeric_type=numeric_type)
                  for arg in self.args]

        if len(c_args) == 1:
            # TODO: add more operations once implemented
            single_op_map = {
                "sqrt": "Sqrt12",
            }
            if self.op in {"+", "-"}:
                neg = [f"{self.op}{x.strip()}" for x in c_args[0].strip(
                    "{}").split(",")]
                return "(dd){" + ", ".join(neg) + "}"
            elif self.op in single_op_map:
                return "{}({})".format(single_op_map[self.op], ", ".join(c_args) + ".hi")
            else:
                raise NotImplementedError(f"Unknown single operation: {self.op}")

        if len(c_args) == 2 and self.op in {"+", "-", "*", "/"}:
            op_map = {
                "+": "Add22",
                "-": "Sub22",
                "*": "Mul22",
                "/": "Div22",
            }
            return f"{op_map[self.op]}({c_args[0]}, {c_args[1]})"
        # TODO: Handle more operations once added
        raise NotImplementedError(f"Unknown operation '{self}'")


@add_method(FPCore)
def to_libm_c(self, numeric_type=FP64):
    # TODO: create a function signature here
    return self.body.to_libm_c(numeric_type=numeric_type)
