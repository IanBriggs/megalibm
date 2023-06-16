

import lego_blocks
from numeric_types import FP64, FPDD

ret_map = {
    "double": "double",
    "double-double": "dd"
}

comp_map = {
    "double": FP64,
    "dd": FPDD
}


class IfLess(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names, bound, 
                 true_val, false_val, return_type="double", compute_type="double", 
                 out_cast=False):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(self.in_names) == 1)
        assert (len(self.out_names) == 1)

        self.bound = bound
        self.true_val = true_val
        self.false_val = false_val
        self.return_type = ret_map[return_type]
        self.out_cast = out_cast
        self.compute_type = compute_type

    def __repr__(self):
        msg = "IfLess({}, {}, {}, {}, {}, {}, {})"
        return msg.format(repr(self.numeric_type),
                          repr(self.in_names),
                          repr(self.out_names),
                          repr(self.bound),
                          repr(self.true_val),
                          repr(self.false_val))

    def to_c(self):
        fmt = {
            "in": self.in_names[0].to_libm_c(),
            "bound": self.bound,
            "true_val": self.true_val,
            "false_val": self.false_val,
            "out": self.out_names[0].to_libm_c(),
            "type": self.return_type,
        }

        lines = [
            "{type} {out} = {in} <= {bound} ? {true_val} : {false_val};".format(
                **fmt),
        ]

        if self.return_type == ret_map["double-double"] and self.out_cast:
            fmt = {
                "ret": self.numeric_type.c_type,
                "var": self.out_names[0].to_libm_c() + "_lo",
                "val": self.out_names[0].to_libm_c() + ".lo;"
            }
            lines.append("{ret} {var} = {val}".format(**fmt))
            fmt = {
                "ret": self.numeric_type.c_type,
                "var": self.out_names[0].to_libm_c() + "_hi",
                "val": self.out_names[0].to_libm_c() + ".hi;"
            }
            lines.append("{ret} {var} = {val}".format(**fmt))

        return lines
