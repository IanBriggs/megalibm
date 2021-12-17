
import lambdas

import math
import numeric_types
import cmd_sollya
import snake_egg_rules
import lego_blocks.forms as forms


from lambdas import types




class EvenPolynomial(types.Source):

    def __init__(self, function, domain, monomials, coefficients=None):
        self.monomials = monomials
        self.coefficients = coefficients or list()
        super().__init__(function, domain)


    def __repr__(self):
        return "EvenPolynomial({}, {}, {}, {})".format(repr(self.function),
                                                      repr(self.domain),
                                                      repr(self.monomials),
                                                      repr(self.coefficients))


    def type_check(self):
        assert(type(self.monomials) == list)
        assert(type(self.coefficients) == list)
        assert(len(self.monomials) == len(set(self.monomials)))
        assert(len(self.coefficients) <= len(self.monomials))
        assert(all([type(m) == int for m in self.monomials]))
        assert(all([type(c) == float or c is None for c in self.coefficients]))
        assert(snake_egg_rules.is_even(self.function))
        assert(all(m%2 == 0 for m in self.monomials))

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
    def generate_hole(cls, out_type):
        # We only output
        # (Poly (func) low high)
        # where low and high are finite
        if (type(out_type) != types.Poly
            or not math.isfinite(float(out_type.domain.inf))
            or not math.isfinite(float(out_type.domain.sup))
            or not snake_egg_rules.is_even(out_type.function)):
            return list()

        # To get this output we just need be contructed with given args
        # TODO: how should monomials be done?
        return [(out_type.function, out_type.domain, list(range(2,30,2))),]

