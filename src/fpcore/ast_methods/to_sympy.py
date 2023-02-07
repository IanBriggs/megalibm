from fpcore.ast import ASTNode, Constant, FPCore, Number, Operation, Variable
from utils import add_method
import sympy

_CONST_MAPPING = {
    "E": sympy.E,
    "PI": sympy.pi,
}

_UNOP_MAPPING = {
    "-": lambda x: -x,  # leverage sympy's operator overloading
    "acos": sympy.acos,
    "acosh": sympy.acosh,
    "asin": sympy.asin,
    "asinh": sympy.asinh,
    "atan": sympy.atan,
    "atanh": sympy.atanh,
    "cbrt": sympy.cbrt,
    "ceil": sympy.ceiling,
    "cos": sympy.cos,
    "cosh": sympy.cosh,
    "erf": sympy.erf,
    "erfc": sympy.erfc,
    "exp": sympy.exp,
    # "exp2": ,
    # "expm1": ,
    "fabs": sympy.Abs,
    "floor": sympy.floor,
    "lgamma": sympy.loggamma,
    "log": sympy.log,
    # "log10": ,
    # "log1p": ,
    # "log2": ,
    "sin": sympy.sin,
    "sinh": sympy.sinh,
    "sqrt": sympy.sqrt,
    "tan": sympy.tan,
    "tanh": sympy.tanh,
    "tgamma": sympy.gamma,
}

_BINOP_MAPPING = {
    "-": lambda a, b: a - b,  # leverage sympy's operator overloading
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
    "+": lambda a, b: a + b,
    # "fmod": ,
    "pow": sympy.Pow,
    # "hypot": ,
    "atan2": sympy.atan2,
    # "fmax": ,
    # "fmin": ,
    # "fdim": ,
}

_COMP_MAPPING = {
    # "<": ,
    # ">": ,
    # "<=": ,
    # ">=": ,
    # "==": ,
    # "!=": ,
}



@add_method(ASTNode)
def to_sympy(self, *args, **kwargs):
    # Make sure calling to_sympy leads to an error if not overridden
    class_name = type(self).__name__
    msg = "to_sympy not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)


@add_method(Constant)
def to_sympy(self):
    try:
        return _CONST_MAPPING[self.source]
    except KeyError:
        raise NotImplementedError(f"Unknown constant '{self.source}'")


@add_method(Variable)
def to_sympy(self):
    return sympy.symbols(self.source)


@add_method(Number)
def to_sympy(self):
    return sympy.Number(self.source)


@add_method(Operation)
def to_sympy(self):
    f_args = [arg.to_sympy() for arg in self.args]

    if len(f_args) == 1 and self.op in _UNOP_MAPPING:
        return _UNOP_MAPPING[self.op](f_args[0])

    if len(f_args) == 2 and self.op in _BINOP_MAPPING:
        return _BINOP_MAPPING[self.op](f_args[0], f_args[1])

    msg = f"Operation not yet supported for to_sympy: '{self.op}'"
    raise NotImplementedError(msg)


@add_method(FPCore)
def to_sympy(self):
    return self.body.to_sympy()
