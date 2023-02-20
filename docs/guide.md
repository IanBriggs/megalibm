# General Guide

## Overall Goal

We want to make a tool that can take in a mathematical expression paired with a domain and create an assortment of implementaions of that expression that are valid on that domain.


### Lego Blocks

This is done through multiple levels of abstraction.
At the bottom there are `lego_blocks` that can be thought of as a higher level assembly.
These include basic operations like `abs` or `multiply`, and some larger pieces like `polynomial` or `simple_additive`.
For the most part these are made to connect the data flow between basic operations, that can then be asked to generate a C version of the computation.


### Lambdas

One level up is the `lambdas` language, described in the aptly named [lambda_description.md](lambda_description.md).
The `lambdas` make up a language where the expression being implemented and its domain are the type.
If a constructed expression in the `lambdas` language passes its `.type_check()` then it represents a reasonable version of the type.
Then the lambda expression can construct the lego blocks required.


### Type Synthesis

All parts of the lambda language either create or transform an implementation.
Knowing this, what we can do is start with a type we want at the end and see which lambda terms can output that type.
Then we can get a new type(s) that we want, or a completed expression in the lambda language.


