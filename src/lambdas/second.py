

from lambdas import types




class Second(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        assert(type(our_in_type) == types.Tuple)

        self.out_type = our_in_type.b


    def generate(self):
        ga, gb = super().generate()
        return gb
