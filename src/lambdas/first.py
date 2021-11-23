

from lambdas import types




class First(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        assert(type(our_in_type) == types.Tuple)

        self.out_type = our_in_type.a


    def generate(self):
        ga, gb = super().generate()
        return ga

    @classmethod
    def generate_hole(cls, out_type):
        # We output anything
        # (thing)
        # To get this output we need as input
        # (Tuple (thing) (do-not-care))
        return list()

    # TODO: this method
    # in_type = types.Impl(out_type.function, Interval(0.0, period))
    # return [lambdas.Hole(in_type)]
