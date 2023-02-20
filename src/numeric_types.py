

class NumericType():

    def __init__(self):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()

    def c_abs(self):
        raise NotImplementedError()

    def c_const_suffix(self):
        raise NotImplementedError()

    def c_sign(self):
        raise NotImplementedError()

    def c_type(self):
        raise NotImplementedError()

    def half_pi(self):
        raise NotImplementedError()

    def pi(self):
        raise NotImplementedError()

    def quarter_pi(self):
        raise NotImplementedError()

    def sollya_type(self):
        raise NotImplementedError()


class fp32(NumericType):

    def __init__(self):
        pass

    def __repr__(self):
        return "fp32()"

    def c_abs(self):
        return "fabsf"

    def c_const_suffix(self):
        return "f"

    def c_sign(self):
        return "signbit"

    def half_pi(self):
        return "0x1.921fb6p+0"

    def pi(self):
        return "0x1.921fb6p+1"

    def quarter_pi(self):
        return "0x1.921fb6p-1"

    def sollya_type(self):
        return "single"

    def c_type(self):
        return "float"


class fp64(NumericType):

    def __init__(self):
        pass

    def __repr__(self):
        return "fp64()"

    def c_abs(self):
        return "fabs"

    def c_const_suffix(self):
        return ""

    def c_sign(self):
        return "signbit"

    def half_pi(self):
        return "0x1.921fb54442d18p+0"

    def pi(self):
        return "0x1.921fb54442d18p+1"

    def quarter_pi(self):
        return "0x1.921fb54442d18p-1"

    def sollya_type(self):
        return "double"

    def c_type(self):
        return "double"

    def c_pow(self):
        return "pow"

    def c_ldexp(self):
        return "ldexp"
