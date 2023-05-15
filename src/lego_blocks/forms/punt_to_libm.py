

from fpcore.ast import Variable
from lego_blocks import forms


class PuntToLibm(forms.Form):

    def __init__(self, numeric_type, in_names, out_names, func):
        super().__init__(numeric_type, in_names, out_names)
        self.func = func

    def to_c(self):
        c_type = self.numeric_type.c_type
        in_var = Variable(self.in_names[0])
        out = self.out_names[0]

        var = self.func.arguments[0]
        func = self.func.substitute(var, in_var)
        expr = func.to_libm_c()

        code = "{} {} = {};".format(c_type, out, expr)

        return [code]
