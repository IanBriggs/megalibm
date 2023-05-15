import lego_blocks
import fpcore
from numeric_types import FP64


class SetExp(lego_blocks.LegoBlock):
    def __init__(self, numeric_type, in_names, out_names):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(in_names) == 2)
        assert (len(out_names) == 1)

    def to_c(self):
        c_type = self.numeric_type.c_type
        arg = self.in_names[0]
        n = self.in_names[1]
        out = self.out_names[0]

        assert self.numeric_type == FP64
        lines = [
            f"{c_type} {out} = {arg} * set_exponent_double(1.0, (uint16_t) {n}+1023);"
        ]

        return lines
