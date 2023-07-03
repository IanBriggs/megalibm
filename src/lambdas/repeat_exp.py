

from calculate_cody_waite_constants import calculate_cody_waite_constants
import interval
import lambdas
import lego_blocks
import numeric_types
from better_float_cast import better_float_cast
from interval import Interval
from lambdas import types
from utils import Logger

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

    def __init__(self,
                 in_node: types.Node,
                 bits_per: int,
                 entries: int):
        super().__init__(in_node)
        self.bits_per = bits_per
        self.entries = entries

    def type_check(self):
        self.in_node.type_check()
        our_in_type = self.in_node.out_type
        assert (type(our_in_type) == types.Impl)
        #assert (better_float_cast(our_in_type.domain.inf) == 0.0)

        self.out_type = types.Impl(our_in_type.function,
                                   Interval("0.0", "INFINITY"))

    def generate(self, numeric_type=numeric_types.FP64):
        self.type_check()
        so_far = super().generate()
        our_in_type = self.in_node.out_type
        in_name = self.gensym("in")
        out_red = so_far[0].in_names[0]
        k = self.gensym("k")
        constant = our_in_type.domain.sup - our_in_type.domain.inf
        period_strs = calculate_cody_waite_constants(constant,
                                                     self.bits_per,
                                                     self.entries)
        inv_period = 1 / self.constant
        inv_period = better_float_cast(inv_period)
        add = lego_blocks.CodyWaite(numeric_type,
                                    [in_name],
                                    [out_red, k],
                                    inv_period,
                                    period_strs,
                                    self.gensym)

        out_name = self.gensym("out")
        in_red = so_far[-1].out_names[0]
        ldexp = lego_blocks.SetExp(numeric_type,
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
            or better_float_cast(out_type.domain.inf) != 0.0
                or better_float_cast(out_type.domain.sup) != better_float_cast("inf")):
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
