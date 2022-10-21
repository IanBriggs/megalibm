

import lego_blocks
import numeric_types
import fpcore
import interval
import lambdas
import snake_egg_rules

from interval import Interval
from lambdas import types
from utils import Logger

# from wolframclient.evaluation import WolframLanguageSession
# from wolframclient.language import wl, wlexpr

from math import pi


logger = Logger(level=Logger.HIGH)


def has_period_function(func, egraph, period):
    arg = func.arguments[0]
    flipped_arg = period + arg
    flipped = func.substitute(arg, flipped_arg)
    main_id = egraph.add(func.to_snake_egg(to_rule=False))
    flip_id = egraph.add(flipped.to_snake_egg(to_rule=False))
    logger("Egg says: {}equal", "not " if main_id != flip_id else "")
    logger("Flipped: {}", flipped)
    return main_id == flip_id


class RepeatExp(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        assert (type(our_in_type) == types.Impl)
        assert (float(our_in_type.domain.inf) == 0.0)
#        assert (has_period_function(our_in_type.function, our_in_type.domain.sup))

        self.out_type = types.Impl(our_in_type.function,
                                   Interval("0.0", "INFINITY"))

    def generate(self):
        our_in_type = self.in_node.out_type
        so_far = super().generate()
        in_name = self.gensym("in")
        out_red = so_far[0].in_names[0]
        k = self.gensym("k")
        add = lego_blocks.SimpleAdditive(numeric_types.fp64(),
                                         [in_name],
                                         [out_red, k],
                                         our_in_type.domain.sup)

        out_name = self.gensym("out")
        in_red = so_far[0].out_names[0]
        ldexp = lego_blocks.Ldexp(numeric_types.fp64(),
                                     [in_red, k],
                                     [out_name])
                                     
        return [add] + so_far + [ldexp]

    @classmethod
    def generate_hole(cls, out_type, egraph):
        # Yash, don't worry about this function for now

        # We only output
        # (Impl (func) 0.0 INFINITY)
        # where (func) is periodic
        if (type(out_type) != types.Impl
            or float(out_type.domain.inf) != 0.0
                or float(out_type.domain.sup) != float("inf")):
            return list()

        # TODO: real periodicity test, for now just guess some pi values
        # only take the smallest
        period = None
        possible_periods = [
            interval.parse_bound("PI"),
            interval.parse_bound("(* 2 PI)"),
        ]
        for p in possible_periods:
            if has_period_function(out_type.function, egraph, p):
                period = p
                break

        if period == None:
            return list()

        # To get this output we need as input
        # (Impl (func) 0.0 period)
        in_type = types.Impl(out_type.function, Interval(0.0, period))
        return [lambdas.Hole(in_type)]
