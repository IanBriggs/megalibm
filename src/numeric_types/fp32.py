

from numeric_types.numeric_type import NumericType
from utils.logging import Logger


logger = Logger()




class FP32(NumericType):

    def __init__(self):
        pass


    def c_type(self):
        return "float"


    def c_abs(self):
        return "fabsf"


    def c_sign(self):
        return "signbit"


    def fptaylor_cast(self):
        return "rnd32"


    def fptaylor_type(self):
        return "float32"


    def sollya_type(self):
        return "single"


    def pi(self):
        return "0x1.921fb6p+1"


    def half_pi(self):
        return "0x1.921fb6p+0"


    def quarter_pi(self):
        return "0x1.921fb6p-1"
