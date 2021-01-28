

from passes.base import Pass




class Divide(Pass):

    def __init__(self, numeric_type, in_var, out_var, in_den):
        super().__init__(numeric_type, in_var, out_var)

        self.in_den = in_den


    def to_c(self):
        line = "{} {} = {}/{};".format(self.numeric_type.c_type(),
                                       self.out_var,
                                       self.in_var,
                                       self.in_den)
        return [line]


    def to_fptaylor(self):
        line = "{} {} = {}/{};".format(self.numeric_type.fptaylor_round(),
                                       self.out_var,
                                       self.in_var,
                                       self.inden)
        return [line]
