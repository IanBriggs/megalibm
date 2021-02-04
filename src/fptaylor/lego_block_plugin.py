
from numeric_types import NumericType, fp32, fp64

from utils.class_modifier import add_method

from lego_blocks.lego_block import LegoBlock

from lego_blocks.abs import Abs
from lego_blocks.case import Case
from lego_blocks.divide import Divide
from lego_blocks.multiply import Multiply
from lego_blocks.neg_flip import NegFlip
from lego_blocks.simple_additive import SimpleAdditive

from lego_blocks.forms.general import General
from lego_blocks.forms.horner import Horner


@add_method(NumericType)
def fptaylor_cast(self):
    raise NotImplementedError()

@add_method(NumericType)
def fptaylor_type(self):
    raise NotImplementedError()

@add_method(fp32)
def fptaylor_cast(self):
    return "rnd32",

@add_method(fp32)
def fptaylor_type(self):
    return "float32",

@add_method(fp64)
def fptaylor_cast(self):
    return "rnd64"

@add_method(fp64)
def fptaylor_type(self):
    return "float64"




@add_method(LegoBlock)
def to_fptaylor(self, *args):
    raise NotImplementedError()


@add_method(Abs)
def to_fptaylor(self):
    fmt = {
        "cast": self.numeric_type.fptaylor_cast,
        "in": self.in_names[0],
        "out": self.out_names[0],
    }

    lines = [
        "{out} {cast}= abs({in});".format(fmt),
    ]

    return lines


@add_method(Case)
def to_fptaylor(self, k):
    fmt = {
        "cast": self.numeric_type.fptaylor_cast,
        "out": self.out_names[0],
        "expr": self.cases[k%self.mod],
    }

    lines = [
        "{out} {cast}= {expr};".format(fmt),
    ]

    return lines


@add_mathod(Divide)
def to_fptaylor(self):
    fmt = {
        "cast": self.numeric_type.fptaylor_cast,
        "den": self.in_names[1],
        "num": self.in_names[0],
        "out": self.out_names[0],
    }

    lines = [
        "{out} {cast}= {num}/{den};".format(fmt),
    ]

    return lines


@add_mathod(Multiply)
def to_fptaylor(self):
    fmt = {
        "cast": self.numeric_type.fptaylor_cast,
        "out": self.out_names[0],
    }
    fmt["prods"] = "*".join([n for n in self.in_names])

    lines = [
        "{out} {cast}= {prods};".format(fmt),
    ]

    return lines


@add_mathod(NegFlip)
def to_fptaylor(self, sign):
    fmt = {
        "cast": self.numeric_type.fptaylor_cast,
        "in": self.in_names[0],
        "neg": "-" if sign else "",
        "out": self.out_names[0],
    }

    lines = [
        "{out} {cast}= {neg}{in};".format(fmt),
    ]

    return lines


@add_mathod(SimpleAdditive)
def to_fptaylor(self, k):
    fmt = {
        "cast": self.numeric_type.fptaylor_cast,
        "in": self.in_names[0],
        "k": k,
        "out": self.out_names[0],
        "period": self.period,
    }

    lines = [
        "{out} {cast}= {in} - {k}*{period};".format(fmt),
    ]

    return lines


@add_mathod(General)
def to_fptaylor(self):
    fpt_cast = self.numeric_type.fptaylor_cast
    parts = ["{}*{}^{}".format(c, self.in_var, m) for c, m
             in zip(self.polynomial.coefficients, self.polynomial.monomials)]
    rhs = " + ".join(parts)
    code = "{} {}= {};".format(self.out_var, fpt_cast, rhs)

    return [code]


@add_mathod(Horner)
def to_fptaylor(self):
    fpt_cast = self.numeric_type.fptaylor_cast()
    parts = list()
    mons = self.polynomial.monomials
    coef = self.polynomial.coefficients

    def expand_pow(n):
        return "*".join([self.in_var for _ in range(n)])

    if mons[0] == 0:
        parts.append("{} + ".format(coef[0]))
    else:
        parts.append("{}*({} + ".format(expand_pow(mons[0]), coef[0]))

    for i in range(1, len(mons)-1):
        this_power = mons[i] - mons[i-1]
        parts.append("{}*({} + ".format(expand_pow(this_power), coef[i]))

    final_power = mons[-1] - mons[-2]
    parts.append("{}*{}".format(expand_pow(final_power),
                                       coef[-1]))

    for i in range(1, len(mons)):
        parts.append(")")

    rhs = "".join(parts)
    code = "{} {}= {};".format(self.out_var, fpt_cast, rhs)

    return [code]
