# Lambda Language

We use a simple language to describe the structure of function implementations.

The language has evolved over time with it's use.
This document is meant to be musings on what the end language should look like,
since it is in flux.

We want a small core langrage as well as syntactic sugar type functions.
Overall the goal is to generate code that can approximate a function over a
domain in floating point.

## Type: SimplePolynomial(function, domain)

Starting at the innermost, and simplest, part we have the _simple polynomial_.
It represents a single polynomial approximation of a function over a domain.
Mathematically this is something like
$c_0 + c_1 \cdot x + c_2 \cdot x^2 + \ldots$
We represent this as two lists pairing monomial power to coefficient constant.
For our purposes the monomial powers are non-negative integers.
These monomials are often full, even, or odd rank.
The polynomial itself is just the mathematical idea of a polynomial and not how
to implement it.
For a simple polynomial object to typecheck it will have to know its type
(function and domain) as well as these monomials and coefficients.

### Functions

#### `FixedSimplePolynomial(function, domain, monomials, coefficients)`

All required information is given.
This is used when copying a polynomial from a mathematics textbook, existing
source code, or other external source.

#### `RemezSimplePolynomial(function, domain, monomials|term_count)`

The function and domain must be given as well as some information about the
monomials.
This uses Sollya's Remez function to fill out the missing information.
Either a full list of monomials can be given, or just the length of monomials.
If the length is given then an attempt is made to characterize the function
as even or odd, and determine if a constant term should be included.

#### Other possible versions

* FPMinimax from Sollya would be a good way to find constants, and is
  applicable when the fp type is known.
* Taylor polynomials are what everybody says when you mention functions, so
  might be a good idea to include.
* Chebyshev from Sollya

## Type: CompoundPolynomial(function, domain)

A compound polynomial is two simple polynomials and a way to combine their
values.
This type was made due to how often we have seen multiple polynomials being
used to create an approximation.
The combining expression is phrased in terms of the polynomial values $p$ and
$q$ as well as the input $x$.
Importantly, the `SimplePolynomial` objects held will be missing their
describing function, since such a thing makes no sense for parts of a
compound polynomial.

### Functions

#### `CompoundPolynomial(p_polynomial, q_polynomial, combining_expression)`

This is the most generic form, which takes in two simple polynomials and a
way to combine them.

#### `RationalPolynomial(num_polynomial, den_polynomial)`

Sugar for $\frac{p}{q}$

## Type: Implementation(function, domain)

This is the most common type seen in our language.
What it means is that the corresponding object is able to generate code for
the function over the domain.
Some objects of this type take in a polynomial object, while most take in an
implementation and produce a new one with a different domain.

### Functions: polynomial to implementation

All of these can handle compound polynomials by applying the technique to the
simple polynomials individually and combining the results.

#### `GeneralForm(polynomial, fp_type)`

This uses the standard grade school style of implementation.
A full rank polynomial would be `c_0 + c_1*x + c_2*x*x + ...`.
The fp_type is used for the computations.

#### `HornerForm(polynomial, fp_type, break_out_terms)`

This uses Horner's method to implement the polynomial.
A full version implementing a polynomial with full rank starting at 1 and
coefficients denoted by $a$ through $d$ is `x*(a + x*(b + x*(c + x*d)))`
It might be better to break out the first term from this expression, to get
`x*a + x*x*(b + x*(c + x*d))`.