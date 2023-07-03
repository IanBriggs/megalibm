

import fpcore
from fpcore.ast import Variable
import lego_blocks
from numeric_types import FPDD


class AssignDD(lego_blocks.LegoBlock):

    def __init__(self,
                 in_names:list,
                 out_names:list):
        super().__init__(FPDD, in_names, out_names)

        assert len(in_names) == 2
        assert len(out_names) == 1

    def to_c(self):
        cdecl = FPDD.c_type
        lines = [
            f"{cdecl} {self.out_names[0]} = Add12({self.in_names[0]}, {self.in_names[1]});"
        ]

        return lines