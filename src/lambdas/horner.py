

import numeric_types
import lego_blocks.forms as forms
from lambdas import types




class Horner(types.Transform):

    def type_check(self):
        our_in_type = self.in_node.out_type
        assert(type(our_in_type) == types.Poly)

        self.out_type = types.Impl(our_in_type.function, our_in_type.domain)

    def generate(self):
        p = super().generate()
        in_name = self.gensym("in")
        out_name = self.gensym("out")
        return [forms.Horner(numeric_types.fp64(), [in_name], [out_name], p)]
