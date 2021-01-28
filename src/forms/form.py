

from utils.logging import Logger


logger = Logger()




class Form():

    def __init__(self, polynomial, numeric_type, in_var, out_var):
        self.polynomial = polynomial
        self.numeric_type = numeric_type
        self.in_var = in_var
        self.out_var = out_var


    def to_c(self):
        raise NotImplementedError()


    def to_fptaylor(self):
        raise NotImplementedError()
