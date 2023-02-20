from fpcore.ast import ASTNode, Constant, FPCore, Number, Operation, Variable
from utils import add_method


_CONST_MAPPING = {
    "E": lambda name: f"mpfr_const_euler({name}, MPFR_RNDN);",
    "PI": lambda name: f"mpfr_const_pi({name}, MPFR_RNDN);",
}

_UNOP_MAPPING = {
    "-": "mpfr_neg",
    "acos": "mpfr_acos",
    "acosh": "mpfr_acosh",
    "asin": "mpfr_asin",
    "asinh": "mpfr_asinh",
    "atan": "mpfr_atan",
    "atanh": "mpfr_atanh",
    "cbrt": "mpfr_cbrt",
    "ceil": "mpfr_ceil",
    "cos": "mpfr_cos",
    "cosh": "mpfr_cosh",
    "erf": "mpfr_erf",
    "erfc": "mpfr_erfc",
    "exp": "mpfr_exp",
    "exp2": "mpfr_exp2",
    "expm1": "mpfr_expm1",
    "fabs": "mpfr_abs",
    "floor": "mpfr_floor",
    "lgamma": "mpfr_lgamma",
    "log": "mpfr_log",
    "log10": "mpfr_log10",
    "log1p": "mpfr_log1p",
    "log2": "mpfr_log2",
    "sin": "mpfr_sin",
    "sinh": "mpfr_sinh",
    "sqrt": "mpfr_sqrt",
    "tan": "mpfr_tan",
    "tanh": "mpfr_tanh",
    "tgamma": "mpfr_gamma",
}

_BINOP_MAPPING = {
    "-": "mpfr_sub",
    "*": "mpfr_mul",
    "/": "mpfr_div",
    "+": "mpfr_add",
    "fmod": "mpfr_fmod",
    "pow": "mpfr_pow",
    "hypot": "mpfr_hypot",
    "atan2": "mpfr_atan2",
    "fmax": "mpfr_max",
    "fmin": "mpfr_min",
    "fdim": "mpfr_dim",
}

_COMP_MAPPING = {
    "<":  "mpfr_less_p",
    ">":  "mpfr_greater_p",
    "<=":  "mpfr_lessequal_p",
    ">=":  "mpfr_greaterequal_p",
    "==":  "mpfr_equal_p",
    "!=":  "!mpfr_equal_p",
}


@add_method(ASTNode)
def to_mpfr_c(self, *args, **kwargs):
    # Make sure calling to_mpfr_c leads to an error if not overridden
    class_name = type(self).__name__
    msg = "to_mpfr_c not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)


@add_method(Constant)
def to_mpfr_c(self, lines, temps):
    my_name = "generated_{}".format(len(temps))

    try:
        formatter = _CONST_MAPPING[self.source]
    except KeyError:
        raise NotImplementedError(f"Unknown constant '{self.source}'")

    line = formatter(my_name)
    lines.append(line)
    temps.append(my_name)

    return my_name


@add_method(Number)
def to_mpfr_c(self, lines, temps):
    my_name = "generated_{}".format(len(temps))
    line = "  mpfr_set_str({}, \"{}\", 10, MPFR_RNDN);"
    lines.append(line.format(my_name, self.source))
    temps.append(my_name)
    return my_name


@add_method(Variable)
def to_mpfr_c(self, lines, temps):
    return self.source


@add_method(Operation)
def to_mpfr_c(self, lines, temps):
    c_args = [arg.to_mpfr_c(lines, temps) for arg in self.args]
    str_args = ", ".join(c_args)

    my_name = "generated_{}".format(len(temps))

    if len(c_args) == 1 and self.op in _UNOP_MAPPING:
        fname = _UNOP_MAPPING[self.op]
        if self.op == "lgamma":
            ignore = f"ignore_{len(lines)}"
            lines.append(f"  int {ignore};")
            line = f"  {fname}({my_name}, &{ignore}, {str_args}, MPFR_RNDN);"
        else:
            line = f"  {fname}({my_name}, {str_args}, MPFR_RNDN);"
    elif len(c_args) == 2 and self.op in _BINOP_MAPPING:
        fname = _BINOP_MAPPING[self.op]
        line = f"  {fname}({my_name}, {str_args}, MPFR_RNDN);"
    elif len(c_args) == 2 and self.op in _COMP_MAPPING:
        fname = _COMP_MAPPING[self.op]
        line = f"  int {my_name} = {fname}({str_args})"
    else:
        msg = f"Operation not yet supported for MPFR exporter: '{self.op}'"
        raise NotImplementedError(msg)

    lines.append(line)
    temps.append(my_name)

    return my_name


@add_method(FPCore)
def to_mpfr_c(self, out_name):
    lines = list()
    temps = list()
    top_name = self.body.to_mpfr_c(lines, temps)
    temps = temps[:-1]
    lines[-1] = lines[-1].replace(top_name, out_name)
    return lines, temps
