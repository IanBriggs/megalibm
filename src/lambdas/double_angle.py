
import lego_blocks
import numeric_types
from interval import Interval
from lambdas import types, hole



class DoubleAngle(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        assert(type(our_in_type) == types.Tuple)
        assert(type(our_in_type.a) == types.Impl)
        assert(type(our_in_type.b) == types.Impl)
        assert(our_in_type.a.function == "sin")
        assert(our_in_type.b.function == "cos")
        assert(our_in_type.a.domain.inf == 0.0)
        assert(our_in_type.b.domain.inf == 0.0)

        high = 2 * min(our_in_type.a.domain.sup, our_in_type.b.domain.sup)
        self.out_type = types.Tuple(types.Impl("sin", Interval(0.0, high)),
                                    types.Impl("cos", Interval(0.0, high)))

    @classmethod
    def generate_hole(cls, out_type):
        # We only output
        # (Tuple (Impl (sin arg) 0.0 high)
        #        (Impl (cos arg) 0.0 high))
        # with arg and high being free
        if type(out_type) != types.Tuple:
            return list()

        a = out_type.a
        if (type(a) != types.Impl
            or type(a.function.body) != fpcore.Operation
            or a.function.body.op != "sin"):
            return list()

        b = out_type.b
        if (type(b) != types.Impl
            or type(b.function.body) != fpcore.Operation
            or b.function.body.op != "cos"):
            return list()

        a_high = a.domain.sup
        b_high = b.domain.sup
        if (float(a.domain.inf) != 0.0
            or float(b.domain.inf) != 0.0
            or a_high != b_high):
            return list()

        a_arg = a.function.body.args[0]
        b_arg = b.function.body.args[0]
        if a_arg != b_arg:
            return list()

        # To get this output we need as input
        # (Tuple (Impl (sin arg) 0.0 (/ high 2))
        #        (Impl (cos arg) 0.0 (/ high 2)))
        in_type = types.Tuple(types.Impl(a.function, Interval(0.0, a_high/fpcore.ast.Number("2"))),
                              types.Impl(b.function, Interval(0.0, a_high/fpcore.ast.Number("2"))))
        return [lambdas.Hole(in_type)]
