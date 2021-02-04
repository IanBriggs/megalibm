
import lego_blocks
import numeric_types
from interval import Interval
from lambdas import types



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


