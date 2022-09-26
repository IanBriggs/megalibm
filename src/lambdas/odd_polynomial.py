
import lambdas

import math
import numeric_types
import cmd_sollya
import snake_egg_rules
import lego_blocks.forms as forms

from lambdas import types
from lambdas.flip_about_zero_x import is_odd_function


class OddPolynomial(types.Source):

    def __init__(self, function, domain, monomials, coefficients=None):
        self.monomials = monomials
        self.coefficients = coefficients or list()
        super().__init__(function, domain)

    def __repr__(self):
        return "OddPolynomial({}, {}, {}, {})".format(repr(self.function),
                                                      repr(self.domain),
                                                      repr(self.monomials),
                                                      repr(self.coefficients))

    def type_check(self):
        assert (type(self.monomials) == list)
        assert (type(self.coefficients) == list)
        assert (len(self.monomials) == len(set(self.monomials)))
        assert (len(self.coefficients) <= len(self.monomials))
        assert (all([type(m) == int for m in self.monomials]))
        assert (all([type(c) == float or c is None for c in self.coefficients]))
        #assert (is_odd_function(self.function))
        #assert(all(m%2 == 1 for m in self.monomials))

        self.out_type = types.Poly(self.function, self.domain)

    def generate(self):
        res = cmd_sollya.Result(self.function,
                                self.domain,
                                self.monomials,
                                numeric_types.fp64())
        return forms.Polynomial(self.function,
                                self.monomials,
                                res.coefficients,
                                self.domain)

    @classmethod
    def generate_hole(cls, out_type, egraph):
        # We only output
        # (Poly (func) low high)
        # where low and high are finite
        if (type(out_type) != types.Poly
            or not math.isfinite(float(out_type.domain.inf))
            or not math.isfinite(float(out_type.domain.sup))
                or not is_odd_function(out_type.function, egraph)):
            return list()

        # To get this output we just need be contructed with given args
        # TODO: how should monomials be done?
        monomials = list(range(1, 31, 2))
        try:
            if out_type.function.eval(0) != 0:
                monomials = [0] + monomials
        except ZeroDivisionError:
            pass
        return [(out_type.function, out_type.domain, monomials), ]
