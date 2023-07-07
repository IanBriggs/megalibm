import fpcore
import lambdas

from interval import Interval
from lambdas import *
from numeric_types import FP64

libm_func_name = "libm_vdt_exp"

lambda_function_name = "dsl_vdt_exp"

input_ranges = [Interval("(- (/ (log 2) 2))", "(/ (log 2) 2)"),
                Interval("-20", "20"),
                Interval("0", "50")
                ]

numeric_type = FP64

reference_filename = "vdt_exp.c"

exp = fpcore.parse("(FPCore (x) (exp x))")
log_2 = fpcore.parse_expr("(log 2)")

exp_poly = \
    Approx(exp, Interval("(- (/ (log 2) 2))", "(/ (log 2) 2)"), 1e-16,
           Add(Polynomial({0: "1"}),
               Mul(Polynomial({0: "2"}),
                   Div(Polynomial({
                       1: "9.99999999999999999910E-1",
                       3: "3.02994407707441961300E-2",
                       5: "1.26177193074810590878E-4"
                   }),
                   Sub(
                       Polynomial({
                           0: "2.00000000000000000009E0",
                           2: "2.27265548208155028766E-1",
                           4: "2.52448340349684104192E-3",
                           6: "3.00198505138664455042E-6"
                       }),
                       Polynomial({
                           1: "9.99999999999999999910E-1",
                           3: "3.02994407707441961300E-2",
                           5: "1.26177193074810590878E-4"
                       })
                   )
               ))))

lambda_expression = \
    Additive(log_2,
             exp_poly,
             fpcore.parse("(FPCore (y k) (* k (pow 2 k)))"),
             method="cody-waite",
             cw_bits=18,
             cw_len=2)
