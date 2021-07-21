

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



def is_odd_function(func):
    arg = func.arguments[0]
    flipped_arg = -arg
    flipped = func.substitute(arg, flipped_arg)
    query = func + flipped
    logger("Query: {}", query)
    wolf_query = query.to_wolfram()
    logger("Wolf Query: {}", wolf_query)
    session = WolframLanguageSession()
    res = session.evaluate(wlexpr(wolf_query))
    logger("Wolf's Result: {}", res)
    return  res == 0



class FlipAboutZeroX(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        assert(type(our_in_type) == types.Impl)
        assert(float(our_in_type.domain.inf) == 0.0)
        assert(is_odd_function(our_in_type.function))

        self.out_type = types.Impl(our_in_type.function,
                                   Interval(fpcore.Operation("-", our_in_type.domain.sup),
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

