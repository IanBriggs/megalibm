

from better_float_cast import better_float_cast
from fpcore.ast import ASTNode, Variable
from lego_blocks import forms


def simple_horner_poly(x, mons, coeffs):
    assert len(mons) == len(coeffs)
    if len(mons) == 0:
        return None

    c = coeffs[0]
    coeffs = coeffs[1:]

    if mons[0] == 0:
        part = ""
        next_mons = mons[1:]
    elif mons[0] == 1:
        part = f"{x}*"
        next_mons = [m - 1 for m in mons[1:]]
    elif mons[0] == 2:
        part = f"({x}*{x})*"
        next_mons = [m - 2 for m in mons[1:]]
    elif mons[0] == 3:
        part = f"(({x}*{x})*{x})*"
        next_mons = [m - 3 for m in mons[1:]]
    elif mons[0] == 4:
        part = f"(({x}*{x})*({x}*{x}))*"
        next_mons = [m - 4 for m in mons[1:]]
    elif mons[0] == 5:
        part = f"((({x}*{x})*({x}*{x}))*{x})*"
        next_mons = [m - 5 for m in mons[1:]]
    else:
        raise ValueError(f"Simple Horner is broken: {mons[0]}")

    next_part = simple_horner_poly(x, next_mons, coeffs)

    if issubclass(type(c), ASTNode):
        c = better_float_cast(c)

    if next_part is None:
        if better_float_cast(c) == 1 and part != "":
            return f"{part[:-1]}"
        return f"{part}{c}"
    return f"{part}({c} + {next_part})"


class Horner(forms.Form):

    def __init__(self, numeric_type, in_names, out_names, polynomial, split=0):
        super().__init__(numeric_type, in_names, out_names)
        assert (type(polynomial) in {
                forms.Polynomial, forms.RationalPolynomial})

        self.polynomial = polynomial
        self.split = split

    def __repr__(self):
        return "Horner({}, {}, {}, {})".format(repr(self.numeric_type),
                                               repr(self.in_names),
                                               repr(self.out_names),
                                               repr(self.polynomial))

    def to_c(self):
        c_type = self.numeric_type.c_type()
        out = self.out_names[0]
        x = self.in_names[0]


        if type(self.polynomial) == forms.Polynomial:
            mons = self.polynomial.monomials
            coeffs = self.polynomial.coefficients
            start = ""
            for i in range(self.split):
                start += simple_horner_poly(x, [mons[i]], [coeffs[i]])
                start += " + "
            mons = mons[self.split:]
            coeffs = coeffs[self.split:]
            body = start + simple_horner_poly(x, mons, coeffs)
        elif type(self.polynomial) == forms.RationalPolynomial:
            num_mons = self.polynomial.numerator_monomials
            num_coeffs = self.polynomial.numerator_coefficients
            p = simple_horner_poly(x, num_mons, num_coeffs)
            den_mons = self.polynomial.denominator_monomials
            den_coeffs = self.polynomial.denominator_coefficients
            q = simple_horner_poly(x, den_mons, den_coeffs)
            o = self.polynomial.offset.substitute(Variable("x"), x)
            body = f"{o} + ({p}) / ({q})"

        code = "{} {} = {};".format(c_type, out, body)

        return [code]
