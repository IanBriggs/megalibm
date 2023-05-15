
import math

import cmd_sollya
import lego_blocks.forms as forms
from better_float_cast import better_float_cast
from fpcore.ast import FPCore, Operation, Variable
from interval import Interval
from lambdas import types
from numeric_types import FP64


class MinimaxPolynomial(types.Source):

    def __init__(self, function: FPCore, domain: Interval, terms: int):
        """
        Create a minimax polynomial approximation of the function on the domain

        function: FPCore representing the function
        domain: Interval domain, must be finite
        terms: the number of terms in the generated expression not counting
                   the possible constant term
        """
        super().__init__(function, domain)

        # This is a Poly, not an Impl as assumed for other Source nodes
        self.out_type = types.Poly(self.out_type.function,
                                   self.out_type.domain)

        self.terms = terms

    def __str__(self):
        body = self.out_type.function.body
        inf = self.out_type.domain.inf
        sup = self.out_type.domain.sup
        terms = self.terms
        return f"(MinimaxPolynomial {body} [{inf} {sup}] {terms})"

    def __repr__(self):
        return ("MinimaxPolynomial",
                f"{repr(self.out_type.function)}, ",
                f"{repr(self.out_type.domain)}, ",
                f"{repr(self.terms)}, ",
                ")")

    def type_check(self):
        """ Makes sure the domain is finite """
        if self.type_check_done:
            return

        if not self.out_type.domain.isfinite():
            raise TypeError("MinimaxPolynomial must have a finite domain")

        self.type_check_done = True

    def generate(self, numeric_type=FP64):
        """
        Uses Sollya to fit a polynomial to the function choosing whether a
          constant term is needed and whether even, odd, or all degrees should
          be used
        Returns the lego_block form for a polynomial
        """
        self.type_check()

        monomials = list()

        # Do we need a constant term?
        try:
            if self.out_type.function.eval(0) != 0:
                monomials.append(0)
        except ZeroDivisionError:
            pass

        # Is the function even, odd, or neither?
        decomposed_identities = self.out_type.function.decompose_identities()
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
        res = cmd_sollya.Result(self.out_type.function,
                                self.out_type.domain,
                                monomials,
                                numeric_type)
        self.p_monomials = monomials
        self.p_coefficients = res.coefficients
        self.q_monomials = list()
        self.q_coefficients = list()

    @classmethod
    def generate_hole(cls, out_type):
        # We only output
        # (Poly (func) low high)
        # where low and high are finite
        if type(out_type) != types.Poly or not out_type.domain.isfinite():
            return list()

        # To get this output we just need be constructed with given args
        # TODO: How to pick the number of terms?
        return [ MinimaxPolynomial(out_type.function, out_type.domain, 14), ]
