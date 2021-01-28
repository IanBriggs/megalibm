

from forms.form import Form
from utils.logging import Logger


logger = Logger()




class General(Form):

    def to_c(self):
        c_type = self.numeric_type.c_type()
        cast_in_var = "(({}){})".format(c_type, self.in_var)
        expanded_powers = ["*".join([cast_in_var for _ in range(m)])
                           for m in self.polynomial.monomials]
        parts = ["(({}){})*{}".format(c_type, c, e) for c, e
                 in zip(self.polynomial.coefficients, expanded_powers)]
        rhs = " + ".join(parts)
        code = "{} {} = {};".format(c_type, self.out_var, rhs)

        return [code]


    def to_fptaylor(self):
        fpt_cast = self.numeric_type.fptaylor_cast()
        parts = ["{}*{}^{}".format(c, self.in_var, m) for c, m
                 in zip(self.polynomial.coefficients, self.polynomial.monomials)]
        rhs = " + ".join(parts)
        code = "{} {}= {};".format(self.out_var, fpt_cast, rhs)

        return [code]
