

from utils.logging import Logger


logger = Logger()




class Pass():

    def __init__(self, numeric_type, in_var, out_var, *args):
        self.numeric_type = numeric_type
        self.in_var = in_var
        self.out_var = out_var


    def to_c(self):
        raise NotImplementedError()


    def to_fptaylor(self, *args):
        raise NotImplementedError()

