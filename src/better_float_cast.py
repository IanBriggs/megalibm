
def better_float_cast(x):
    # Catch non-string types
    try:
        return float(x)
    except ValueError as e:
        if type(x) != str:
            raise e

    x = x.strip()      # cleanup
    x = x.rstrip("f")  # drop C float suffix
    x = x.rstrip("d")  # drop C double suffix

    if x.startswith("0x") or x.startswith("-0x"):
        try:
            return float.fromhex(x)  # read as C's %a format
        except ValueError as e:
            raise e
    else:
        try:
            return float(x)  # try again
        except ValueError as e:
            raise e
