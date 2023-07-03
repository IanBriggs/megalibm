

from better_float_cast import better_float_cast
import lego_blocks
import fpcore


class SimpleAdditive(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names, offset, period):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(self.in_names) == 1)
        assert (len(self.out_names) == 2)
        self.period = period
        self.offset = offset

    def __repr__(self):
        return "SimpleAdditive({}, {}, {}, {}, {})".format(repr(self.numeric_type),
                                                       repr(self.in_names),
                                                       repr(self.out_names),
                                                       repr(self.offset),
                                                       repr(self.period))

    def to_c(self):
        fmt = {
            "k": self.out_names[1],
            "out": self.out_names[0],
            "type": self.numeric_type.c_type,
            "suffix": self.numeric_type.suffix
        }
        inv_period = fpcore.ast.Operation(
            "/", fpcore.ast.Number("1"), self.period)
        inv_period_value = better_float_cast(inv_period.eval(assignment={}))
        period_value = better_float_cast(self.period.eval(assignment={}))
        fmt["cast_in"] = "(({}){})".format(fmt["type"], self.in_names[0])
        fmt["cast_period"] = "(({}){}{})".format(
            fmt["type"], period_value, fmt["suffix"])
        fmt["cast_inv_period"] = "(({}){}{})".format(
            fmt["type"], inv_period_value, fmt["suffix"])
        fmt["cast_offset"] = "(({}){}{})".format(fmt["type"], better_float_cast(self.offset), fmt["suffix"])
        lines = [
            "int {k} = (int) floor(({cast_in}-{cast_offset})*{cast_inv_period});".format(**fmt),
            "{type} {out} = {cast_in} - {k}*{cast_period};".format(**fmt),
        ]

        return lines
