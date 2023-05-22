
from better_float_cast import better_float_cast
from mpmath_hex_str import mpmath_hex_str

import mpmath


class NumericType():

    def __init__(self):
        raise NotImplementedError()

    sollya_type = "NotImplemented"
    c_type = "NotImplemented"
    name = "NotImplemented"

    @classmethod
    def num_to_str(self, bound):
        raise NotImplementedError()


class FP32(NumericType):
    sollya_type = "single"
    c_type = "float"
    name = "FP32"

    @classmethod
    def num_to_str(self, x):
        # Keep integer values since they are easy to read
        double_x = better_float_cast(x)
        int_x = int(double_x)
        if double_x == int_x:
            lead_nonzero = bin(int_x).lstrip("0b").rstrip("0")
            if len(lead_nonzero) > 24:
                raise ValueError(f"Int too large for 32 bit float: {int_x}")
            return f"{int_x}.0f"

        # Others become %a form
        with mpmath.workprec(24):
            mpf_x = mpmath.mpf(x)
            hex_str = mpmath_hex_str(mpf_x)
            return f"{hex_str}f"


class FP64(NumericType):
    sollya_type = "double"
    c_type = "double"
    name = "FP64"

    @classmethod
    def num_to_str(self, x):
        # Keep integer values since they are easy to read
        double_x = better_float_cast(x)
        int_x = int(double_x)
        if double_x == int_x:
            lead_nonzero = bin(int_x).lstrip("0b").rstrip("0")
            if len(lead_nonzero) > 53:
                raise ValueError(f"Int too large for 64 bit float: {int_x}")
            return f"{int_x}.0"

        # Others become %a form
        return float.hex(double_x)


class FPDD(NumericType):
    sollya_type = "double"
    c_type = "double"
    name = "FPDD"

    @classmethod
    def num_to_str(self, x):
        # TODO
        double_x = better_float_cast(x)
        int_x = int(double_x)
        if double_x == int_x:
            lead_nonzero = bin(int_x).lstrip("0b").rstrip("0")
            if len(lead_nonzero) > 53:
                raise ValueError(f"Int too large for 64 bit float: {int_x}")
            return "{" + f"{int_x}.0" + ", 0.0}"

        # Others become %a form
        return "{" + float.hex(double_x) + ", 0.0}"


