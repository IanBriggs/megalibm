

from utils.logging import Logger


logger = Logger()




class NumericType():

    def __init__(self):
        pass


    def c_type(self):
        raise NotImplementedError()


    def c_abs(self):
        raise NotImplementedError()


    def c_sign(self):
        raise NotImplementedError()


    def fptaylor_cast(self):
        raise NotImplementedError()


    def fptaylor_type(self):
        raise NotImplementedError()


    def sollya_type(self):
        raise NotImplementedError()


    def pi(self):
        raise NotImplementedError()


    def half_pi(self):
        raise NotImplementedError()


    def quarter_pi(self):
        raise NotImplementedError()
