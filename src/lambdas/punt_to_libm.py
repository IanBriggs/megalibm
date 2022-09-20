
import lambdas

import numeric_types
import lego_blocks.forms as forms
from lambdas import types
import math


class PuntToLibm(types.Source):

    def type_check(self):
        self.out_type = types.Impl(self.function, self.domain)

    def generate(self):
        in_name = self.gensym("in")
        out_name = self.gensym("out")
        return [forms.PuntToLibm(numeric_types.fp64(), [in_name], [out_name], self.function)]

    @classmethod
    def generate_hole(cls, out_type):
        # We only output
        # (Impl (func) low high)
        if (type(out_type) != types.Impl
            or not math.isfinite(float(out_type.domain.inf))
                or not math.isfinite(float(out_type.domain.sup))):
            return list()

        # To get this output we just need be contructed with given args
        return [(out_type.function, out_type.domain)]
