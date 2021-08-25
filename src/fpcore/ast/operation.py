

from .expr import Expr
from .ast_errors import ArityError
from .ast_utils import list_to_str, list_to_repr

from fpcore.lexer import FPCoreLexer
from utils import Logger


logger = Logger()




class Operation(Expr):
    def __init__(self, op, *args):
        super().__init__()
        self.op = op
        self.args = args

    def __str__(self):
        format_str = super().__str__()
        this_str = "({} {})".format(self.op, list_to_str(self.args))
        return format_str.format(this_str)

    def __repr__(self):
        format_repr = super().__repr__()
        this_repr = "{}, {}".format(repr(self.op), list_to_repr(self.args))
        return format_repr.format(this_repr)

    def __eq__(self, other):
        return (type(other) == Operation
                and self.op == other.op
                and all(a_arg == o_arg for a_arg, o_arg
                        in zip(self.args, other.args)))

    def __add__(self, other):
        return Operation("+", self, other)

    def __sub__(self, other):
        return Operation("-", self, other)

    def __neg__(self):
        return Operation("-", self)

    def __float__(self):
        f_args = [float(arg) for arg in self.args]

        if len(f_args) == 1:
            mapping = {
                "-" : (lambda x: -x)
            }
            return mapping[self.op](f_args[0])

        if len(f_args) == 2:
            mapping = {
                "+" : (lambda x, y : x+y), 
                "-" : (lambda x, y : x-y), 
                "*" : (lambda x, y : x*y), 
                "/" : (lambda x, y : x/y), 
            }
            return mapping[self.op](f_args[0], f_args[1])

        msg = "could not convert Operation to float: '{}'".format(repr(self))
        raise ValueError(msg)

    def substitute(self, old, new):
        if self == old:
            return new
        new_args = [arg.substitute(old, new) for arg in self.args]
        return Operation(self.op, *new_args)

    def to_wolfram(self):
        w_args = [arg.to_wolfram() for arg in self.args]

        if len(w_args) == 1 and self.op in {"+", "-"}:
            return "({}{})".format(self.op, w_args[0])

        if len(w_args) == 2 and self.op in {"+", "-", "*", "/"}:
            return "({}{}{})".format(w_args[0], self.op, w_args[1])

        mapping = {
            "sin" : "Sin",
            "cos" : "Cos",
            "tan" : "Tan",
            "asin" : "ArcSin",
            "acos" : "ArcCos",
            "atan" : "ArcTan",
        }
        op = mapping.get(self.op, self.op)
        return "{}[{}]".format(op, ", ".join(w_args))

    def to_sollya(self):
        s_args = [arg.to_sollya() for arg in self.args]

        if len(s_args) == 1 and self.op in {"+", "-"}:
            return "({}{})".format(self.op, s_args[0])

        if len(s_args) == 2 and self.op in {"+", "-", "*", "/"}:
            return "({}{}{})".format(s_args[0], self.op, s_args[1])

        return "{}({})".format(self.op, ", ".join(s_args)) 

    def to_c(self):
        c_args = [arg.to_c() for arg in self.args]

        if len(c_args) == 1 and self.op in {"+", "-"}:
            return "({}{})".format(self.op, c_args[0])

        if len(c_args) == 2 and self.op in {"+", "-", "*", "/"}:
            return "({}{}{})".format(c_args[0], self.op, c_args[1])

        return "{}({})".format(self.op, ", ".join(c_args)) 

    def to_libm_c(self):
        c_args = [arg.to_libm_c() for arg in self.args]

        if len(c_args) == 1 and self.op in {"+", "-"}:
            return "({}{})".format(self.op, c_args[0])

        if len(c_args) == 2 and self.op in {"+", "-", "*", "/"}:
            return "({}{}{})".format(c_args[0], self.op, c_args[1])

        return "{}({})".format(self.op, ", ".join(c_args)) 

    def to_mpfr_c(self, lines, temps):
        mpfr_functions = {
            "sin" : "mpfr_sin",
            "cos" : "mpfr_cos",
            "tan" : "mpfr_tan",
            "+" : "mpfr_add",
            "-" : "mpfr_sub",
            "*" : "mpfr_mul",
            "/" : "mpfr_div",
            }
        c_args = [arg.to_mpfr_c(lines, temps) for arg in self.args]

        my_name = "generated_{}".format(len(temps))

        fname = mpfr_functions[self.op]

        line = ("  " + fname + "(" + my_name + ", "
                + ", ".join(c_args) + ", MPFR_RNDN);")

        lines.append(line)
        temps.append(my_name)
        return my_name
