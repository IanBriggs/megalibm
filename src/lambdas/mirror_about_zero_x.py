

import lego_blocks
import numeric_types

import lambdas

from interval import Interval
from lambdas import types
from utils import Logger

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

from math import pi


logger = Logger(level=Logger.HIGH)


def is_even_function(func):
    arg = func.arguments[0]
    flipped_arg = -arg
    flipped = func.substitute(arg, flipped_arg)
    query = func - flipped
    logger("Query: {}", query)
    wolf_query = query.to_wolfram()
    logger("Wolf Query: {}", wolf_query)
    with WolframLanguageSession() as session:
        res = session.evaluate(wlexpr(wolf_query))
        logger("Wolf's Result: {}", res)
        return  res == 0




class MirrorAboutZeroX(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        assert(type(our_in_type) == types.Impl)
        assert(float(our_in_type.domain.inf) == 0.0)
        assert(is_even_function(our_in_type.function))

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
    def generate_hole(cls, out_type):
        # We only output
        # (Impl (func) (- bound) bound)
        # where (func) is even
        if (type(out_type) != types.Impl
            or -float(out_type.domain.inf) != float(out_type.domain.sup)):
            return list()

        if not is_even_function(out_type.function):
            return list()

        # To get this output we need as input
        # (Impl (func) 0.0 bound)
        in_type = types.Impl(out_type.function,
                             Interval(0.0, out_type.domain.sup))
        return [lambdas.Hole(in_type)]
