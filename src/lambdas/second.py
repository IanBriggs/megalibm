

from lambdas import types




class Second(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        assert(type(our_in_type) == types.Tuple)

        self.out_type = our_in_type.b


    def generate(self):
        ga, gb = super().generate()
        return gb

    @classmethod
    def generate_hole(cls, out_type):
        # We output anything
        # (thing)
        # To get this output we need as input
        # (Tuple (do-not-care) (thing))
        return list()

    # TODO: this method
    # in_type = types.Impl(out_type.function, Interval(0.0, period))
    # return [lambdas.Hole(in_type)]
