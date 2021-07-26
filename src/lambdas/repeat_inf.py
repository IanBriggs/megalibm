

import lego_blocks
import numeric_types
import fpcore

from interval import Interval
from lambdas import types
from utils import Logger

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

from math import pi


logger = Logger(level=Logger.HIGH)



def has_period_function(func, period):
    arg = func.arguments[0]
    flipped_arg = period + arg
    flipped = func.substitute(arg, flipped_arg)
    query = func - flipped
    logger("Query: {}", query)
    wolf_query = query.to_wolfram()
    logger("Wolf Query: {}", wolf_query)
    session = WolframLanguageSession()
    res = session.evaluate(wlexpr(wolf_query))
    logger("Wolf's Result: {}", res)
    return  res == 0


class RepeatInf(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        assert(type(our_in_type) == types.Impl)
        assert(float(our_in_type.domain.inf) == 0.0)
        assert(has_period_function(our_in_type.function, our_in_type.domain.sup))

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

        return [add] + so_far
