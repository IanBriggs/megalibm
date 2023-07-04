

from fpcore.ast import Variable
import lego_blocks


class Neg(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names, expr):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(self.in_names) == 1)
        assert (len(self.out_names) == 1)
        self.expr = expr

    def to_c(self):
        cdecl = self.numeric_type.c_type

        in_name = self.in_names[0]
        out = self.out_names[0]

        new_expr = self.expr.substitute(Variable("y"), Variable(in_name))

        lines = [
            f"{cdecl} {out} = {new_expr.to_libm_c()};"
        ]

        return lines
