

from passes.base import Pass




class Abs(Pass):

    def __init__(self, numeric_type, in_var, out_var, sign_var):
        super().__init__(numeric_type, in_var, out_var)
        self.sign_var = sign_var


    def to_c(self):
        c_type = self.numeric_type.c_type()
        c_abs = self.numeric_type.c_abs()
        c_sign = self.numeric_type.c_sign()
        cast_var = "(({}){})".format(c_type, self.in_var)
        lines = [
            "int {} = {}({});".format(self.sign_var, c_sign, cast_var),
            "{} {} = {}({});".format(c_type, self.out_var, c_abs, cast_var),
        ]

        return lines


    def to_fptaylor(self):
        fpt_cast = self.numeric_type.fptaylor_cast()
        line = "{} {}= abs({});".format(self.out_var, fpt_cast, self.in_var)

        return [line]
