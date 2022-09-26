

import lego_blocks
import numeric_types
import snake_egg_rules

import lambdas

from interval import Interval
from lambdas import types
from utils import Logger

# from wolframclient.evaluation import WolframLanguageSession
# from wolframclient.language import wl, wlexpr

from math import pi


logger = Logger(level=Logger.HIGH)


def is_even_function(func, egraph):
    arg = func.arguments[0]
    flipped_arg = -arg
    flipped = func.substitute(arg, flipped_arg)
    main_id = egraph.add(func.to_snake_egg(to_rule=False))
    flip_id = egraph.add(flipped.to_snake_egg(to_rule=False))
    logger("Egg says: {}equal", "not " if main_id != flip_id else "")
    logger("Flipped: {}", flipped)
    return main_id == flip_id


class MirrorAboutZeroX(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        assert (type(our_in_type) == types.Impl)
        assert (float(our_in_type.domain.inf) == 0.0)
        # assert (is_even_function(our_in_type.function))

        self.out_type = types.Impl(our_in_type.function,
                                   Interval(-our_in_type.domain.sup,
                                            our_in_type.domain.sup))

    def generate(self):
        so_far = super().generate()
        in_name = self.gensym("in")
        out_abs = so_far[0].in_names[0]
        sign = self.gensym("sign")
        abs = lego_blocks.Abs(numeric_types.fp64(), [in_name], [out_abs, sign])

        return [abs] + so_far

    @classmethod
    def generate_hole(cls, out_type, egraph):
        # We only output
        # (Impl (func) (- bound) bound)
        # where (func) is even
        if (type(out_type) != types.Impl
                or -float(out_type.domain.inf) != float(out_type.domain.sup)):
            return list()

        if not is_even_function(out_type.function, egraph):
            return list()

        # To get this output we need as input
        # (Impl (func) 0.0 bound)
        in_type = types.Impl(out_type.function,
                             Interval(0.0, out_type.domain.sup))
        return [lambdas.Hole(in_type)]
