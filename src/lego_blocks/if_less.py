

import lego_blocks


class IfLess(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names, bound, tval, fval):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(self.in_names) == 1)
        assert (len(self.out_names) == 1)

        self.bound = bound
        self.tval = tval
        self.fval = fval

    def __repr__(self):
        msg = "IfLess({}, {}, {}, {}, {}, {}, {})"
        return msg.format(repr(self.numeric_type),
                          repr(self.in_names),
                          repr(self.out_names),
                          repr(self.bound),
                          repr(self.tval),
                          repr(self.fval))

    def to_c(self):
        fmt = {
            "in": self.in_names[0],
            "bound": self.bound,
            "tval": self.tval,
            "fval": self.fval,
            "out": self.out_names[0],
            "type": self.numeric_type.c_type(),
        }

        lines = [
            "{type} {out} = {in} < {bound} ? {tval} : {fval};".format(**fmt),
        ]

        return lines
