

from passes.base import Pass




class No(Pass):

    def to_c(self):
        c_type = self.numeric_type.to_c()
        rhs = "(({}){})".format(c_type, self.in_var)
        code = "{} {} = {};".format(c_type, self.out_var, rhs)

        return [code]


    def to_fptaylor(self):
        fpt_cast = self.numeric_type.fptaylor_cast()
        code = "{} {}= {};".format(self.out_var, fpt_type, self.in_var)

        return [code]
