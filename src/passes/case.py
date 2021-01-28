

from passes.base import Pass




class Case(Pass):

    def __init__(self, numeric_type, in_var, out_var, in_k, mod, cases):
        super().__init__(numeric_type, in_var, out_var)

        self.in_k = in_k
        self.mod = mod
        self.cases = cases


    def to_c(self):
        lines = [
            "{} {};".format(self.numeric_type.c_type(), self.out_var),
            "switch ({}%{}) {{".format(self.in_k, self.mod),
        ]

        for c in sorted(self.cases.keys()):
            val = self.cases[c]
            code_case = [
                "  case {}:".format(c),
                "    {} = {};".format(self.out_var, val),
                "    break;",
            ]
            lines += code_case

        final_case = [
            "  default:",
            "    assert(0);",
            "    return NAN;",
            "}",
        ]
        lines += final_case

        return lines


    def to_fptaylor(self, k):
        line = "{} {}= {};".format(self.out_var,
                                   self.numeric_type.fptaylor_cast(),
                                   self.cases[k%self.mod])
        return [line]
