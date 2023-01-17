import lego_blocks
from fpcore.ast import Variable

class Expression(lego_blocks.LegoBlock):
    def __init__(self, numeric_type, in_names, out_names, expr):
        super().__init__(numeric_type, in_names, out_names, expr)
        assert (len(self.out_names) == 1)
        assert (len(self.in_names) == 2)
        self.expr = expr

    def __repr__(self):
        return f"Expression({repr(self.numeric_type)}, {repr(self.in_names)}, {repr(self.out_names)}, {repr(self.expr)})"

    def to_c(self):
        x, k = self.in_names
        recons = self.expr.substitute(Variable("x"), Variable(x))
        recons = recons.substitute(Variable("k"), Variable(k))
        s_str = recons.to_libm_c()

        fmt = {
            "out": self.out_names[0],
            "type": self.numeric_type.c_type(),
            "expr": s_str
        }

        lines = [
            "{type} {out} = {expr};".format(**fmt),
        ]
        return lines