

import fpcore
from fpcore.ast import Variable
import lego_blocks
from numeric_types import FPDD


class LegoFPCore(lego_blocks.LegoBlock):

    def __init__(self,
                 numeric_type,
                 in_names:list,
                 out_names:list,
                 fpc:fpcore.ast.FPCore,
                 return_type: str = "double"):
        super().__init__(numeric_type, in_names, out_names)

        assert len(in_names) == len(fpc.arguments)
        assert len(out_names) == 1
        self.fpc = fpc
        self.return_type = return_type

    def to_c(self):
        cdecl = self.return_type
        typ = type(self.out_names[0])
        out = self.out_names[0] if typ == str else self.out_names[0].to_libm_c()
        fpc = self.fpc
        for i in range(len(self.in_names)):
            in_type = type(self.in_names[i])
            inner_name = Variable(self.in_names[i]) if in_type != Variable else self.in_names[i]
            fpc = fpc.substitute(fpc.arguments[i],
                                 inner_name)
        lines = [
            f"{cdecl} {out} = {fpc.body.to_libm_c(numeric_type=self.numeric_type)};"
        ]

        return lines