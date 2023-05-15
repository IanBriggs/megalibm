import lego_blocks


class Pow(lego_blocks.LegoBlock):
    def __init__(self, numeric_type, in_names, out_names):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(in_names) == 2)
        assert (len(out_names) == 1)

    def to_c(self):
        fmt = {
            "out": self.out_names[0],
            "type": self.numeric_type.c_type,
            "c_pow": self.numeric_type.c_pow(),
        }
        fmt["power"] = "{}(({}){}, ({}){})".format(
            fmt["c_pow"], fmt["type"], self.in_names[0], fmt["type"], self.in_names[1])
        lines = [
            "{type} {out} = {power};".format(**fmt),
        ]
        return lines
