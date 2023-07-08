import fpcore
import lambdas

from interval import Interval
from lambdas import *
from lambdas.types import Impl
from numeric_types import FP64
from synthesize import paper_synthesize

libm_func_name = "libm_vdt_exp"

lambda_function_name = "dsl_vdt_exp_faster"

input_ranges = [Interval("(- (/ (log 2) 2))", "(/ (log 2) 2)"), Interval("-20", "20"), Interval("0", "50")]

numeric_type = FP64

reference_filename = "vdt_exp.c"

exp = fpcore.parse("(FPCore (x) (exp x))")
log_2 = fpcore.parse_expr("(log 2)")

# exp_poly = \
#     Estrin(
#         MinimaxPolynomial(
#             exp,
#             Interval("(- (/ (log 2) 2))",
#                      "(/ (log 2) 2)"),
#             11),
#         split=2)


# TODO: Ian, don't know how to pass split=2 to paper_synthesize
h = Hole(Impl(exp, Interval("(- (/ (log 2) 2))",
                     "(/ (log 2) 2)")))
exp_poly = paper_synthesize(h, tools=["fpminimax"], terms=[11], scheme="estrin")[0]
lambda_expression = \
    Additive(log_2,
             exp_poly,
             fpcore.parse("(FPCore (y k) (* k (pow 2 k)))"),
             method="cody-waite",
             cw_bits=18,
             cw_len=2)
