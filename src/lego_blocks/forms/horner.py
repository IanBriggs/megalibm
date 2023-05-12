

import fpcore
from lego_blocks import forms


def tree_pow(x: fpcore.ast.Expr,
             n: int):
    """
    Constructs an FPCore.ast expression representing pow(x, n) as repeated
    multiplication parenthesized similar to "Ancient Egyptian multiplication"

    x- base
    n- exponent, non-negative integer

    >>> x = fpcore.ast.Variable("g")
    >>> str(tree_pow(x, 1))
    'g'
    >>> str(tree_pow(x, 2))
    '(* g g)'
    >>> str(tree_pow(x, 3))
    '(* (* g g) g)'
    >>> str(tree_pow(x, 4))
    '(* (* g g) (* g g))'
    >>> str(tree_pow(x, 5))
    '(* (* (* g g) (* g g)) g)'
    """
    # Check x
    if not issubclass(type(x), fpcore.ast.Expr):
        raise ValueError(f"'x' must be an FPCore.ast.Expr, given: {type(x)}")

    # Check n
    if type(n) != int:
        raise ValueError(f"'n' must be an int, given: {type(n)}")
    if n < 0:
        raise ValueError(f"'n' must be non-negative, given: {n}")

    def _tree_pow(x, n):
        if n == 0:
            return fpcore.ast.Number("1")
        if n == 1:
            return x
        if n % 2 == 1:
            return tree_pow(x, n-1) * x
        else:
            part = tree_pow(x, n // 2)
            return part * part

    return _tree_pow(x, n)


class Horner(forms.Form):

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
        return ("Horner("
                f"{self.numeric_type.name}, "
                f"[{fpcore.ast.list_to_repr(self.in_names)}], "
                f"[{fpcore.ast.list_to_repr(self.out_names)}], "
                f"[{fpcore.ast.list_to_repr(self.monomials)}], "
                f"[{fpcore.ast.list_to_repr(self.coefficients)}], "
                f"{self.split}"
                ")")

    def to_c(self):
        """
        Create a list of strings representing C source code for this block

        >>> import numeric_types
        >>> doit = lambda m, c, s: \
        Horner(numeric_types.FP64, ["x"], ["poly"], m, c, s).to_c()
        >>> doit([0], ["1.23"], 0)
        ['double poly = 1.23;']
        >>> doit([1], [1], 0)
        ['double poly = x;']
        >>> doit([2], [-1], 0)
        ['double poly = (-(x*x));']
        >>> doit([0, 1], ["1.23", "4.56"], 0)
        ['double poly = (1.23+(x*4.56));']
        >>> doit([0], ["1.23"], 0)
        ['double poly = 1.23;']
        """
        # Build the horner polynomial as an fpcore ast expression

        # Local names for things
        x = fpcore.ast.Variable(self.in_names[0])
        mons = self.monomials.copy()
        coeffs = self.coefficients.copy()

        # Handle length 1
        if len(mons) == 1:
            poly = coeffs.pop() * tree_pow(x, mons.pop())

            # Use the fpcore C generation
            poly = poly.constant_propagate()
            cdecl = self.numeric_type.c_type
            body = poly.to_libm_c(numeric_type=self.numeric_type)
            code = f"{cdecl} {self.out_names[0]} = {body};"
            return [code]

        # We want 'split' terms in general form
        general_mons = mons[0:self.split]
        general_coeffs = coeffs[0:self.split]
        mons = mons[self.split:]
        coeffs = coeffs[self.split:]

        # Build the polynomial expression from the inside out
        poly = coeffs.pop()
        old_mon = mons.pop()
        while len(mons) > 0:
            # Figure out the power of x needed for this term
            mon = mons.pop()
            mon_diff = old_mon - mon
            x_pow = tree_pow(x, mon_diff)

            # Multiply it then add the next coefficient
            poly = x_pow * poly
            poly = coeffs.pop() + poly

            # Update old monomial
            old_mon = mon

        # The last pow isn't based on a difference of monomials
        if mon != 0:
            x_pow = tree_pow(x, mon)
            poly = x_pow * poly

        # Now build up the general form
        while len(general_mons) > 0:
            # Build x**mon
            mon = general_mons.pop()
            x_pow = tree_pow(x, mon)

            # Add new term
            new_term = general_coeffs.pop() * x_pow
            poly = new_term + poly

        # Use the fpcore C generation
        poly = poly.constant_propagate()
        cdecl = self.numeric_type.c_type
        body = poly.to_libm_c(numeric_type=self.numeric_type)
        code = f"{cdecl} {self.out_names[0]} = {body};"
        return [code]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
