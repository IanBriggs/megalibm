

from domain import Domain

from fptaylor.result import FPTaylorResult, CHECK_CONFIG

from error import Error

from forms.general import General
from forms.horner import Horner

from implementations.implementation import Implementation

from polynomial import Polynomial

from passes.abs import Abs
from passes.case import Case
from passes.neg_flip import NegFlip
from passes.no import No
from passes.simple_additive import SimpleAdditive

from sollya.result import SollyaResult

from utils.logging import Logger


logger = Logger(level=Logger.HIGH)





class Cosine(Implementation):

    def __init__(self, numeric_type, name, domain, degree, FormType):
        super().__init__(numeric_type)
        self.name = name
        self.passes = []

        mons = [i for i in range(degree+1)]
        res = SollyaResult("cos(x)", domain, mons, numeric_type)
        pol = Polynomial("cos", mons, res.coefficients, domain)
        pol.add_algorithmic_error(res.error)
        in_name = self.gensym("in")
        out_name = self.gensym("out")
        form = FormType(pol, numeric_type, in_name, out_name)
        self.passes.append(form)


    def add_abs(self, numeric_type=None):
        numeric_type = numeric_type or self.numeric_type

        in_abs = self.gensym("in")
        out_abs = self.passes[0].in_var
        sign = self.gensym("sign")
        self.passes.insert(0, Abs(numeric_type, in_abs, out_abs, sign))


    def add_half_pi_reduction(self, numeric_type=None, additive_reduction=None):
        numeric_type = numeric_type or self.numeric_type
        additive_reduction = additive_reduction or SimpleAdditive

        # Stack case on before actual additive reduction
        in_case = self.gensym("in")
        out_case = self.passes[0].in_var
        hpi = numeric_type.half_pi()
        cases = {0: in_case, 1: "{}-{}".format(hpi, in_case),
                 2: in_case, 3: "{}-{}".format(hpi, in_case)}
        self.passes.insert(0, Case(numeric_type, in_case, out_case, k, 4, cases))

        in_add = self.gensym("in")
        out_add = self.passes[0].in_var
        k = self.gensym("k")
        self.passes.insert(0, additive_reduction(numeric_type, in_add, out_add, k, hpi))

        in_case = self.passes[-1].out_name
        out_case = self.gensym("out")
        cases = {0: in_case, 1: "-{}".format(in_case),
                 2: in_case, 3: "-{}".format(in_case)}
        self.passes += Case(numeric_type, in_case, out_case, k, 2, cases)


    def add_pi_reduction(self, numeric_type=None, additive_reduction=None):
        numeric_type = numeric_type or self.numeric_type
        additive_reduction = additive_reduction or SimpleAdditive

        in_add = self.gensym("in")
        out_add = self.passes[0].in_var
        k = self.gensym("k")
        self.passes.insert(0, additive_reduction(numeric_type, in_add, out_add, k, numeric_type.pi()))

        in_case = self.passes[-1].out_name
        out_case = self.gensym("out")
        cases = {0: in_case, 1: "-{}".format(in_case)}
        self.passes += Case(numeric_type, in_case, out_case, k, 2, cases)


