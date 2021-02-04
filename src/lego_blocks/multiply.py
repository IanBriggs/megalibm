

import lego_blocks




class Multiply(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names):
        super().__init__(numeric_type, in_names, out_names)
        assert(len(self.in_names) >= 2)
        assert(len(self.out_names) == 1)


    def to_c(self):
        fmt = {
            "out": self.out_names[0],
            "type": self.numeric_type.c_type(),
        }
        fmt["prods"] = "*".join(["(({}){})".format(fmt["type"], n)
                                 for n in self.in_names])

        lines = [
            "{type} {out} = {prods};".format(**fmt),
        ]

        return lines
