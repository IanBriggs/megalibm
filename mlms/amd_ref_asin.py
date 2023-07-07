import fpcore
import lambdas

from interval import Interval
from lambdas import *
from numeric_types import FP64

libm_func_name = "libm_amd_ref_asin"

lambda_function_name = "dsl_amd_ref_asin"

input_ranges = [Interval("0", "0.5"), Interval("-1", "1")]

numeric_type = FP64

reference_filename = "amd_ref_asin.c"

asin = fpcore.parse("(FPCore (x) (asin x))")
linear_cutoff = "1.38777878078144552146e-17"

lambda_expression = \
    InflectionLeft(
        InflectionRight(
            Horner(
                FixedMultiPolynomial(
                    asin,
                    Interval("0", "0.5"),
                    fpcore.parse("(FPCore (x p q) (+ x (* x (/ p q))))"),
                    [2, 4, 6, 8, 10, 12],
                    [" 0.227485835556935010735943483075",
                     "-0.445017216867635649900123110649",
                     " 0.275558175256937652532686256258",
                     "-0.0549989809235685841612020091328",
                     " 0.00109242697235074662306043804220",
                     " 0.0000482901920344786991880522822991"],
                    [0, 2, 4, 6, 8],
                    [" 1.36491501334161032038194214209",
                     "-3.28431505720958658909889444194",
                     " 2.76568859157270989520376345954",
                     "-0.943639137032492685763471240072",
                     " 0.105869422087204370341222318533"]), 
                     useDD=True),
            [ExprIfLess(None, fpcore.parse_expr("(sqrt (/ (- 1 x) 2))"), return_type="dd", compute="dd")],
            [ExprIfLess(None, fpcore.parse_expr("(- (/ PI 2) (* 2 y))"), "double", compute="dd")], useDD=True),
        fpcore.parse_expr("(- x)"),
        fpcore.parse_expr("(- y)"))