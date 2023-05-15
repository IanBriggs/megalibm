

import math

import sympy
from better_float_cast import better_float_cast
import fpcore
import mpmath
from sympy_solve_equality import sympy_to_fpcore

from utils.logging import Logger


logger = Logger(level=Logger.EXTRA)


def parse_bound(something):
    if "+inf" == something:
        return fpcore.ast.Constant("INFINITY")
    if "-inf" == something:
        return fpcore.ast.Operation("-", fpcore.ast.Constant("INFINITY"))
    fpc = fpcore.parse_expr(something)
    return fpc.simplify()

class Interval():

    def __init__(self, inf, sup):
        self.inf = parse_bound(inf)
        self.sup = parse_bound(sup)

        fi = self.float_inf
        if (math.isfinite(fi) and int(fi) == fi):
            self.inf = parse_bound(int(fi))

        fs = self.float_sup
        if (math.isfinite(fs) and int(fs) == fs):
            self.sup = parse_bound(int(fs))

        if not self.float_inf <= self.float_sup:
            raise ValueError(f"Upside down interval: [{inf}, {sup}]")

    @property
    def float_inf(self):
        return better_float_cast(self.inf.eval({}))

    @property
    def float_sup(self):
        return better_float_cast(self.sup.eval({}))

    def __str__(self):
        return f"[{self.inf}, {self.sup}]"

    def __repr__(self):
        return 'Interval("{}", "{}")'.format(self.inf, self.sup)

    def __abs__(self):
        #                 0
        # <---------------+--------------->
        #                    [********]
        if self.float_inf >= 0.0:
            return Interval(self.inf, self.sup)
        #                 0
        # <---------------+--------------->
        #               [********]
        if self.float_inf <= 0.0 and 0.0 <= self.float_sup:
            abs_max = max(-self.inf, self.sup)
            return Interval(0.0, abs_max)
        #                 0
        # <---------------+--------------->
        #      [********]
        if self.float_sup <= 0.0:
            return Interval(-self.sup, -self.inf)

        raise ValueError(f"Internal error: unable to abs {self}")

    def __getitem__(self, key):
        if key == 0:
            return self.inf
        if key == 1:
            return self.sup
        raise IndexError(f"Interval cannot be indexed with '{key}'")

    def isfinite(self):
        return (math.isfinite(self.float_inf)
                and math.isfinite(self.float_sup))

    def width(self):
        return self.sup - self.inf

    def contains(self, other):
        logger.log("Testing if {} is in [{}, {}]", other, self.inf, self.sup)
        if type(other) == mpmath.iv.mpf:
            inf = str(self.inf).replace("INFINITY", "inf")
            sup = str(self.sup).replace("INFINITY", "inf")
            me = mpmath.iv.mpf([inf, sup])
            return other in me
        if type(other) == Interval:
            me = mpmath.iv.mpf([str(self.inf).replace("INFINITY", "inf"),
                                str(self.sup).replace("INFINITY", "inf")])
            other = mpmath.iv.mpf([str(other.inf).replace("INFINITY", "inf"),
                                   str(other.sup).replace("INFINITY", "inf")])
            return other in me
        f_point = better_float_cast(other)
        return self.float_inf <= f_point and f_point <= self.float(sup)

    def join(self, other):
        if self.sup < other.inf:
            msg = f"Intervals do not overlap:\nself = {self}\nother = {other}"
            raise ValueError(msg)
        inf = self.inf
        if self.float_inf > other.float_inf:
            inf = other.inf
        sup = self.sup
        if self.float_sup < other.float_sup:
            sup = other.sup
        return Interval(inf, sup)

    @staticmethod
    def try_symbolic_interval_eval(fpc, in_domain):
        # What is the input's name?
        vars = fpc.get_variables()
        if len(vars) != 1:
            raise ValueError("Only single variable functions are supported")
        in_var = fpcore.ast.Variable(vars.pop())

        # Determine if the func in monotonic on this interval
        diff_fpc = sympy_to_fpcore(sympy.diff(fpc.to_sympy(),
                                                      in_var.to_sympy()))
        diff_on_interval = diff_fpc.interval_eval({in_var.source:
                                                          in_domain})
        if diff_on_interval >= 0:
            # Yay, we can just use the endpoints
            inf = fpc.substitute(in_var, in_domain.inf)
            sup = fpc.substitute(in_var, in_domain.sup)
            return Interval(inf, sup)

        # Hopefully just interval arith makes a tight answer
        # (doubtful)
        mpf_domain = fpc.interval_eval({in_var.source: in_domain})
        inf, sup = mpf_domain._mpi_  # Don't do this
        return Interval(mpmath.nstr(mpmath.mpf(inf), 4096),
                              mpmath.nstr(mpmath.mpf(sup), 4096))

