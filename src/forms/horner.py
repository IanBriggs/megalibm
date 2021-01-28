

from forms.form import Form
from utils.logging import Logger


logger = Logger()




class Horner(Form):

    def to_c(self):
        c_type = self.numeric_type.c_type()
        cast_in_var = "(({}){})".format(c_type, self.in_var)
        parts = list()
        mons = self.polynomial.monomials
        cast_coef = ["(({}){})".format(c_type, c) for c
                     in self.polynomial.coefficients]

        def expand_pow(n):
            return "*".join([cast_in_var for _ in range(n)])

        if mons[0] == 0:
            parts.append("{} + ".format(cast_coef[0]))
        else:
            parts.append("{}*({} + ".format(expand_pow(mons[0]),
                                                       cast_coef[0]))
        for i in range(1, len(mons)-1):
            this_power = mons[i] - mons[i-1]
            parts.append("{}*({} + ".format(expand_pow(this_power),
                                            cast_coef[i]))
        if len(mons) == 1:
            final_power = mons[0]
        else:
            final_power = mons[-1] - mons[-2]
        parts.append("{}*{}".format(expand_pow(final_power),
                                    cast_coef[-1]))

        for i in range(1, len(mons)-1):
            parts.append(")")

        if mons[0] != 0:
            parts.append(")")

        rhs = "".join(parts)
        code = "{} {} = {};".format(c_type, self.out_var, rhs)

        return [code]


    def to_fptaylor(self):
        fpt_cast = self.numeric_type.fptaylor_cast()
        parts = list()
        mons = self.polynomial.monomials
        coef = self.polynomial.coefficients
        def expand_pow(n):
            return "*".join([self.in_var for _ in range(n)])

        if mons[0] == 0:
            parts.append("{} + ".format(coef[0]))
        else:
            parts.append("{}*({} + ".format(expand_pow(mons[0]), coef[0]))

        for i in range(1, len(mons)-1):
            this_power = mons[i] - mons[i-1]
            parts.append("{}*({} + ".format(expand_pow(this_power), coef[i]))

        final_power = mons[-1] - mons[-2]
        parts.append("{}*{}".format(expand_pow(final_power),
                                       coef[-1]))

        for i in range(1, len(mons)):
            parts.append(")")

        rhs = "".join(parts)
        code = "{} {}= {};".format(self.out_var, fpt_cast, rhs)

        return [code]

