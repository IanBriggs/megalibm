

from utils.logging import Logger


logger = Logger()




class Polynomial():

    def __init__(self, modeled_function, monomials, coefficients, domain):
        self.modeled_function = modeled_function
        paired = {m:c for m, c in zip(monomials, coefficients)}
        self.monomials = sorted(paired.keys())
        self.coefficients = [paired[m] for m in self.monomials]
        self.domain = domain
        self.algorithmic_errors = list()


    def add_algorithmic_error(self, error):
        self.algorithmic_errors.append(error)

