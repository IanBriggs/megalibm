

import fpcore
from fpcore.ast import Variable
import lego_blocks


class LegoFPCore(lego_blocks.LegoBlock):

    def __init__(self,
                 numeric_type,
                 in_names:list,
                 out_names:list,
                 fpc:fpcore.ast.FPCore):
        super().__init__(numeric_type, in_names, out_names)

        assert len(in_names) == len(fpc.arguments)
        assert len(out_names) == 1
        self.fpc = fpc

    def to_c(self):
        cdecl = self.numeric_type.c_type
        out = self.out_names[0]
        fpc = self.fpc
        for i in range(len(self.in_names)):
            fpc = fpc.substitute(fpc.arguments[i],
                                 Variable(self.in_names[i]))
        lines = [
            f"{cdecl} {out} = {fpc.body.to_libm_c()};"
        ]

        return lines