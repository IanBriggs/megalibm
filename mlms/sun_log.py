import fpcore
import lambdas

from interval import Interval
from lambdas import *
from numeric_types import FP64


libm_func_name = "libm_sun_log"

lambda_function_name = "dsl_sun_log"

input_ranges = [Interval("(+ (/ (sqrt 2) 2) 1)", "(+ (sqrt 2) 1)"),
                Interval("1", "50")]

numeric_type = FP64

reference_filename = "sun_log.c"

log = fpcore.parse("(FPCore (x) (log x))")
domain = Interval(fpcore.parse_expr("(/ (sqrt 2) 2)"),
                  fpcore.parse_expr("(sqrt 2)"))

x_to_f_remap = fpcore.parse("(FPCore (x) (- x 1))")
f_log = fpcore.parse("(FPCore (f) (log (+ f 1)))")
f_log_sub_f = fpcore.parse("(FPCore (f) (- (log (+ f 1)) f))")
f_domain = Interval(fpcore.parse_expr("(- (/ (sqrt 2) 2) 1)"),
                    fpcore.parse_expr("(- (sqrt 2) 1)"))

f_to_s_remap = fpcore.parse("(FPCore (f) (/ f (+ 2 f)))")
s_log = fpcore.parse("(FPCore (s) (- (log (+ 1 s)) (log (- 1 s))))")
s_log_sub_two_s = fpcore.parse(
    "(FPCore (s) (- (- (log (+ 1 s)) (log (- 1 s))) (* 2 s)))")
s_domain = Interval(
    fpcore.parse_expr("(/ (- (/ (sqrt 2) 2) 1) (+ 2 (- (/ (sqrt 2) 2) 1)))"),
    fpcore.parse_expr("(/ (- (sqrt 2) 1) (+ 2 (- (sqrt 2) 1)))"))

#zero_point = Interval(0, 0)
#zero_polynomial = Horner(FixedPolynomial(f_log, zero_point, [0], ["0"]))

mac_domain = Interval(-9.5367431640625e-7,
                      9.536743161842053950749686919152736663818359375e-7)
mac_polynomial = \
    Add(fpcore.parse_expr("f"),
        Horner(
            FixedPolynomial(f_log_sub_f,
                            mac_domain,
                            [2, 3],
                            ["-0.5", "0.3333333333333333"])))

extra_domain = Interval(0.3799991607666015625,
                        f_domain.sup)

extra_polynomial = \
    Recharacterize(
        f_log,
        f_to_s_remap,
        Rewrite(
            fpcore.parse_expr("(* 2 s)"),
            fpcore.parse_expr("(+ (- f (* (* f f) 0.5)) (* s (* (* f f) 0.5)))"),
            Add(fpcore.parse_expr("(* 2 s)"),
                Horner(
                FixedMultiPolynomial(
                    s_log_sub_two_s,
                    s_domain,
                    fpcore.parse(
                        "(FPCore (x p q) (* x (+ p q)))"),
                    [4, 8, 12],
                    ["3.999999999940941908e-01",
                     "2.222219843214978396e-01",
                     "1.531383769920937332e-01",],
                    [2, 6, 10, 14],
                    ["6.666666666666735130e-01",
                     "2.857142874366239149e-01",
                     "1.818357216161805012e-01",
                     "1.479819860511658591e-01"])),
                useDD=True)))

f_polynomial = \
    Recharacterize(
        f_log,
        f_to_s_remap,
        Rewrite(
            fpcore.parse_expr("(* 2 s)"),
            fpcore.parse_expr("(fma (- s) f f)"),
            Add(fpcore.parse_expr("(* 2 s)"),
                Horner(
                FixedMultiPolynomial(
                    s_log_sub_two_s,
                    s_domain,
                    fpcore.parse(
                        "(FPCore (x p q) (* x (+ p q)))"),
                    [4, 8, 12],
                    ["3.999999999940941908e-01",
                     "2.222219843214978396e-01",
                     "1.531383769920937332e-01",],
                    [2, 6, 10, 14],
                    ["6.666666666666735130e-01",
                     "2.857142874366239149e-01",
                     "1.818357216161805012e-01",
                     "1.479819860511658591e-01"])),
                useDD=True)))

lambda_expression = \
    Multiplicative(
        Recharacterize(
            log,
            x_to_f_remap,
            SplitDomain({
                #zero_point: zero_polynomial,
                mac_domain: mac_polynomial,
                extra_domain: extra_polynomial,
                f_domain: f_polynomial,
            },
                        useDD=True)), useDD=True)
