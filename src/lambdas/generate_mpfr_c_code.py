

import math


def generate_mpfr_c_code(typ, name):
    func = typ.function

    func_lines, temps = func.to_mpfr_c("out")

    in_name = func.arguments[0]

    signature = "int {}(mpfr_t out, double dx)".format(name)
    signature_h = signature + ";"

    lines = [signature,
             "{",
             "  static int init_called = 0;",
             "  static mpfr_t {};".format(in_name),
             ]

    for tempnam in temps:
        lines.append("  static mpfr_t {};".format(tempnam))

    lines.append("  if (!init_called) {")
    lines.append("    mpfr_init2({}, ORACLE_PREC);".format(in_name))

    for tempnam in temps:
        lines.append("    mpfr_init2({}, ORACLE_PREC);".format(tempnam))

    lines.append("    init_called = 1;")
    lines.append("  }")

    lines.append("  mpfr_set_d({}, dx, MPFR_RNDN);".format(in_name))

    lines.extend(func_lines)

    lines.append("  return 0;")
    lines.append("}")

    return signature_h, lines
