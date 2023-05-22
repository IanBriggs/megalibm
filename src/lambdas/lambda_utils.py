
from better_float_cast import better_float_cast
from fpcore.ast import FPCore
from numeric_types import FP32, FP64


def get_mirrors_at(func: FPCore, point):
    # Get all mirror identities
    decomposed_identities = func.decompose_identities()
    mirrors = decomposed_identities["mirror"]

    # See if (mirror point) is present
    f_point = better_float_cast(point)
    s_exprs = list()
    for s, t_arg in mirrors:
        # TODO: epsilon cmp is not proper here
        if t_arg.contains_op("thefunc"):
            continue
        if t_arg.is_constant() and abs(better_float_cast(t_arg) - f_point) < 1e-16:
            s_exprs.append(s)

    return s_exprs


def has_period(func: FPCore, period):
    # Get all period identities
    decomposed_identities = func.decompose_identities()
    periods = decomposed_identities["periodic"]

    # See if (periodic period) is present
    f_period = better_float_cast(period)
    for s, t_arg in periods:
        # TODO: epsilon cmp is not proper here
        if t_arg.contains_op("thefunc") or better_float_cast(t_arg) == 0.0:
            continue
        if abs(abs(better_float_cast(t_arg)) - f_period) < 1e-16:
            return True

    # Didn't find it
    return False


def get_mirrors(func: FPCore):
    # Get all mirror identities
    decomposed_identities = func.decompose_identities()
    mirrors = decomposed_identities["mirror"]
    return mirrors


def find_periods(func: FPCore):
    # Get all period identities
    decomposed_identities = func.decompose_identities()
    periods = decomposed_identities["periodic"]
    return periods


def generate_c_code(lam, name, numeric_type=FP64, func_type=FP64):
    passes = lam.generate(numeric_type=numeric_type)
    in_type = func_type.c_type
    in_name = passes[0].in_names[0]
    out_type = func_type.c_type
    out_name = passes[-1].out_names[0]
    signature = "{} {}({} {})".format(out_type, name, in_type, in_name)
    signature_h = signature + ";"

    lines = [
        signature,
        "{",
        "// {}".format(lam)
    ]

    for p in passes:
        lines += ["    " + l for l in p.to_c()]
    lines.append("    return {};".format(out_name))
    lines.append("}")

    return signature_h, lines


def generate_libm_c_code(typ, name, numeric_type=FP64):
    func = typ.function
    in_type = numeric_type.c_type
    in_name = func.arguments[0]
    out_type = numeric_type.c_type
    signature = "{} {}({} {})".format(out_type, name, in_type, in_name)
    signature_h = signature + ";"

    lines = [signature, "{"]

    expr = func.to_libm_c()

    lines.append("    return {};".format(expr))
    lines.append("}")

    return signature_h, lines


def generate_mpfr_c_code(typ, name, numeric_type=FP64):
    func = typ.function

    func_lines, temps = func.to_mpfr_c("out")

    in_name = func.arguments[0]

    cdecl = numeric_type.c_type
    signature = f"int {name}(mpfr_t out, {cdecl} fpx)"
    signature_h = signature + ";"

    lines = [signature,
             "{",
             "  static int init_called = 0;",
             "  static mpfr_t {};".format(in_name),
             ]

    for temp_name in temps:
        lines.append("  static mpfr_t {};".format(temp_name))

    lines.append("  if (!init_called) {")
    lines.append("    mpfr_init2({}, ORACLE_PREC);".format(in_name))

    for temp_name in temps:
        lines.append("    mpfr_init2({}, ORACLE_PREC);".format(temp_name))

    lines.append("    init_called = 1;")
    lines.append("  }")

    if numeric_type == FP64:
        lines.append("  mpfr_set_d({}, fpx, MPFR_RNDN);".format(in_name))
    elif numeric_type == FP32:
        lines.append("  mpfr_set_f({}, fpx, MPFR_RNDN);".format(in_name))
    else:
        raise NotImplementedError(f"Unknown numeric type '{numeric_type}'")

    lines.extend(func_lines)

    lines.append("  return 0;")
    lines.append("}")

    return signature_h, lines
