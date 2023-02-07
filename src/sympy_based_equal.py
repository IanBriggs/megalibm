
from sympy import simplify, trigsimp
import fpcore


def sympy_based_equal(a: fpcore.ast.ASTNode, b: fpcore.ast.ASTNode):
    """
    Symbolic equality testing for fpcore expressions

    Note: If True is returned it is guaranteed that the expressions are equal
          but, if False is returned the expressions may or may not be equal
    """
    print(f"a: {a}")
    print(f"b: {b}")
    a = a.to_sympy()
    b = b.to_sympy()

    # both == and .eq can't be used
    # https://docs.sympy.org/latest/explanation/gotchas.html
    print(f"a: {a}")
    print(f"b: {b}")
    eq = trigsimp(a - b)

    print(f"a-b: {eq}")

    return eq == 0
