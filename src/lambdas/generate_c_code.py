

import math




def generate_c_code(lam, name):
    passes = lam.generate()
    in_type = passes[0].numeric_type.c_type()
    in_name = passes[0].in_names[0]
    out_type = passes[-1].numeric_type.c_type()
    out_name = passes[-1].out_names[0]
    signature = "{} {}({} {})".format(out_type, name, in_type, in_name)
    signature_h = signature + ";"

    lines = [signature, "{"]

    for p in passes:
        lines += ["    "+l for l in p.to_c()]
    lines.append("    return {};".format(out_name))
    lines.append("}")

    return signature_h, lines
