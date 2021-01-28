

from numeric_types.numeric_type import NumericType
from utils.logging import Logger


logger = Logger()




class FP64(NumericType):

    def __init__(self):
        pass


    def c_type(self):
        return "double"


    def c_abs(self):
        return "fabs"


    def c_sign(self):
        return "signbit"


    def fptaylor_cast(self):
        return "rnd64"


    def fptaylor_type(self):
        return "float64"


    def sollya_type(self):
        return "double"


    def pi(self):
        return "0x1.921fb54442d18p+1"


    def half_pi(self):
        return "0x1.921fb54442d18p+0"


    def quarter_pi(self):
        return "0x1.921fb54442d18p-1"
