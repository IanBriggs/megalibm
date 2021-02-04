

import lego_blocks
import numeric_types
from interval import Interval
from lambdas import types

from math import inf, pi



def is_periodic_function(func):
    return func in {"sin", "cos"}

def has_period_function(func, period):
    if func in {"sin", "cos"}:
        return period == 2*pi
    return False


class RepeatInf(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        assert(type(our_in_type) == types.Impl)
        assert(our_in_type.domain.inf == 0.0)
        assert(is_periodic_function(our_in_type.function))
        assert(has_period_function(our_in_type.function, our_in_type.domain.sup))

        self.out_type = types.Impl(our_in_type.function,
                             Interval(0.0, inf))


    def generate(self):
        our_in_type = self.in_node.out_type
        so_far = super().generate()
        in_name = self.gensym("in")
        out_red = so_far[0].in_names[0]
        k = self.gensym("k")
        add = lego_blocks.SimpleAdditive(numeric_types.fp64(), [in_name], [out_red, k], our_in_type.domain.sup)

        return [add] + so_far
