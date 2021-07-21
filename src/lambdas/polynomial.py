

import numeric_types
import cmd_sollya
import lego_blocks.forms as forms

from lambdas import types




class Polynomial(types.Source):

    def __init__(self, function, domain, monomials, coefficients=None):
        self.monomials = monomials
        self.coefficients = coefficients or list()
        super().__init__(function, domain)


    def __repr__(self):
        return "Polynomial({}, {}, {}, {})".format(repr(self.function),
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
