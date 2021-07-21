 

from error import Error
from interval import Interval




class Polynomial():

    def __init__(self, modeled_function, monomials, coefficients, domain):
        assert(type(monomials) == list)
        assert(type(coefficients) == list)
        assert(all(type(m) == int for m in monomials))
        # assert(all(type(c) == float for c in coefficients))
        assert(len(monomials) == len(coefficients))
        assert(type(domain) == Interval)

        self.modeled_function = modeled_function
        paired = {m:c for m, c in zip(monomials, coefficients)}
        self.monomials = sorted(paired.keys())
        self.coefficients = [paired[m] for m in self.monomials]
        self.domain = domain
        self.algorithmic_errors = list()


    def add_algorithmic_error(self, error):
        assert(type(error) == Error)

        self.algorithmic_errors.append(error)

