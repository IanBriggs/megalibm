

import lego_blocks


class Divide(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(self.in_names) == 2)
        assert (len(self.out_names) == 1)

    def to_c(self):
        fmt = {
            "out": self.out_names[0],
            "type": self.numeric_type.c_type,
        }
        fmt["cast_den"] = "(({}){})".format(fmt["type"], self.in_names[1])
        fmt["cast_num"] = "(({}){})".format(fmt["type"], self.in_names[0])

        lines = [
            "{type} {out} = {cast_num}/{cast_den};".format(**fmt),
        ]

        return lines
