

from passes.base import Pass




class NegFlip(Pass):

    def __init__(self, numeric_type, in_var, out_var, sign_var):
        super().__init__(numeric_type, in_var, out_var)
        self.sign_var = sign_var


    def to_c(self):
        c_type = self.numeric_type.c_type()
        line = "{} {} = {}==0 ? {} : -{};".format(c_type, self.out_var,
                                                  self.sign_var,
                                                  self.in_var, self.in_var)

        return [line]


    def to_fptaylor(self, sign):
        fpt_cast = self.numeric_type.fptaylor_cast()
        neg = "-" if sign else ""
        line = "{} {}= {}{};".format(self.out_var, fpt_cast, neg, self.in_var)

        return [line]

