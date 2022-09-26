

import lambdas
import lego_blocks
import numeric_types
import fpcore
import snake_egg_rules

from interval import Interval
from lambdas import types
from utils import Logger

# from wolframclient.evaluation import WolframLanguageSession
# from wolframclient.language import wl, wlexpr

from math import pi


logger = Logger(level=Logger.HIGH)


def is_symmetric_function(func, egraph, low, middle, high):
    # TODO: currently only made for symmetry starting at 0
    arg = func.arguments[0]
    flipped_arg = high - arg
    flipped = func.substitute(arg, flipped_arg)
    main_id = egraph.add(func.to_snake_egg(to_rule=False))
    flip_id = egraph.add(flipped.to_snake_egg(to_rule=False))
    logger("Egg says: {}equal", "not " if main_id != flip_id else "")
    logger("Flipped: {}", flipped)
    return main_id == flip_id


class RepeatFlip(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        old_high = our_in_type.domain.sup
        new_high = fpcore.ast.Operation("*", fpcore.ast.Number("2"), old_high)
        assert (type(our_in_type) == types.Impl)
        assert (float(our_in_type.domain.inf) == 0.0)
        # assert (is_symmetric_function(our_in_type.function,
        #                               0.0,
        #                               old_high,
        #                               new_high))

        self.out_type = types.Impl(our_in_type.function,
                                   Interval(0, new_high))

    def generate(self):
        our_in_type = self.in_node.out_type
        so_far = super().generate()
        in_name = self.gensym("in")
        out_red = self.gensym("out")
        k = self.gensym("k")
        add = lego_blocks.SimpleAdditive(numeric_types.fp64(),
                                         [in_name],
                                         [out_red, k],
                                         our_in_type.domain.sup)

        in_case = out_red
        out_case = so_far[0].in_names[0]
        cases = {
            0: in_case,
            1: "{}-{}".format(our_in_type.domain.sup.to_libm_c(), in_case),
        }
        case = lego_blocks.Case(numeric_types.fp64(), [
                                in_case, k], [out_case], 2, cases)

        return [add, case] + so_far

    @classmethod
    def generate_hole(cls, out_type, egraph):
        # We only output
        # (Impl (func) 0.0 (* 2 bound))
        # where (func) is symmetric for [0.0, bound] w.r.t. [bound, (* 2 bound)]
        if (type(out_type) != types.Impl
                or float(out_type.domain.inf) != 0.0):
            return list()

        two_bound = out_type.domain.sup
        bound = two_bound / fpcore.ast.Number("2")
        if not is_symmetric_function(out_type.function, egraph,
                                     0.0,
                                     bound,
                                     two_bound):
            return list()

        # To get this output we need as input
        # (Impl (func) 0.0 bound)
        in_type = types.Impl(out_type.function, Interval(0.0, bound))
        return [lambdas.Hole(in_type)]
