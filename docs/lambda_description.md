# Lambda Language

We use a simple langauge to describe the structure of function implementations.


## Types

There are only three types in this language.

### `Poly<func, [low, high]>`

This is a polynomial approximating the function over the given domain.

### `Impl<func, [low, high]>`

This is an implementation of the function over the given domain.

### `Tuple<a, b>`

A Tuple


## Functions


### Function `(polynomial func low high monomials coefficients)`

__Return Type__: `Poly<func, [low, high]>`

__Conditions__:
 * `(<= (len monomials) (len coefficients))`
 * `(all-integers monomials)`
 * `(all-float-or-none coefficients)`


### Function `(general Poly<func,[low,high]>)`

__Return Type__: `Impl<func, [low, high]>`

__Conditions__: None


### Function `(horner Poly<func, [low, high]>)`

__Return Type__: `Impl<func, [low, high]>`

__Conditions__: None


### Function `(narrow Impl<func, [low, high]> new_low new_high)`
__Return Type__: `Impl<func, [new_low, new_high]>`
__Conditions__:
 * `(<= low new_low new_high high)`


### Function: `(double-angle Tuple<Impl<sin, [0.0, high_c]>,Impl<cos, [0.0, high_c]>>)`
__Return Type__: `Tuple<Impl<sin, [0.0, high]>,Impl<cos, [0.0, high]>>` where `high = (* 2 (min high_s high_c))`
__Conditions__: None


### Function: `(flip-about-zero-x Impl<func,[0.0,high]>)`
__Return Type__: `Impl<func, [-high, high]>`
__Conditions__:
  * `(is-odd func)`


### Function: `(mirror-about-zero-x Impl<func, [0.0, high]>)`
__Return Type__: `Impl<func, [-high, high]>`
__Conditions__:
  * `(is-even func)`


### Function: `(repeat-inf Impl<func, [0.0, high]>)`
__Return Type__: `Impl<func,0.0,inf>`
__Conditions__:
  * `(is-periodic func)`
  * `(has-period func period)`


### Function: `(repeat-flip Impl<func,[0.0,high]>)`
__Return Type__: `Impl<func, [0.0, new_high]>` where `new_high = (* 2 high)`
__Conditions__:
  * `(is-symmetric-x func 0.0 high 2*high)`


### Function: `(repeat-negate Impl<func, [0.0, high]>)`
__Return Type__: `Impl<func,[0.0,new_high]>` where `new_high = (* 2 high)`
__Conditions__:
  * `(is-negation func 0.0 high 2*high)`


### Function: `(make-tuple a b)`
__Return Type__: `Tuple<a, b>`
__Conditions__: None


### Function: `(first Tuple<a, b>)`
__Return Type__: `a`
__Conditions__: None


### Function: `(second Tuple<a, b>)`
__Return Type__: `b`
__Conditions__: None


