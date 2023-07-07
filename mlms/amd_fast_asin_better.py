
import fpcore
from fpcore.interface import *
import lambdas

from interval import Interval
from lambdas import *
from lambdas.types import Impl
from numeric_types import FP64
from synthesize import paper_synthesize


libm_func_name = "libm_amd_fast_asin"

lambda_function_name = "dsl_amd_fast_asin_better"

input_ranges = [Interval("0", "0.5"), Interval("-1", "1")]

reference_filename = "amd_fast_asin.c"

numeric_type = FP64

fp_core_asin = fpcore.parse("(FPCore (x) (asin x))")


linear_cutoff = "2.1491193328907396e-08"
linear_region = Interval("0", linear_cutoff)

rest = Interval(linear_cutoff, "1")

core_region = Interval(linear_cutoff, "0.5")

x = fpcore.interface.var("x")

h = Hole(Impl(make_function([x], asin(x)), core_region))
poly_approx = paper_synthesize(h, tools=["fpminimax"], terms=[13], scheme="estrin")[0]

lambda_expression = \
    InflectionLeft(
        SplitDomain({
            linear_region:
                Approx(fp_core_asin, linear_region, 1e-16, Polynomial({1:"1"})),
            rest:
            InflectionRight(
                poly_approx,
                fpcore.parse_expr("(sqrt (/ (- 1 x) 2))"),
                fpcore.parse_expr("(- (/ PI 2) (* 2 y))"))}),
        fpcore.parse_expr("(- x)"),
        fpcore.parse_expr("(- y)"))
