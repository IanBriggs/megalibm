

import numeric_types
import math




def generate_libm_c_code(typ, name):
    func = typ.function
    in_type = numeric_types.fp64().c_type()
    in_name = func.arguments[0]
    out_type = numeric_types.fp64().c_type()
    signature = "{} {}({} {})".format(out_type, name, in_type, in_name)
    signature_h = signature + ";"

    lines = [signature, "{"]

    expr = func.to_libm_c()

    lines.append("    return {};".format(expr))
    lines.append("}")

    return signature_h, lines
