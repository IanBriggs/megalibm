

from lego_blocks import forms




class General(forms.Form):

    def __init__(self, numeric_type, in_names, out_names, polynomial):
        super().__init__(numeric_type, in_names, out_names)
        assert(type(polynomial) == forms.Polynomial)

        self.polynomial = polynomial


    def __repr__(self):
        return "General({}, {}, {}, {}, {}, {})".format(repr(self.numeric_type),
                                                        repr(self.in_names),
                                                        repr(self.out_names),
                                                        repr(self.polynomial))


    def to_c(self):
        c_type = self.numeric_type.c_type()
        cast_in = "(({}){})".format(c_type, self.in_names[0])
        expanded_powers = ["*".join([cast_in for _ in range(m)])
                           for m in self.polynomial.monomials]
        parts = ["(({}){})*{}".format(c_type, c, e) for c, e
                 in zip(self.polynomial.coefficients, expanded_powers)]
        rhs = " + ".join(parts)
        code = "{} {} = {};".format(c_type, self.out_names[0], rhs)

        return [code]
