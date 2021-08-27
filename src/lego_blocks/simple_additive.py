

import lego_blocks
import fpcore




class SimpleAdditive(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names, period):
        super().__init__(numeric_type, in_names, out_names)
        assert(len(self.in_names) == 1)
        assert(len(self.out_names) == 2)
        self.period = period


    def __repr__(self):
        return "SimpleAdditive({}, {}, {}, {})".format(repr(self.numeric_type),
                                                       repr(self.in_names),
                                                       repr(self.out_names),
                                                       repr(self.period))

    def to_c(self):
        fmt = {
            "k": self.out_names[1],
            "out": self.out_names[0],
            "type": self.numeric_type.c_type(),
        }
        inv_period = fpcore.ast.Operation("/", fpcore.ast.Number("1"), self.period)
        fmt["cast_in"] = "(({}){})".format(fmt["type"], self.in_names[0])
        fmt["cast_period"] = "(({}){})".format(fmt["type"], self.period.to_libm_c())
        fmt["cast_inv_period"] = "(({}){})".format(fmt["type"], inv_period.to_libm_c())

        lines = [
            "int {k} = (int) floor({cast_in}*{cast_inv_period});".format(**fmt),
            "{type} {out} = {cast_in} - {k}*{cast_period};".format(**fmt),
        ]

        return lines
