
import fpcore
from fpcore.ast import FPCore
from interval import Interval
from lambdas.fixed_multi_polynomial import FixedMultiPolynomial


class FixedPolynomial(FixedMultiPolynomial):

    def __init__(self,
                 function: FPCore,
                 domain: Interval,
                 monomials: list,
                 coefficients: list):
        # Run FixedMultiPolynomial initialization
        super().__init__(function=function,
                         domain=domain,
                         combiner=fpcore.parse("(FPCore (x p q) p)"),
                         p_monomials=monomials,
                         p_coefficients=coefficients,
                         q_monomials=list(),
                         q_coefficients=list())

    def __str__(self):
        return ("(FixedPolynomial"
                f" {self.out_type.function}"
                f" {self.out_type.domain}"
                f" [{fpcore.list_to_str(self.p_monomials)}]"
                f" [{fpcore.list_to_str(self.p_coefficients)}]"
                ")")

    def __repr__(self):
        return ("FixedPolynomial("
                f"{repr(self.out_type.function)}, "
                f"{repr(self.out_type.domain)}, "
                f"[{fpcore.list_to_repr(self.p_monomials)}], "
                f"[{fpcore.list_to_repr(self.p_coefficients)}], "
                ")")
