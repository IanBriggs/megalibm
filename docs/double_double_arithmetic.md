# Double Double Arithmetic

These are ways to use multiple lower precision operation to perform higher precision.
Higher precision values are held as two floating point values whose mantissas do not overlap.
The possible dynamic range of the split type is the same as the base type.

These algorithms will be presented in C and assume that `flt` is typedef-ed for a floating point type with correctly rounded `+`, `-`, `*`, `/`, and `fma` operations.

In addition `finite`, `isinf`, `frexp`, and `ldexp` are also assumed to be present for `flt`.

The constant `mantissa_bits` is the number of mantissa bits in `flt`, including the implicit 1 bit.

Requirements for the algorithms to perform properly are given as `assume` statements.


## Helpers

These functions are used in those described below.

Simply extract the exponent.
There are more efficient variations that take advantage of the floating point representation in memory no shown here.

```C
int exponent(flt x) {
    int e;

    assume(finite(x));
    frexp(x, &e);
    return e;
}
```

Split a binary floating point value into two parts.

```C
void split(flit x,
           flt* x_lo, flt* x_hi) {
    const int half_bits_int;
    const flt two, flt_bits, pre_scale, oen, scale;
    flt scaled, diff;

    assume(finite(x));

    two = (flt) 2;
    flt_bits = (flt) mantissa_bits;
    half_bits = ceil(flt_bits / two);
    pre_scale = ldexp(1.0, half_bits);
    one = (flt) 1
    scale = pre_scale + one;

    scaled = scale * x;
    diff = scaled - x;
    *x_hi = scaled - diff;
    *x_lo = x - *x_hi;
}
```




## 2Sum

This algorithm takes in two floating point values and returns their sum in two part.
Often, this is viewed as the sum as well as its error.
It is often referred to as the Knuth or Møller sum.

```C
void two_sum(flt a, flt b,
             flt* sum, flt* err) {
    flt a_prime, b_prime, delta_a, delta_b;

    assume(finite(a));
    assume(finite(b));
    assume(!isinf(a + b));

    *sum = a + b;
    a_prime = *sum - b;
    b_prime = *sum - a_prime;
    delta_a = a - a_prime;
    delta_b = b - b_prime;
    *err = delta_a + delta_b;
}

```


## Fast2Sum

While reaching the same result as normal 2Sum, this algorithm is able works in only three operations.
It also has more strict requirements, as the number system must be radix 2 or 3.
It is also referred to as the Dekker algorithm or Quick Two Sum.

```C
void fast_two_sum(flt a, flt b,
                  flt* sum, flt* err) {
    flt z;

    assume(finite(a));
    assume(finite(b));
    assume(!isinf(a + b));
    assume(exponent(a) >= exponent(b));

    *sum = a + b;
    z = *sum - a;
    *err = b - z;
}
```


## 2Prod

The multiplication is performed by splitting the inputs and using a polynomial style FOIL multiplication.

This is then rearranged so that similar magnitude values are kept together.

$
a \cdot b - a \cdot b \\
= (a_{hi} + a_{lo}) \cdot (b_{hi} + b_{lo}) - a*b \\
= a_{hi} \cdot b_{hi} + a_{hi} \cdot b_{lo} + a_{lo} \cdot b_{hi} + a_{lo} \cdot b_{lo} - a*b \\
= a_{hi} \cdot b_{hi} - a \cdot b + a_{hi} \cdot b_{lo} + a_{lo} \cdot b_{hi} + a_{lo} \cdot b_{lo}
$

```C
void two_prod(flt a, flt b,
              flt* prod, flt* err) {
    flt a_hi, a_lo, b_hi, b_lo, F, O, I, L, combine_0, combine_1, combine_2;

    assume(finite(a));
    assume(finite(b));
    assume(!isinf(a * b));

    *prod = a * b;
    split(a, &a_hi, &a_lo);
    split(b, &b_hi, &b_lo);
    F = a_hi * b_hi;
    O = a_hi * b_lo;
    I = a_lo * b_hi;
    L = a_lo * b_lo;
    combine_0 = F - prod;
    combine_1 = combine_0 + O;
    combine_2 = combine_1 + I;
    *err = combine_2 + L;
}
```


## Fast2Prod

This requires fma be available.

```C
void fast_two_prod(flt a, flt b,
                   flt* prod, flt* err) {
    flt neg_prod;

    assume(finite(a));
    assume(finite(b));
    assume(!isinf(a * b));

    *prod = a * b;
    neg_prod = -(*prod);
    *err = fma(a, b, neg_prod);
}
```