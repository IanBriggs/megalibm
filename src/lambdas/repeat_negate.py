
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




# def is_negation_function(func, low, middle, high):
#     arg = func.arguments[0]
#     negated_arg = high - arg
#     negated = func.substitute(arg, negated_arg)
#     query = func + negated
#     logger("Query: {}", query)
#     wolf_query = query.to_wolfram()
#     logger("Wolf Query: {}", wolf_query)
#     with WolframLanguageSession() as session:
#         res = session.evaluate(wlexpr(wolf_query))
#         logger("Wolf's Result: {}", res)
#         return  res == 0


class RepeatNegate(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        old_high = our_in_type.domain.sup
        new_high = old_high * fpcore.ast.Number("2")
        assert(type(our_in_type) == types.Impl)
        assert(float(our_in_type.domain.inf) == 0.0)
        assert(snake_egg_rules.is_negation(our_in_type.function,
                                    0.0,
                                    old_high,
                                    new_high))

        self.out_type = types.Impl(our_in_type.function,
                             Interval(0, new_high))


    def generate(self):
        our_in_type = self.in_node.out_type
        so_far = super().generate()
        in_name = self.gensym("in")
        out_red = so_far[0].in_names[0]
        k = self.gensym("k")
        add = lego_blocks.SimpleAdditive(numeric_types.fp64(),
                                         [in_name],
                                         [out_red, k], our_in_type.domain.sup)

        in_case = so_far[-1].out_names[0]
        out_case = self.gensym("out")
        cases = {
            0: in_case,
            1: "-{}".format(in_case),
        }
        case = lego_blocks.Case(numeric_types.fp64(),
                                [in_case, k],
                                [out_case], 2, cases)

        return [add] + so_far + [case]

    @classmethod
    def generate_hole(cls, out_type):
        # We only output
        # (Impl (func) 0.0 (* 2 bound))
        # where (func) is a negation for [0.0, bound] w.r.t. [bound, (* 2 bound)]
        if (type(out_type) != types.Impl
            or float(out_type.domain.inf) != 0.0):
            return list()

        two_bound = out_type.domain.sup
        bound = two_bound / fpcore.ast.Number("2")
        if not snake_egg_rules.is_negation(out_type.function,
                                   0.0,
                                   bound,
                                   two_bound):
            return list()

        # To get this output we need as input
        # (Impl (func) 0.0 bound)
        in_type = types.Impl(out_type.function, Interval(0.0, bound))
        return [lambdas.Hole(in_type)]
