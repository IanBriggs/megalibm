
from expect import expect_type
import fpcore
from fpcore.ast import Variable
from interval import Interval
import lambdas
import lego_blocks
import lego_blocks.forms as forms
from lambdas import types
from lego_blocks.forms.horner import tree_pow
from numeric_types import FP64, FPDD, NumericType

# Like in the paper!


def Polynomial(monomials_to_coefficients: dict,
               scheme: str = "horner",
               split: int = 0,
               ):
    # turn m,c into fpcore expression
    m_c = [(m, c) for m, c in monomials_to_coefficients.items()]
    m_c.sort(key=lambda t: t[0])
    x = fpcore.interface.var("x")
    terms = [c * tree_pow(x, m) for m, c in m_c]
    summer = terms[0]
    for t in terms[1:]:
        summer = summer + t
    poly_func = fpcore.interface.make_function([x], summer)

    poly = lambdas.FixedPolynomial(
        poly_func,
        Interval("(- INFINITY)", "INFINITY"),
        [t[0] for t in m_c],
        [t[1] for t in m_c])

    if scheme == "general":
        return lambdas.General(poly)
    elif scheme == "horner":
        return lambdas.Horner(poly, split)
    elif scheme == "estrn":
        return lambdas.Estrin(poly, split)
    else:
        raise TypeError("scheme must be one of general, horner, or estrin")
