# Ideas from LibMs

## Things done to improve accuracy.

* perform some computations in higher precision
    + this can be doing some things in `double` for a `float` functions
    + more commonly this is doing "double-double" tricks as outlined in [this other doc](double_double_arithmetic.md)
    + notably it is rare to mix more than two higher precision types
* split the domain into multiple sections and have different approximations for each
* force usage of `fma`
    + especially useful in polynomial evaluation
* Different additive range reductions
    + [fma based](papers/correct_argument_reduction_using_fma.pdf)
    + cody-waite 
    + payne hanek (explaned in section 1.1 of [this paper](papers/modular_argument_reduction.pdf))
    + [high precision](papers/argument_reduction.pdf)
    + [modular](papers/modular_argument_reduction.pdf)
* If a square root is present in a compuatation before polynomial evaluation, then factor the polynomial


## Things done to improve speed

Note that things done to improve speed change over time as the relative costs of things change.
Table lookups used to be very cheap, but now are considered quite expensive on most systems.


* use other polynomial evaluation schemes
    + [Estrin Scheme](https://en.wikipedia.org/wiki/Estrin%27s_scheme)
    + ["fast polynomials"](papers/fast_polynomial.pdf)
* [type punn](https://en.wikipedia.org/wiki/Type_punning) to integer types for branch evaluation
* hand optimizing the "double-double" arithmetic to remove unused portions
* fixing polynomial coefficients to something fast to compute
    + e.g. forcing a coefficient to 1 means you can remove that multiply
    + e.g. powers of two can be turned into a bit-extract, integer add, and bit-recombine
* using vector instructions
    + this can be done by forcing tree vectorization in the compiler or hand coding vector intrinsic instructions in order to speed up the evaluation of one call
    + for far more wins the function can be made to evaluate multiple points at the same time (i.e. the function now takes 2, 4, 8, etc inputs and returns that many values)
