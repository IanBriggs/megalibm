

import lego_blocks


class Abs(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(self.in_names) == 1)
        assert (len(self.out_names) == 2)

    def to_c(self):
        fmt = {
            "c_abs": self.numeric_type.c_abs(),
            "c_sign": self.numeric_type.c_sign(),
            "out": self.out_names[0],
            "sign": self.out_names[1],
            "type": self.numeric_type.c_type(),
        }
        fmt["cast_in"] = "(({}){})".format(fmt["type"], self.in_names[0])

        lines = [
            "int {sign} = {c_sign}({cast_in});".format(**fmt),
            "{type} {out} = {c_abs}({cast_in});".format(**fmt),
        ]

        return lines
