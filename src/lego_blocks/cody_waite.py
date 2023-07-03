
from better_float_cast import better_float_cast
from calculate_cody_waite_constants import calculate_cody_waite_constants
import lego_blocks
import fpcore


class CodyWaite(lego_blocks.LegoBlock):

    def __init__(self, numeric_type, in_names, out_names,
                 inv_period, period_strs,
                 gensym):
        super().__init__(numeric_type, in_names, out_names)
        assert (len(self.in_names) == 1)
        assert (len(self.out_names) == 2)
        self.inv_period = inv_period
        self.period_strs = period_strs
        self.gensym = gensym

    def to_c(self):
        cdecl = self.numeric_type.c_type

        cw_in = self.in_names[0]
        r = self.out_names[0]
        k = self.out_names[1]
        inv_period = self.gensym("inv_period")
        period = self.gensym("period")

        period_str = ",".join(self.period_strs)

        source_lines = [
            f"{cdecl} {inv_period} = {1/better_float_cast(self.period)};",
            f"{cdecl} {period}[{len(self.period_strs)}] = {{{period_str}}};",
            f"int {k};",
            f"{cdecl} {r} = fast_cody_waite_reduce({cw_in}, {inv_period}, {len(self.period_strs)}, {period}, &{k}, NULL);",
        ]

        return source_lines
