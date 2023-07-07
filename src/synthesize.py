
import math

import cmd_sollya
import fpcore
import lambdas
from dirty_equal import dirty_equal
from interval import Interval
from lego_blocks.forms.horner import tree_pow
from utils.logging import Logger

logger = Logger(color=Logger.green, level=Logger.LOW)

def synthesize(target, fuel=10):
    lam = lambdas.Hole(target)
    return paper_synthesize(lam,
                            tools=["tds", "remez"],
                            terms=[14],
                            fuel=fuel)

def paper_synthesize(lam,
                     tools:list=None,
                     terms: int=None, # for poly
                     powers: str="auto", # for poly
                     precisions: list=None, # for poly
                     fixed_terms: dict=None, # for poly
                     fuel=10):

    transforms = []
    if "tds" in tools:
        transforms = [
        lambdas.InflectionLeft,
        lambdas.InflectionRight,
        lambdas.Periodic,
        lambdas.PeriodicRecons
        ]

    # Each list item is a lambda expression with Hole elements
    completed = list()
    old_partials = [lam]
    for i in range(fuel):
        new_partials = list()
        for partial in old_partials:
            logger("Finishing partial impl: {}", partial)
            holes = partial.find_lambdas(lambda l: type(l) == lambdas.Hole)

            # The expression had no holes,
            if len(holes) == 0:
                completed.append(partial)
                continue

            # One hole
            found_at_least_one = False
            assert len(holes) == 1
            hole = holes.pop()

            # TDS part
            # See if any lambdas can create this hole
            for t in transforms:
                #logger("  trying: {}", t.__name__)
                hole_fillers = t.generate_hole(hole.out_type)
                for hf in hole_fillers:
                    found_at_least_one = True
                    filled = partial.replace_lambda(hole, hf)
                    logger("    filled: {}", str(filled))
                    new_partials.append(filled)

            # Polynomial synth part
            if hole.out_type.domain.isfinite():
                for t in terms:
                    if "taylor" in tools:
                        tay = fill_sollya_polynomial(hole.out_type.function,
                                                     hole.out_type.domain,
                                                     "taylor",
                                                     t,
                                                     powers,
                                                     precisions,
                                                     fixed_terms)
                        found_at_least_one = True
                        new_partials.append(partial.replace_lambda(hole, tay))
                    if "chebyshev" in tools:
                        tay = fill_sollya_polynomial(hole.out_type.function,
                                                     hole.out_type.domain,
                                                     "chebyshev",
                                                     t,
                                                     powers,
                                                     precisions,
                                                     fixed_terms)
                        found_at_least_one = True
                        new_partials.append(partial.replace_lambda(hole, tay))
                    if "remez" in tools:
                        tay = fill_sollya_polynomial(hole.out_type.function,
                                                     hole.out_type.domain,
                                                     "remez",
                                                     t,
                                                     powers,
                                                     precisions,
                                                     fixed_terms)
                        found_at_least_one = True
                        new_partials.append(partial.replace_lambda(hole, tay))
                    if "fpminimax" in tools:
                        tay = fill_sollya_polynomial(hole.out_type.function,
                                                     hole.out_type.domain,
                                                     "fpminimax",
                                                     t,
                                                     powers,
                                                     precisions,
                                                     fixed_terms)
                        found_at_least_one = True
                        new_partials.append(partial.replace_lambda(hole, tay))

            # Complain
            if not found_at_least_one:
                logger.warning("Unable to fill hole!")

        # Update list
        old_partials = new_partials

        # Early out
        if len(old_partials) == 0:
            break

        if i == fuel - 1:
            logger.warning("Ran out of fuel!")

    my_lambdas = list()
    for c in completed:
        logger("Type check on: {}", c)
        c.type_check()
        my_lambdas.append(c)

    return my_lambdas


def fill_sollya_polynomial(func: fpcore.ast.FPCore,
                           domain: Interval,
                           method: str,
                           terms: int,
                           powers: str="auto",
                           precisions: list=None,
                           fixed_terms: dict=None):
    if method not in {"fpminimax", "remez", "chebyshev", "taylor"}:
        raise TypeError(f"method must be one of fpminimax, remez, chebyshev, taylor")
    assert powers in {"odd", "even", "auto", "all"}
    assert type(terms) == int, "must provide `terms`"
    poly_terms = dict()

    # Taylor and chebyshev do not allow selecting powers, they automatically
    # match the odd/even properties of the func
    if method in {"taylor", "chebyshev"}:
        assert powers == "auto"
        assert fixed_terms == None

    # Fill fixed terms
    if fixed_terms is not None:
        for m,c in fixed_terms.items():
            assert type(m) == int
            poly_terms[m] = c

    # Decide if constant terms should be used, if not set
    try:
        if 0 not in poly_terms and func.eval(0) != 0:
            poly_terms[0] = None # signifies we should auto generate
    except ZeroDivisionError:
        pass

    # Find odd/even if needed
    if powers == "auto":
        f_x = func
        x = f_x.arguments[0]
        f_nx = f_x.substitute(x, -x)
        nf_nx = - f_nx

        if dirty_equal(f_x, f_nx, domain):
            powers = "even"
        elif dirty_equal(f_x, nf_nx, domain):
            powers = "odd"
        else:
            power = "all"

    # Fix known terms
    x = func.arguments[0]
    modeled_body = func.body
    for m,c in poly_terms.items():
        if c is not None:
            modeled_body -= fpcore.interface.num(c) * tree_pow(x, m)
    modeled_func = fpcore.ast.FPCore(None, [x], [], modeled_body)

    # Add Nones to signify values to synth
    step = 1 if powers == "all" else 2
    monomial = 2 if powers == "even" else 1
    while len(poly_terms) < terms:
        if monomial not in poly_terms:
            poly_terms[monomial] = None
        monomial += step

    # monomials for synth
    monomials = sorted([m for m,c in poly_terms.items() if c==None])

    # precisions for synth
    if precisions != None:
        assert method == "fpminimax"
        assert len(precisions) == len(monomials)
    else:
        precisions = ["double"]*len(monomials)

    # synth
    res = cmd_sollya.Result(modeled_func,
                            domain,
                            monomials,
                            precisions,
                            method)
    # get coefficients out
    for m,c in zip(monomials, res.coefficients):
        poly_terms[m] = fpcore.interface.num(c)
    poly = lambdas.Polynomial(poly_terms, split=1)

    # round up the epsilon just incase
    eps = cmd_sollya.DirtyInfNorm(poly.in_node.out_type.function, func, domain)
    scale = 2**23
    eps = math.ceil(eps*scale)/scale

    return lambdas.Approx(func, domain, eps, poly)