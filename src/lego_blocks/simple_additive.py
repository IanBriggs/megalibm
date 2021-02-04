

import lego_blocks




class SimpleAdditive(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names, period):
        super().__init__(numeric_type, in_names, out_names)
        assert(len(self.in_names) == 1)
        assert(len(self.out_names) == 2)
        #assert(type(period) == float)

        self.period = period


    def to_c(self):
        fmt = {
            "k": self.out_names[1],
            "out": self.out_names[0],
            "type": self.numeric_type.c_type(),
        }
        fmt["cast_in"] = "(({}){})".format(fmt["type"], self.in_names[0])
        fmt["cast_period"] = "(({}){})".format(fmt["type"], self.period)

        lines = [
            "int {k} = floor({cast_in}/{cast_period});".format(**fmt),
            "{type} {out} = {cast_in} - {k}*{cast_period};".format(**fmt),
        ]

        return lines
