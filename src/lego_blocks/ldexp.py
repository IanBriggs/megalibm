import lego_blocks
import fpcore

class Ldexp(lego_blocks.LegoBlock):
    def __init__(self, numeric_type, in_names, out_names):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(in_names) == 2)
        assert (len(out_names) == 1)

    def to_c(self):
        fmt = {
            "out": self.out_names[0],
            "type": self.numeric_type.c_type(),
            "c_ldexp": self.numeric_type.c_ldexp(),
        }
        fmt["ldexp"] = "{}({}, {})".format(fmt["c_ldexp"], self.in_names[0], self.in_names[1])

        lines = [
            "{type} {out} = {ldexp};".format(**fmt),
        ]

        return lines