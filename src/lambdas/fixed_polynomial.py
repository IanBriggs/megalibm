import math
from fpcore.ast import FPCore
from interval import Interval
from lambdas import types
from lego_blocks import forms


class FixedPolynomial(types.Source):

    def __init__(self, function: FPCore, domain: Interval, terms: int,
                 monomials: list, coefficients: list, symmetry = None):
        """
        User defined polynomial approximation for the function on the domain

        function: FPCore representing the function
        domain: Interval domain, must be finite
        terms: the number of terms in the expression including the constant term
        monomials: list of monomials in ascending order
        coefficients: list of coefficients for the monomials
        """
        super().__init__(function, domain)
        self.terms = terms
        self.monomials = monomials
        self.coefficients = coefficients
        self.symmetry = symmetry

    def __str__(self):
        body = self.function.body
        inf = self.domain.inf
        sup = self.domain.sup
        terms = self.terms
        return f"(FixedPolynomial {body} [{inf} {sup}] {terms})" 

    def __repr__(self):
        return "FixedPolynomial({}, {}, {})".format(repr(self.function),
                                                      repr(self.domain),
                                                      repr(self.terms))

    def type_check(self):
        # try:
        #     if self.function.eval(0) != 0:
        #         assert(self.monomials[0] == 0)
        # except ZeroDivisionError:
        #     pass

        if (not math.isfinite(self.domain.inf)
                or not math.isfinite(self.domain.sup)):
            raise TypeError("FixedPolynomial must have a finite domain")

        if self.symmetry == 0:
            assert(all(term % 2 == 0 for term in self.monomials))
        elif self.symmetry == 1:
            assert(all(term % 2 != 0 for term in self.monomials))

        self.out_type = types.Poly(self.function, self.domain)

    def generate(self):
        return forms.Polynomial(self.function,
                                self.monomials,
                                self.coefficients,
                                self.domain)                      
    