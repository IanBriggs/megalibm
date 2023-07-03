

import fpcore
from fpcore.ast import Variable
import lego_blocks
from numeric_types import FPDD, NumericType


class AddDD(lego_blocks.LegoBlock):

    def __init__(self,
                 numeric_type:NumericType,
                 in_names:list,
                 out_names:list,):
        super().__init__(FPDD, in_names, out_names)

        assert len(in_names) == 2
        assert len(out_names) == 1
        self.numeric_type = numeric_type

    def to_c(self):
        cdecl = self.numeric_type.c_type
        tail = ""
        if cdecl != FPDD.c_type:
            tail = ".hi"
        lines = [
            f"{cdecl} {self.out_names[0]} = Add22({self.in_names[0]}, {self.in_names[1]}){tail};"
        ]

        return lines