

import lego_blocks
import numeric_types
from interval import Interval
from lambdas import types

from math import pi



def is_negation_function(func, low, middle, high):
    if (func == "sin"
        and low == 0.0
        and middle == pi
        and high == 2*pi):
        return True
    if (func == "cos"
        and low == 0.0
        and middle == pi/2
        and high == pi):
        return True
    return False


class RepeatNegate(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        assert(type(our_in_type) == types.Impl)
        assert(our_in_type.domain.inf == 0.0)
        assert(is_negation_function(our_in_type.function,
                                    0.0,
                                    our_in_type.domain.sup,
                                    2*our_in_type.domain.sup))

        new_high = 2 * our_in_type.domain.sup
        self.out_type = types.Impl(our_in_type.function,
                             Interval(0, new_high))


    def generate(self):
        our_in_type = self.in_node.out_type
        so_far = super().generate()
        in_name = self.gensym("in")
        out_red = so_far[0].in_names[0]
        k = self.gensym("k")
        add = lego_blocks.SimpleAdditive(numeric_types.fp64(), [in_name], [out_red, k], our_in_type.domain.sup)

        in_case = so_far[-1].out_names[0]
        out_case = self.gensym("out")
        cases = {
            0: in_case,
            1: "-{}".format(in_case),
        }
        case = lego_blocks.Case(numeric_types.fp64(), [in_case, k], [out_case], 2, cases)

        return [add] + so_far + [case]
