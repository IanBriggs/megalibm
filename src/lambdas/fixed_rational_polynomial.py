import math
from fpcore.ast import FPCore, ASTNode
from interval import Interval
from lambdas import types
from lego_blocks import forms
from numeric_types import fp64 


class FixedRationalPolynomial(types.Source):

    def __init__(self, function: FPCore, domain: Interval,
                 offset: ASTNode,
                 numerator_monomials: list, numerator_coefficients: list,
                 denominator_monomials: list, denominator_coefficients: list):
        """
        User defined polynomial approximation for the function on the domain

        function: FPCore representing the function
        domain: Interval domain, must be finite
        offset: polynomial is $o + p/q$, this is the o
        numerator_monomials: list of monomials in ascending order
        numerator_coefficients: list of coefficients for the monomials
        denominator_monomials: list of monomials in ascending order
        denominator_coefficients: list of coefficients for the monomials
        """
        super().__init__(function, domain)
        self.offset = offset
        assert len(numerator_monomials) == len(numerator_coefficients)
        self.numerator_monomials = numerator_monomials
        self.numerator_coefficients = numerator_coefficients
        assert len(denominator_monomials) == len(denominator_coefficients)
        self.denominator_monomials = denominator_monomials
        self.denominator_coefficients = denominator_coefficients

    def __str__(self):
        body = self.function.body
        inf = self.domain.inf
        sup = self.domain.sup
        return f"(FixedRationalPolynomial {body} [{inf} {sup}])"

    def __repr__(self):
        msg = "FixedPolynomial({}, {}, {}, {}, {}, {}, {})"
        return msg.format(repr(self.function),
                          repr(self.domain),
                          repr(self.offset),
                          repr(self.numerator_monomials),
                          repr(self.numerator_coefficients),
                          repr(self.denominator_monomials),
                          repr(self.denominator_coefficients))

    def type_check(self):
        try:
            if self.function.eval(0) != 0:
                assert (self.monomials[0] == 0)
        except ZeroDivisionError:
            pass

        if (not math.isfinite(self.domain.inf)
                or not math.isfinite(self.domain.sup)):
            raise TypeError("FixedPolynomial must have a finite domain")

        self.out_type = types.Poly(self.function, self.domain)

    def generate(self, numeric_type=fp64):
        return forms.RationalPolynomial(self.function,
                                        self.offset,
                                        self.numerator_monomials,
                                        self.numerator_coefficients,
                                        self.denominator_monomials,
                                        self.denominator_coefficients,
                                        self.domain)
