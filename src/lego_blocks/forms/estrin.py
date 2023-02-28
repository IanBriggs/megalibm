

from lego_blocks import forms
from fpcore.ast import ASTNode, Atom, Constant, FPCore, Operation, Number, Variable



class Estrin(forms.Form):

    def __init__(self, numeric_type, in_names, out_names, polynomial):
        super().__init__(numeric_type, in_names, out_names)
        assert (type(polynomial) == forms.Polynomial)

        self.polynomial = polynomial

    def __repr__(self):
        return "Estrin({}, {}, {}, {}, {}, {})".format(repr(self.numeric_type),
                                                       repr(self.in_names),
                                                       repr(self.out_names),
                                                       repr(self.polynomial))

    # def to_c(self):
    #     """ Suppose we want to evaluate c1 + c2x """
    #     c_type = self.numeric_type.c_type()
    #     out = self.out_names[0]
    #     cast_in = "(({}){})".format(c_type, self.in_names[0])
    #     # our_poly = Operation("+", Number("1"), Operation("+", Operation("*", Variable("x"), Number("2")), Operation("*", Operation("+", Number("3"), Operation("+", Operation("*", Variable("x"), Number("4")), Operation("*",  Variable("x"), Variable("x"))))))             
    #     # our_poly = Operation("+", Number("1"), Operation("*", Variable("x"), Number("2")))
    #     our_poly = Operation("+", Operation("+", Number("1"), Operation("*", Variable("x"), Number("2"))),Operation("*", Operation("+", Number("3"), Operation("*", Variable("x"), Number("4"))), Operation("*", Variable("x"), Variable("x"))))
    #     our_poly = our_poly.substitute(Variable("x"), Variable("in_0"))

    #     code = f"{c_type} {out} = {our_poly.to_libm_c2()};"
    #     c = f"{c_type} {out} = {our_poly.to_libm_c()};"
    #     print(c)
    #     return [code]

    def expand_pow(self, n):
        if n == 0:
            return ""
        c_type = self.numeric_type.c_type()
        cast_in = "(({}){})".format(c_type, self.in_names[0])
        return "*".join(cast_in for _ in range(n))

    def estrin(self, mons, groups, x_power):
        degree = mons[-1]

        if len(mons) <= 2:
            if len(mons) == 0:
                return f"{groups[0]}*{self.expand_pow(x_power)}"
            else:
                return f"{groups[0]} + \n {groups[1]}*{self.expand_pow(x_power)}"
        
        even = groups[0::2]
        odd = groups[1::2]
        new_groups = []

        for i, (a, b) in enumerate(zip(even, odd)):
            group = f"({a} + {b}*{self.expand_pow(x_power)})"
            new_groups.append(group)
        
        if len(even) > len(odd):
            new_groups.append(even[-1])

        new_len = len(new_groups)
        new_mons = mons[:new_len]

        return self.estrin(new_mons, new_groups, x_power * 2)


    def to_c(self):
        c_type = self.numeric_type.c_type()
        out = self.out_names[0]
        mons = self.polynomial.monomials
        cast_coeff = ["(({}){})".format(c_type, c) for c
                      in self.polynomial.coefficients]
        cast_in = "(({}){})".format(c_type, self.in_names[0])

        if all(term % 2 != 0 for term in self.polynomial.monomials):
            mons = [pow - 1 for pow in mons]
            rhs = f"{cast_in}*({self.estrin(mons, cast_coeff, 2)})"
        else:
            rhs = self.estrin(mons, cast_coeff, 1)


        code = "{} {} = {};".format(c_type, out, rhs)
        return [code]


