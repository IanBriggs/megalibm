

from interval import Interval


class RationalPolynomial():

    def __init__(self, modeled_function, offset,
                 numerator_monomials, numerator_coefficients,
                 denominator_monomials, denominator_coefficients,
                 domain):
        self.modeled_function = modeled_function
        self.offset = offset
        numerator_paired = {m: c for m, c in zip(numerator_monomials,
                                                 numerator_coefficients)}
        self.numerator_monomials = sorted(numerator_paired.keys())
        self.numerator_coefficients = [numerator_paired[m] for m in self.numerator_monomials]
        denominator_paired = {m: c for m, c in zip(denominator_monomials,
                                                 denominator_coefficients)}
        self.denominator_monomials = sorted(denominator_paired.keys())
        self.denominator_coefficients = [denominator_paired[m] for m in self.denominator_monomials]
        self.domain = domain
        self.algorithmic_errors = list()

    def add_algorithmic_error(self, error):
        assert (type(error) == Error)

        self.algorithmic_errors.append(error)
