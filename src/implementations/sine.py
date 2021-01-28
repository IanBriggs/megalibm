

from domain import Domain

from fptaylor.result import FPTaylorResult, CHECK_CONFIG

from error import Error

from forms.horner import Horner

from implementations.implementation import Implementation
from implementations.cosine import Cosine

from polynomial import Polynomial

from passes.abs import Abs
from passes.case import Case
from passes.neg_flip import NegFlip
from passes.no import No
from passes.multiply import Multiply
from passes.divide import Divide
from passes.simple_additive import SimpleAdditive

from sollya.result import SollyaResult

from utils.logging import Logger


logger = Logger(level=Logger.HIGH)





class Sine(Implementation):


    def __init__(self, numeric_type, name, domain, degree, FormType):
        super().__init__(numeric_type)
        self.name = name
        self.degree = degree
        self.domain = domain
        self.FormType = FormType
        self.passes = []

        mons = [i for i in range(1, 2*degree, 2)]
        conf = SollyaResult.default_config.copy()
        for _ in range(1):
            res = SollyaResult("sin(x)", domain, mons, numeric_type, conf)
            all_done = True
            for dom,tup in res.error.normal_errors.items():
                if tup[1] == "error":
                    all_done = False
                    break
            if all_done:
                for dom,tup in res.error.denormal_errors.items():
                    if tup[0] == "error":
                        all_done = False
                        break
            if all_done:
                break
            conf["prec"] *= 2

        pol = Polynomial("sin", mons, res.coefficients, domain)
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

        in_negflip = self.passes[-1].out_var
        out_negflip = self.gensym("out")
        self.passes += [NegFlip(numeric_type, in_negflip, out_negflip, sign)]


    def add_half_pi_reduction(self, numeric_type=None, additive_reduction=None):
        numeric_type = numeric_type or self.numeric_type
        additive_reduction = additive_reduction or SimpleAdditive

        # Stack case on before actual additive reduction
        k = self.gensym("k")
        in_case = self.gensym("in")
        out_case = self.passes[0].in_var
        hpi = numeric_type.half_pi()
        cases = {0: in_case, 1: "{}-{}".format(hpi, in_case),
                 2: in_case, 3: "{}-{}".format(hpi, in_case)}
        self.passes.insert(0, Case(numeric_type, in_case, out_case, k, 4, cases))

        in_add = self.gensym("in")
        out_add = self.passes[0].in_var
        self.passes.insert(0, additive_reduction(numeric_type, in_add, out_add, k, hpi))

        in_case = self.passes[-1].out_var
        out_case = self.gensym("out")
        cases = {0: in_case, 1: in_case,
                 2: "-{}".format(in_case),  3:"-{}".format(in_case)}
        self.passes += [Case(numeric_type, in_case, out_case, k, 4, cases)]


    def add_pi_reduction(self, numeric_type=None, additive_reduction=None):
        numeric_type = numeric_type or self.numeric_type
        additive_reduction = additive_reduction or SimpleAdditive

        in_add = self.gensym("in")
        out_add = self.passes[0].in_var
        k = self.gensym("k")
        self.passes.insert(0, additive_reduction(numeric_type, in_add, out_add, k, numeric_type.pi()))

        in_case = self.passes[-1].out_var
        out_case = self.gensym("out")
        cases = {0: in_case, 1: "-{}".format(in_case)}
        self.passes += [Case(numeric_type, in_case, out_case, k, 2, cases)]


    def add_double_angle(self, numeric_type=None, cos_impl=None):
        numeric_type = numeric_type or self.numeric_type
        if cos_impl == None:
            cos_impl = Cosine(numeric_type, None, self.domain, self.degree, self.FormType)


        in_sincos = self.passes[0].in_var
        cos_impl.passes[0].in_var = in_sincos
        out_cos = cos_impl.passes[-1].out_var
        self.passes = cos_impl.passes + self.passes

        in_first = self.gensym("in")
        out_div = in_sincos
        self.passes.insert(0, Divide(numeric_type, in_first, out_div, 2))

        out_sin = self.passes[-1].out_var

        out_final = self.gensym("out")
        self.passes += [Multiply(numeric_type, "2", out_final, [out_sin, out_cos])]


    def c_signature(self):
        nt = self.numeric_type
        return ["{} {}({} {})".format(nt.c_type(), self.name, nt.c_type(), self.passes[0].in_var)]

    def to_c(self):
        nt = self.numeric_type

        lines = self.c_signature() + ["{"]

        body = sum([["    "+bl for bl in p.to_c()] for p in self.passes], list())
        lines += body

        lines += [
            "    return {};".format(self.passes[-1].out_var),
            "}",
        ]

        return lines


    def to_fptaylor(self, k=None, sign=None):
        nt = self.numeric_type

        s = -1 if sign==True else 1

        lines = [
            "Variables",
            "    {} x in [{},{}];".format(nt.fptaylor_type(),
                                          *(self.domain.k(s*k).full_domain())),
            "",
            "Definitions",
        ]

        for p in self.passes:
            new_lines = None
            if type(p) == NegFlip:
                new_lines = p.to_fptaylor(sign)
            elif type(p) in {Case, SimpleAdditive}:
                new_lines = p.to_fptaylor(k)
            else:
                new_lines = p.to_fptaylor()

            lines += ["    "+l for l in new_lines]

        lines += [
            "",
            "Expressions",
            "    sin_x;",
        ]

        return lines


    def get_fptaylor_errors(self, upto_k):
        errors = dict()

        for k in range(-upto_k, upto_k+1):
            err = Error("FPTaylor")
            query = "\n".join(self.to_fptaylor(abs(k), k<0))
            res = FPTaylorResult(query, CHECK_CONFIG)
            err.add_normal_error(self.domain.k(k).full_domain(),
                                 res.result["absolute_errors"]["final_total"]["value"],
                                 None)
            errors[k] = err

        return errors


