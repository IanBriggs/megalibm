

from interval import Interval
from lambdas import types




class Narrow(types.Transform):

    def __init__(self, in_node, new_domain):
        self.new_domain = new_domain
        super().__init__(in_node)


    def __repr__(self):
        return "Narrow({}, {})".format(repr(self.in_node),
                                       repr(self.new_domain))


    def type_check(self):
        our_in_type = self.in_node.out_type
        assert(type(our_in_type) == types.Impl)
        assert(type(self.new_domain) == Interval)
        #assert(our_in_type.domain.inf <= self.new_domain.inf)
        #assert(self.new_domain.sup <= our_in_type.domain.sup)

        self.out_type = types.Impl(our_in_type.function, self.new_domain)


    def generate(self):
        return super().generate()
