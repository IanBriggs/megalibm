

import fpcore
from fpcore.ast import Variable
import lego_blocks
from numeric_types import FPDD


class CreateDD(lego_blocks.LegoBlock):

    def __init__(self,
                 in_names:list,
                 out_names:list,
                 parts:list):
        super().__init__(FPDD, in_names, out_names)

        assert len(in_names) == 1
        assert len(out_names) == 1
        assert len(parts) == 2
        self.parts = parts

    def to_c(self):
        cdecl = FPDD.c_type
        lines = [
            f"{cdecl} {self.out_names[0]} = {{.hi = {self.in_names[0]}*{self.parts[0]}, .lo = {self.in_names[0]}*{self.parts[1]}}};"
        ]

        return lines