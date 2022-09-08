

from fpcore.ast import ASTNode, Constant, Number, Variable, Operation, FPCore
from utils import add_method, Logger


logger = Logger(level=Logger.EXTRA)


@add_method(ASTNode)
def to_mpfr_c(self, lines, temps):
    # Make sure calling to_mpfr_c leads to an error if not overridden
    class_name = type(self).__name__
    msg = "to_mpfr_c not implemented for class {}".format(class_name)
    raise NotImplementedError(msg)

@add_method(Constant)
def to_mpfr_c(self, lines, temps):
    mapping = {
        "PI" : "mpfr_const_pi"
    }
    my_name = "generated_{}".format(len(temps))
    func = mapping[self.source]
    lines.append("  {}({}, MPFR_RNDN);".format(func, my_name))
    temps.append(my_name);
    return my_name

@add_method(Number)
def to_mpfr_c(self, lines, temps):
    my_name = "generated_{}".format(len(temps))
    line = "  mpfr_set_str({}, \"{}\", 10, MPFR_RNDN);"
    lines.append(line.format(my_name, self.source))
    temps.append(my_name);
    return my_name

@add_method(Variable)
def to_mpfr_c(self, lines, temps):
    return self.source

@add_method(Operation)
def to_mpfr_c(self, lines, temps):
    mpfr_functions = {
        "pow" : "mpfr_pow",
        "sqrt" : "mpfr_sqrt",
        "exp" : "mpfr_exp",
        "log" : "mpfr_log",
        "sin" : "mpfr_sin",
        "asin" : "mpfr_asin",
        "cos" : "mpfr_cos",
        "acos" : "mpfr_acos",
        "tan" : "mpfr_tan",
        "atan" : "mpfr_atan",
        "+" : "mpfr_add",
        "-" : "mpfr_sub",
        "*" : "mpfr_mul",
        "/" : "mpfr_div",
        "fabs": "mpfr_abs",
        "fmod": "mpfr_fmod",
    }
    c_args = [arg.to_mpfr_c(lines, temps) for arg in self.args]
    my_name = "generated_{}".format(len(temps))
    fname = mpfr_functions[self.op]
    if self.op == "-" and len(c_args) == 1:
        fname = "mpfr_neg"
    line = ("  " + fname + "(" + my_name + ", "
            + ", ".join(c_args) + ", MPFR_RNDN);")
    lines.append(line)
    temps.append(my_name)
    return my_name


@add_method(FPCore)
def to_mpfr_c(self, outname):
    lines = list()
    temps = list()
    top_name = self.body.to_mpfr_c(lines, temps)
    temps = temps[:-1]
    lines[-1] = lines[-1].replace(top_name, outname)
    return lines, temps
