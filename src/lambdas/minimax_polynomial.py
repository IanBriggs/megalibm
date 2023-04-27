
import math

import cmd_sollya
import lego_blocks.forms as forms
from better_float_cast import better_float_cast
from fpcore.ast import FPCore, Operation, Variable
from interval import Interval
from lambdas import types
from numeric_types import fp64


class MinimaxPolynomial(types.Source):

    def __init__(self, function: FPCore, domain: Interval, terms: int):
        """
        Create a minimax polynomial approximation of the function on the domain

        function: FPCore representing the function
        domain: Interval domain, must be finite
        terms: the number of terms in the generated expression not counting
                   the possible constant term
        """
        self.terms = terms
        super().__init__(function, domain)

    def __str__(self):
        body = self.function.body
        inf = self.domain.inf
        sup = self.domain.sup
        terms = self.terms
        return f"(MinimaxPolynomial {body} [{inf} {sup}] {terms})"

    def __repr__(self):
        return "MinimaxPolynomial({}, {}, {})".format(repr(self.function),
                                                      repr(self.domain),
                                                      repr(self.terms))

    def type_check(self):
        """ Makes sure the domain is finite """
        if self.type_check_done:
            return

        if (not math.isfinite(self.domain.inf)
                or not math.isfinite(self.domain.sup)):
            raise TypeError("MinimaxPolynomial must have a finite domain")

        self.out_type = types.Poly(self.function, self.domain)
        self.type_check_done = True

    def generate(self, numeric_type=fp64):
        """
        Uses Sollya to fit a polynomial to the function choosing whether a
          constant term is needed and whether even, odd, or all degrees should
          be used
        Returns the lego_block form for a polynomial
        """
        monomials = list()

        # Do we need a constant term?
        try:
            if self.out_type.function.eval(0) != 0:
                monomials.append(0)
        except ZeroDivisionError:
            pass

        # Is the function even, odd, or neither?
        decomposed_identities = self.function.decompose_identities()
        mirrors = decomposed_identities["mirror"]

        for s, t_arg in mirrors:
            if better_float_cast(t_arg) == 0:
                if s == Variable("x"):
                    monomials += range(2, 2*self.terms+1, 2)
                    break
                if s == Operation("-", Variable("x")):
                    monomials += range(1, 2*self.terms, 2)
                    break
        if len(monomials) == 0 or (len(monomials) == 1 and monomials[0] == 0):
            monomials += range(1, self.terms+1)

        # Run generation (this may fail since Sollya is picky)
        res = cmd_sollya.Result(self.function,
                                self.domain,
                                monomials,
                                numeric_type())

        # Return the lego_block.form
        return forms.Polynomial(self.function,
                                monomials,
                                res.coefficients,
                                self.domain)

    @classmethod
    def generate_hole(cls, out_type):
        # We only output
        # (Poly (func) low high)
        # where low and high are finite
        if (type(out_type) != types.Poly
            or not math.isfinite(better_float_cast(out_type.domain.inf))
                or not math.isfinite(better_float_cast(out_type.domain.sup))):
            return list()

        # To get this output we just need be constructed with given args
        # TODO: How to pick the number of terms?
        return [ MinimaxPolynomial(out_type.function, out_type.domain, 14), ]
