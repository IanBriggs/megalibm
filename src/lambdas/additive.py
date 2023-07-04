import fpcore
from lambdas.cody_waite import CodyWaite
from lambdas.periodic_reconstruction import PeriodicRecons
from lambdas.repeat_exp import RepeatExp

# Like in the paper!


def Additive(p,
             impl,
             t_of_y_k,
             method="naive",
             cw_func=None,
             cw_bits=None,
             cw_len=None):
    if type(impl) == list:
        mod_cases = {i: c for i, c in enumerate(impl)}
        assert method == "cody-waite"
        assert type(cw_func) == fpcore.ast.FPCore
        assert type(cw_bits) == int
        assert type(cw_len) == int
        return CodyWaite(cw_func, p, mod_cases, cw_bits, cw_len)
    if t_of_y_k == fpcore.parse("(FPCore (y k) (* k (pow 2 k)))"):
        assert method == "cody-waite"
        assert cw_func == None
        assert type(cw_bits) == int
        assert type(cw_len) == int
        return RepeatExp(impl, cw_bits, cw_len)
    if method == "cody-waite":
        assert cw_func == None
        assert type(cw_bits) == int
        assert type(cw_len) == int
        return CodyWaite(impl.function, p, {0: impl}, cw_bits, cw_len)
    if method == "naive":
        assert cw_func == None
        assert cw_bits == None
        assert cw_len == None
        return PeriodicRecons(impl, p, t_of_y_k.body)
    raise TypeError(
        f"method must be one of naive, cody-waite, given: {method}")
