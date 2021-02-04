

import lego_blocks
import numeric_types
from interval import Interval
from lambdas import types


def is_odd_function(func):
    return func == "sin"


class FlipAboutZeroX(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        assert(type(our_in_type) == types.Impl)
        assert(our_in_type.domain.inf == 0.0)
        assert(is_odd_function(our_in_type.function))

        self.out_type = types.Impl(our_in_type.function,
                                   Interval(-our_in_type.domain.sup,
                                            our_in_type.domain.sup))


    def generate(self):
        so_far = super().generate()
        in_name = self.gensym("in")
        out_abs = so_far[0].in_names[0]
        sign = self.gensym("sign")
        abs = lego_blocks.Abs(numeric_types.fp64(), [in_name], [out_abs, sign])

        in_negflip = so_far[-1].out_names[0]
        out_name = self.gensym("out")
        neg = lego_blocks.NegFlip(numeric_types.fp64(), [in_negflip, sign], [out_name])

        return [abs] + so_far + [neg]

