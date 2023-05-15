
from sympy import expand, simplify, trigsimp

import fpcore
from utils.logging import Logger

logger = Logger(level=Logger.EXTRA)


def sympy_based_equal(a: fpcore.ast.ASTNode, b: fpcore.ast.ASTNode) -> bool:
    """
    Symbolic equality testing for fpcore expressions

    Note: If True is returned it is guaranteed that the expressions are equal
          but, if False is returned the expressions may or may not be equal
    """
    a = a.to_sympy()
    b = b.to_sympy()

    # both == and .eq can't be used, see
    # https://docs.sympy.org/latest/explanation/gotchas.html
    attempts = [
        simplify(a - b),
        trigsimp(a - b),
        expand(a - b),
        expand(a - b, trig=True)
    ]

    return any(equation == 0 for equation in attempts)
