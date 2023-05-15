

from math import floor

import fpcore
from fpcore.ast import (ASTNode, Atom, Constant, FPCore, Number, Operation,
                        Variable)
from lego_blocks import forms
from lego_blocks.forms.horner import tree_pow


def expr_estrin(x: fpcore.ast.Expr,
                mons: list,
                coeffs: list):
    """
    Constructs an FPCore.ast expression representing the given polynomial using
    Estrin's scheme

    x- base
    mons- integer monomials for base 'x', must be full rank
    coeffs- fpcore coefficients for polynomial terms

    >>> x = fpcore.ast.Variable("g")
    >>> cast = lambda l: [fpcore.ast.Number(str(n)) for n in l]
    >>> str(expr_estrin(x, [0], cast([1.0])))
    '1.0'
    >>> str(expr_estrin(x, [0, 1], cast([1.0, 2.0])))
    '(+ 1.0 (* 2.0 g))'
    >>> str(expr_estrin(x, [0, 1, 2], cast([1.0, 2.0, 3.0])))
    '(+ (+ 1.0 (* 2.0 g)) (* 3.0 (* g g)))'
    >>> str(expr_estrin(x, [0, 1, 2, 3], cast([1.0, 2.0, 3.0, 4.0])))
    '(+ (+ 1.0 (* 2.0 g)) (* (+ 3.0 (* 4.0 g)) (* g g)))'
    >>> str(expr_estrin(x, [0, 1, 2, 3, 4], cast([1.0, 2.0, 3.0, 4.0, 5.0])))
    '(+ (+ (+ 1.0 (* 2.0 g)) (* (+ 3.0 (* 4.0 g)) (* g g))) (* 5.0 (* (* g g) (* g g))))'
    >>> str(expr_estrin(x,
    ...                 [0, 1, 2, 3, 4, 5],
    ...                 cast([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])))
    '(+ (+ (+ 1.0 (* 2.0 g)) (* (+ 3.0 (* 4.0 g)) (* g g))) (* (+ 5.0 (* 6.0 g)) (* (* g g) (* g g))))'
    """
    # TODO: figure out how to fit doctest within 80 columns
    # Check x
    if not issubclass(type(x), fpcore.ast.Expr):
        raise ValueError(f"'x' must be an FPCore.ast.Expr, given: {type(x)}")

    # Check mons
    if type(mons) != list:
        raise ValueError(f"'mons' must be a list, given: {type(mons)}")
    if not all(type(m) == int for m in mons):
        bad = [m for m in mons if type(m) != int][0]
        raise ValueError(f"'mons' must be all int, given: {type(bad)}")
    if mons != list(range(len(mons))):
        raise ValueError(f"'mons' must be full rank, given: {mons}")

    # Check coeffs
    if type(coeffs) != list:
        raise ValueError(f"'coeffs' must be a list, given: {type(n)}")
    if not all(issubclass(type(c), fpcore.ast.Expr) for c in coeffs):
        bad = [c for c in coeffs if not issubclass(
            type(c), fpcore.ast.Expr)][0]
        msg = (f"'coeffs' must be all fpcore.ast.Expr, given: {type(bad)}")
        raise ValueError(msg)

    # Check that they match
    if len(mons) != len(coeffs):
        msg = ("'mons' and 'coeffs' must have the same"
               f" length, received: {len(mons)} and {len(coeffs)}")
        raise ValueError(msg)

    # Base cases
    if len(mons) == 1:
        return coeffs[0]
    if len(mons) == 2:
        return coeffs[0] + coeffs[1] * x

    # Pair off
    n = floor(len(mons) / 2)
    next_mons = list()
    next_coeffs = list()
    for i in range(n):
        d = coeffs[2 * i] + coeffs[2 * i + 1] * x
        next_mons.append(i)
        next_coeffs.append(d)

    # Handle straggler
    if len(mons) % 2 == 1:
        next_mons.append(n)
        next_coeffs.append(coeffs[-1])

    return expr_estrin(x*x, next_mons, next_coeffs)

class Estrin(forms.Form):

    def __init__(self,
                 numeric_type,
                 in_names: list,
                 out_names: list,
                 monomials: list,
                 coefficients: list,
                 split: int=0):
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
        self.split = split

    def __repr__(self):
        return ("Estrin("
                f"{self.numeric_type.name}, "
                f"[{fpcore.ast.list_to_repr(self.in_names)}], "
                f"[{fpcore.ast.list_to_repr(self.out_names)}], "
                f"[{fpcore.ast.list_to_repr(self.monomials)}], "
                f"[{fpcore.ast.list_to_repr(self.coefficients)}], "
                f"{self.split}"
                ")")

    def to_c(self):
        # Build the estrin polynomial as an fpcore ast expression

        # Local names for things
        x = fpcore.ast.Variable(self.in_names[0])
        mons = self.monomials.copy()
        coeffs = self.coefficients.copy()

        # We want 'split' terms in general form up front (done last)
        general_terms = self.split
        general_mons = mons[0:general_terms]
        general_coeffs = coeffs[0:general_terms]
        mons = mons[general_terms:]
        coeffs = coeffs[general_terms:]

        # Estrin only works on full-rank polynomials starting at 0
        # This is all based on on the monomials
        # 1 full rank starting at 0
        # 2 even rank starting at 0
        # 3 even rank starting at 2n
        # 4 odd rank starting at 1
        # 5 odd rank starting at 2n+1
        # 6-8 each of the last three with a constant term on the front

        # Reduce 6-8 to 3-5 by pulling off the constant term and adding
        # it back after
        const_term = None
        if mons[0] == 0 and (all(m%2 == 0 for m in mons[1:])
                             or all(m%2 == 1 for m in mons[1:])):
            const_term = coeffs[0]
            mons = mons[1:]
            coeffs = coeffs[1:]

        # Reduce 3-5 to 2 by dividing out the first power of x and multiplying
        # it back after
        mult_term = None
        if mons[0] != 0:
            mult_term = tree_pow(x, mons[0])
            mons = [m - mons[0] for m in mons]

        # Reduce 2 to 1 by phrasing the polynomial as p(x*x)
        estrin_x = x
        if all(m%2 == 0 for m in mons[1:]):
            estrin_x = x * x
            mons = [m // 2 for m in mons]

        # Use the estrin helper then apply any of the after things
        poly = expr_estrin(estrin_x, mons, coeffs)
        if mult_term is not None:
            poly = mult_term * poly
        if const_term is not None:
            poly = const_term + poly

        # Now build up the general form
        while len(general_mons) > 0:
            x_pow = tree_pow(x, general_mons.pop())
            new_term = x_pow * general_coeffs.pop()
            poly = new_term + poly

        # Use the fpcore C generation
        poly = poly.constant_propagate()
        c_type = self.numeric_type.c_type
        body = poly.to_libm_c(numeric_type=self.numeric_type)
        code = f"{c_type} {self.out_names[0]} = {body};"
        return [code]
