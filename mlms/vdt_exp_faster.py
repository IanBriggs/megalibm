import fpcore
import lambdas

from interval import Interval
from lambdas import *
from numeric_types import FP64

libm_func_name = "libm_vdt_exp"

lambda_function_name = "dsl_vdt_exp_faster"

input_ranges = [Interval("(- (/ (log 2) 2))", "(/ (log 2) 2)"), Interval("-20", "20"), Interval("0", "50")]

numeric_type = FP64

reference_filename = "vdt_exp.c"

exp = fpcore.parse("(FPCore (x) (exp x))")

exp_poly = \
    Estrin(
        MinimaxPolynomial(
            exp,
            Interval("(- (/ (log 2) 2))",
                     "(/ (log 2) 2)"),
            11),
        split=2)

lambda_expression = \
    Additive(log_2,
             exp_poly,
             fpcore.parse("(FPCore (y k) (* k (pow 2 k)))"),
             method="cody-waite",
             cw_bits=18,
             cw_len=2)
