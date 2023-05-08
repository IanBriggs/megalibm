
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

        # Polynomials require a finite domain
        if not domain.isfinite():
            raise ValueError("'domain' must be finite, given: {domain}")

        # TODO: check that the function is defined on the entire domain

        # Check and save combiner
        if type(combiner) != FPCore:
            msg = f"'combiner' must be an FPCore, given: {type(combiner)}"
            raise ValueError(msg)
        if len(combiner.arguments) != 3:
            msg = ("'combiner' FPCore must take in 3 arguments, given: "
                   f"{len(combiner.arguments)} arguments")
            raise ValueError(msg)
        # TODO: Maybe we should also check that the variables are used in
        #       the body?
        self.combiner = combiner

        # Check p_monomials
        if type(p_monomials) != list:
            msg = f"'p_monomials' must be a list, given: {type(p_monomials)}"
            raise ValueError(msg)
        if not all(type(m) == int for m in p_monomials):
            bad = [m for m in p_monomials if type(m) != int][0]
            msg = f"'p_monomials' must be all integers, given: {type(bad)}"

        # Check p_coefficients
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
        if type(q_monomials) != list:
            msg = f"'q_monomials' must be a list, given: {type(q_monomials)}"
            raise ValueError(msg)
        if not all(type(m) == int for m in q_monomials):
            bad = [m for m in q_monomials if type(m) != int][0]
            msg = f"'q_monomials' must be all integers, found: {type(bad)}"

        # Check q_coefficients
        if type(q_coefficients) != list:
            msg = ("'q_coefficients' must be a list, given:"
                   f" {type(q_coefficients)}")
            raise ValueError(msg)
        # TODO: Establish a way to determine that the coefficients are the
        #       right type. Currently they can be str (if the str represents
        #       a number), float, and mpmath.mpf
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
                f" {self.function}"
                f" {self.domain}"
                f" {self.combiner}"
                f" [{fpcore.list_to_str(self.p_monomials)}]"
                f" [{fpcore.list_to_str(self.p_coefficients)}]"
                f" [{fpcore.list_to_str(self.q_monomials)}]"
                f" [{fpcore.list_to_str(self.q_coefficients)}]"
                ")")

    def __repr__(self):
        return ("FixedMultiPolynomial("
                f"{repr(self.function)}, "
                f"{repr(self.domain)}, "
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

        # Set out_type and indicate that type_check has completed
        self.out_type = types.Poly(self.function, self.domain)
        self.type_check_done = True

    def generate(self, numeric_type=FP64):
        self.type_check()
        return None
