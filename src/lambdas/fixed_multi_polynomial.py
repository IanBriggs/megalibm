
from expect import expect_type
import fpcore
from fpcore.ast import FPCore
from interval import Interval
from lambdas import types
from numeric_types import FP64


class FixedMultiPolynomial(types.Source):

    def __init__(self,
                 function: FPCore,
                 domain: Interval,
                 combiner: FPCore,
                 p_monomials: list,
                 p_coefficients: list,
                 q_monomials: list,
                 q_coefficients: list):
        # Run Source initialization
        super().__init__(function, domain)

        # This is a Poly, not an Impl as assumed for other Source nodes
        self.out_type = types.Poly(self.out_type.function,
                                   self.out_type.domain)

        # Polynomials require a finite domain
        if not domain.isfinite():
            raise ValueError("'domain' must be finite, given: {domain}")

        # TODO: check that the function is defined on the entire domain

        # Check and save combiner
        expect_type("combiner", combiner, FPCore)
        if len(combiner.arguments) != 3:
            msg = ("'combiner' FPCore must take in 3 arguments, given: "
                   f"{len(combiner.arguments)} arguments")
            raise ValueError(msg)
        self.combiner = combiner

        # Check p_monomials
        expect_type("p_monomials", p_monomials, list)
        if not all(type(m) == int for m in p_monomials):
            bad = [m for m in p_monomials if type(m) != int][0]
            msg = f"'p_monomials' must be all integers, given: {type(bad)}"

        # Check p_coefficients
        expect_type("p_coefficients", p_coefficients, list)
        if type(p_coefficients) != list:
            msg = ("'p_coefficients' must be a list, given:"
                   f" {type(p_coefficients)}")
            raise ValueError(msg)
        # TODO: Establish a way to determine that the coefficients are the
        #       right type. Currently they can be str (if the str represents
        #       a number), float, and mpmath.mpf
        if len(p_monomials) != len(p_coefficients):
            msg = ("'p_monomials' and 'p_coefficients' must have the same"
                   f" length, received: {len(p_monomials)}"
                   f" and {len(p_coefficients)}")
            raise ValueError(msg)

        # Normalize and save p_monomials and p_coefficients
        paired = list(zip(p_monomials, p_coefficients))
        paired.sort()
        self.p_monomials = [p[0] for p in paired]
        self.p_coefficients = [p[1] for p in paired]

        # Check q_monomials
        expect_type("q_monomials", q_monomials, list)
        if not all(type(m) == int for m in q_monomials):
            bad = [m for m in q_monomials if type(m) != int][0]
            msg = f"'q_monomials' must be all integers, found: {type(bad)}"

        # Check q_coefficients
        expect_type("q_coefficients", q_coefficients, list)
        if len(q_monomials) != len(q_coefficients):
            msg = ("'q_monomials' and 'q_coefficients' must have the same"
                   f" length, received: {len(q_monomials)}"
                   f" and {len(q_coefficients)}")
            raise ValueError(msg)

        # Normalize and save q_monomials and q_coefficients
        paired = list(zip(q_monomials, q_coefficients))
        paired.sort()
        self.q_monomials = [p[0] for p in paired]
        self.q_coefficients = [p[1] for p in paired]

    def __str__(self):
        return ("(FixedMultiPolynomial"
                f" {self.out_type.function}"
                f" {self.out_type.domain}"
                f" {self.combiner}"
                f" [{fpcore.list_to_str(self.p_monomials)}]"
                f" [{fpcore.list_to_str(self.p_coefficients)}]"
                f" [{fpcore.list_to_str(self.q_monomials)}]"
                f" [{fpcore.list_to_str(self.q_coefficients)}]"
                ")")

    def __repr__(self):
        return ("FixedMultiPolynomial("
                f"{repr(self.out_type.function)}, "
                f"{repr(self.out_type.domain)}, "
                f"{repr(self.combiner)}, "
                f"[{fpcore.list_to_repr(self.p_monomials)}], "
                f"[{fpcore.list_to_repr(self.p_coefficients)}], "
                f"[{fpcore.list_to_repr(self.q_monomials)}], "
                f"[{fpcore.list_to_repr(self.q_coefficients)}]"
                ")")

    def type_check(self):
        # Only check once
        if self.type_check_done:
            return

        # TODO: Is there anything to check here?

        self.type_check_done = True

    def generate(self, numeric_type=FP64):
        self.type_check()
        return None
