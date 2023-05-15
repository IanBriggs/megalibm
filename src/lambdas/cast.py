from lego_blocks.cast import GenerateCast
import numeric_types
from lambdas import types



class TypeCast(types.Transform):

    def __init__(self, in_node: types.Node, frm: numeric_types.NumericType, to: numeric_types.NumericType):
        """
        Takes a polynomial and implements it using general form

        in_node: A polynomial
        """
        super().__init__(in_node)
        self.cast_in = frm
        self.cast_out = to

    def type_check(self):
        """ Check that the input is a polynomial """
        self.in_node.type_check()
        our_in_type = self.in_node.out_type

        assert type(our_in_type) == types.Impl

        assert(isinstance(self.cast_in(), (numeric_types.FP32, numeric_types.FP64)))
        assert(isinstance(self.cast_out(), (numeric_types.FP32, numeric_types.FP64)))

        self.out_type = types.Impl(our_in_type.function, our_in_type.domain)

    def generate(self, numeric_type=numeric_types.FP64):
        """ Implement a polynomial using the general form lego block """
        so_far = super().generate(numeric_type=numeric_type)

        x_in_name = self.gensym("x_in")
        out_name = so_far[0].in_names[0]


        inp = GenerateCast(numeric_type(),
                             [x_in_name],
                             [out_name],
                             self.cast_in().c_type())


        inner_name = so_far[-1].out_names[0]
        y_out_name = self.gensym("y_out")

        out = GenerateCast(numeric_type(),
                                [inner_name],
                                [y_out_name],
                                self.cast_out().c_type())

        return  [inp] + so_far + [out]
