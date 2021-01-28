

from passes.base import Pass




class SimpleAdditive(Pass):

    def __init__(self, numeric_type, in_var, out_var, k_var, period):
        super().__init__(numeric_type, in_var, out_var)
        self.k_var = k_var
        self.period = period


    def to_c(self):
        c_type = self.numeric_type.c_type()
        cast_in_var = "(({}){})".format(c_type, self.in_var)
        cast_period = "(({}){})".format(c_type, self.period)
        lines = [
            "int {} = floor({}/{});".format(self.k_var, cast_in_var, cast_period),
            "{} {} = {} - {}*{};".format(c_type, self.out_var,
                                         cast_in_var, self.k_var, cast_period),
        ]

        return lines


    def to_fptaylor(self, k):
        fpt_cast = self.numeric_type.fptaylor_cast()
        line = "{} {}= {} - {}*{};".format(self.out_var, fpt_cast, self.in_var,
                                           k, self.period)

        return [line]
