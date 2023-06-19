

import fpcore
from lego_blocks import forms
from lego_blocks.forms.horner import tree_pow


class General(forms.Form):

    def __init__(self,
                 numeric_type,
                 in_names,
                 out_names,
                 monomials,
                 coefficients):
        # Run Form initialization
        super().__init__(numeric_type, in_names, out_names)

        # Check in and out names
        if len(in_names) != 1:
            msg = f"'in_names' must have a length of 1, found: {len(in_names)}"
            raise ValueError(msg)
        if len(out_names) != 1:
            msg = ("'out_names' must have a length of 1, found:"
                   f" {len(out_names)}")
            raise ValueError(msg)

        # No need to run checks here, the lambdas should have done that
        self.monomials = monomials
        self.coefficients = [fpcore.parse_expr(str(c)) for c in coefficients]

    def __repr__(self):
        return ("General("
                f"{self.numeric_type.name}, "
                f"[{fpcore.ast.list_to_repr(self.in_names)}], "
                f"[{fpcore.ast.list_to_repr(self.out_names)}], "
                f"[{fpcore.ast.list_to_repr(self.monomials)}], "
                f"[{fpcore.ast.list_to_repr(self.coefficients)}], "
                f"{self.split}"
                ")")

    def to_c(self):
        # Local names for things
        x = fpcore.ast.Variable(self.in_names[0])
        mons = self.monomials.copy()
        coeffs = self.coefficients.copy()

        terms = [c * tree_pow(x, m) for c,m in zip(coeffs, mons)]
        poly = sum(terms)

        # Use the fpcore C generation
        poly = poly.constant_propagate()
        c_type = self.numeric_type.c_type
        body = poly.to_libm_c(numeric_type=self.numeric_type)
        code = f"{c_type} {self.out_names[0]} = {body};"
        return [code]
