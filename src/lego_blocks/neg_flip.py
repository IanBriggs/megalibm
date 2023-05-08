

import lego_blocks


class NegFlip(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(self.in_names) == 2)
        assert (len(self.out_names) == 1)

    def to_c(self):
        fmt = {
            "in": self.in_names[0],
            "out": self.out_names[0],
            "sign": self.in_names[1],
            "type": self.numeric_type.c_type,
        }

        lines = [
            "{type} {out} = {sign}==0 ? {in} : -{in};".format(**fmt),
        ]

        return lines
