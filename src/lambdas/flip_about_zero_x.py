

import lego_blocks
import numeric_types
import fpcore
import lambdas
import snake_egg_rules


from interval import Interval
from lambdas import types
from utils import Logger

# from wolframclient.evaluation import WolframLanguageSession
# from wolframclient.language import wl, wlexpr

from math import pi


logger = Logger(level=Logger.HIGH)



# def is_odd_function(func):
#     arg = func.arguments[0]
#     flipped_arg = -arg
#     flipped = func.substitute(arg, flipped_arg)
#     query = func + flipped
#     logger("Query: {}", query)
#     wolf_query = query.to_wolfram()
#     logger("Wolf Query: {}", wolf_query)
#     with WolframLanguageSession() as session:
#         res = session.evaluate(wlexpr(wolf_query))
#         logger("Wolf's Result: {}", res)
#         return  res == 0



class FlipAboutZeroX(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        assert(type(our_in_type) == types.Impl)
        assert(float(our_in_type.domain.inf) == 0.0)
        assert(snake_egg_rules.is_odd(our_in_type.function))

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

    @classmethod
    def generate_hole(cls, out_type):
        # We only output
        # (Impl (func) (- bound) bound)
        # where (func) is odd
        if (type(out_type) != types.Impl
            or -float(out_type.domain.inf) != float(out_type.domain.sup)):
            return list()

        if not snake_egg_rules.is_odd(out_type.function):
            return list()

        # To get this output we need as input
        # (Impl (func) 0.0 bound)
        in_type = types.Impl(out_type.function,
                             Interval(0.0, out_type.domain.sup))
        return [lambdas.Hole(in_type)]
