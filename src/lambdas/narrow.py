

from interval import Interval
from lambdas import types




class Narrow(types.Transform):

    def __init__(self, in_node, new_low, new_high):
        self.new_low = new_low
        self.new_high = new_high
        super().__init__(in_node)


    def type_check(self):
        our_in_type = self.in_node.out_type
        assert(type(our_in_type) == types.Impl)
        assert(our_in_type.domain.inf <= self.new_low)
        assert(self.new_low <= self.new_high)
        assert(self.new_high <= our_in_type.domain.sup)

        self.out_type = Impl(our_in_type.function,
                             Interval(self.new_low, self.new_high))


    def generate(self):
        return super().generate()
