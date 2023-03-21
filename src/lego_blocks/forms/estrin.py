

from lego_blocks import forms
from fpcore.ast import ASTNode, Atom, Constant, FPCore, Operation, Number, Variable


class Estrin(forms.Form):

    def __init__(self, numeric_type, in_names, out_names, polynomial, split=0):
        super().__init__(numeric_type, in_names, out_names)
        assert (type(polynomial) == forms.Polynomial)

        self.polynomial = polynomial
        self.split = split

    def __repr__(self):
        return "Estrin({}, {}, {}, {}, {}, {})".format(repr(self.numeric_type),
                                                       repr(self.in_names),
                                                       repr(self.out_names),
                                                       repr(self.polynomial))

    def expand_pow(self, n):
        if n == 0:
            return "1"
        x = f"({self.in_names[0]})"
        if n == 1:
            return x
        x_2 = f"({self.in_names[0]}*{self.in_names[0]})"
        if n == 2:
            return x_2
        if n % 2:
            return f"(({self.expand_pow(n-1)})*{x})"
        else:
            if n // 2 % 2:
                return f"(({self.expand_pow(n-2)})*{x_2})"
            else:
                return f"(({self.expand_pow(n//2)})*({self.expand_pow(n//2)}))"

    def estrin(self, mons, groups, x_power, isFirstCall=False):

        if isFirstCall and len(mons) <= 2:
            if len(mons) == 1:
                return f"{groups[0]}*{self.expand_pow(mons[0])}"
            else:
                return f"{groups[0]}*{self.expand_pow(mons[0])} + {groups[1]}*{self.expand_pow(mons[1])}"

        if len(mons) <= 2:
            if len(mons) == 1:
                return f"{groups[0]}*{self.expand_pow(x_power)}"
            else:
                return f"{groups[0]} \n               + {groups[1]}*{self.expand_pow(x_power)}"

        even = groups[0::2]
        odd = groups[1::2]
        new_groups = []

        for a, b in zip(even, odd):
            group = f"({a} \n               + {b}*{self.expand_pow(x_power)})"
            new_groups.append(group)

        if len(even) > len(odd):
            new_groups.append(even[-1])

        new_len = len(new_groups)
        new_mons = mons[:new_len]

        return self.estrin(new_mons, new_groups, x_power * 2)

    def eval_estrin(self, mons, cast_coeff, cast_in, power, split):
        if split >= 1:
            m = mons[split]
            new_mons = mons[split:]
            new_coeffs = cast_coeff[split:]
            rest = self.eval_estrin(new_mons, new_coeffs, cast_in, power, 0)
            split = self.estrin(
                mons[:split], cast_coeff[:split], power, isFirstCall=True)
            rhs = f"{split} + {rest}"
        elif all(term % 2 != 0 for term in mons):
            m = mons[0]
            mons = [pow - m for pow in mons]
            return f"{self.expand_pow(m)}*({self.estrin(mons, cast_coeff, 2*power)})"
        elif all(term % 2 == 0 for term in mons):
            if mons[0] == 0:
                return self.estrin(mons, cast_coeff, 2 * power)
            else:
                m = mons[0]
                mons = [pow - m for pow in mons]
                return f"{self.expand_pow(m)}*({self.estrin(mons, cast_coeff, 2*power)})"
        else:
            rhs = self.estrin(mons, cast_coeff, power)

        return rhs

    def to_c(self):
        c_type = self.numeric_type.c_type()
        out = self.out_names[0]
        mons = self.polynomial.monomials
        cast_coeff = [c for c
                      in self.polynomial.coefficients]
        cast_in = self.in_names[0]

        rhs = self.eval_estrin(mons, cast_coeff, cast_in, 1, self.split)

        code = "{} {} = {};".format(c_type, out, rhs)
        return [code]
