

from passes.base import Pass




class Multiply(Pass):

    def __init__(self, numeric_type, in_var, out_var, in_vars):
        super().__init__(numeric_type, in_var, out_var)

        self.in_vars = in_vars


    def to_c(self):
        line = "{} {} = {};".format(self.numeric_type.c_type(),
                                    self.out_var,
                                    "*".join([self.in_var] + self.in_vars))
        return [line]


    def to_fptaylor(self):
        line = "{} {} = {};".format(self.numeric_type.fptaylor_round(),
                                    self.out_var,
                                    "*".join([self.in_var] + self.in_vars))
        return [line]
