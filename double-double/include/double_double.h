/******************************************************************************/
/*  ____   __   _  _  ____  __    ____                                        */
/* (    \ /  \ / )( \(  _ \(  )  (  __)                                       */
/*  ) D ((  O )) \/ ( ) _ (/ (_/\ ) _)                                        */
/* (____/ \__/ \____/(____/\____/(____)                                       */
/*          ____   __   _  _  ____  __    ____     _  _                       */
/*         (    \ /  \ / )( \(  _ \(  )  (  __)   / )( \                      */
/*    ____  ) D ((  O )) \/ ( ) _ (/ (_/\ ) _)  _ ) __ (                      */
/*   (____)(____/ \__/ \____/(____/\____/(____)(_)\_)(_/                      */
/*                                                                            */
/* Compute in extra precision!                                                */
/*                                                                            */
/******************************************************************************/
/*  _    _  ___  ______ _   _ _____ _   _ _____  _____                        */
/* | |  | |/ _ \ | ___ \ \ | |_   _| \ | |  __ \/  ___|_                      */
/* | |  | / /_\ \| |_/ /  \| | | | |  \| | |  \/\ `--.(_)                     */
/* | |/\| |  _  ||    /| . ` | | | | . ` | | __  `--. \                       */
/* \  /\  / | | || |\ \| |\  |_| |_| |\  | |_\ \/\__/ /_                      */
/*  \/  \/\_| |_/\_| \_\_| \_/\___/\_| \_/\____/\____/(_)                     */
/* (inherited from double_access.h)                                           */
/* 1. Assumes IEEE754 binary double                                           */
/* 2. Does not care about endianess                                           */
/* 3. May have undefined behavior depending on language standard and compile  */
/*    time setting used                                                       */
/******************************************************************************/

#ifndef DOUBLE_DOUBLE_H
#define DOUBLE_DOUBLE_H

#include "asserts.h"
#include "double_access.h"
#include "double_helpers.h"

#include <math.h> /* for fma() */

/* Based on:                                                                  */
/* "CR-LIBM A library of correctly rounded elementary functions in            */
/*   double-precision"                                                        */
/* https://en.wikipedia.org/wiki/2Sum                                         */
/* "Library for Double-Double and Quad-Double Arithmetic"                     */

/******************************************************************************/
/*   ___  __   _  _  ____  __  __    ____    ____  __  _  _  ____             */
/*  / __)/  \ ( \/ )(  _ \(  )(  )  (  __)  (_  _)(  )( \/ )(  __)            */
/* ( (__(  O )/ \/ \ ) __/ )( / (_/\ ) _)     )(   )( / \/ \ ) _)             */
/*  \___)\__/ \_)(_/(__)  (__)\____/(____)   (__) (__)\_)(_/(____)            */
/*  ____  ____  ____  ____  __  __ _   ___  ____                              */
/* / ___)(  __)(_  _)(_  _)(  )(  ( \ / __)/ ___)                             */
/* \___ \ ) _)   )(    )(   )( /    /( (_ \\___ \                             */
/* (____/(____) (__)  (__) (__)\_)__) \___/(____/                             */
/*                                                                            */
/******************************************************************************/

/* Which TwoSum algorithm to use                                              */
/* 0: 6 addition/subtractions                                                 */
/* 1: 2 bit extractions, 1 conditional, 3 addition/subtractions               */
#ifndef TWO_SUM_ALGO
#define TWO_SUM_ALGO 1
#endif

/* Which conditional to use if TWO_SUM_ALGO == 1                              */
/* 0: 1 double compare                                                        */
/* 1: 2 integer extract, 1 integer compare                                    */
#ifndef TWO_SUM_ONE_COND
#define TWO_SUM_ONE_COND 1
#endif

/* Which TwoProd algorithm to use                                             */
/* 0: 2 constant multiplies, 4 multiplies, 10 addition/subtractions           */
/* 1: 1 multiply, 1 negation, 1 fma                                           */
#ifndef TWO_PROD_ALGO
#ifdef FP_FAST_FMA /* If FMA is fast then use it by default */
#define TWO_PROD_ALGO 1
#else
#define TWO_PROD_ALGO 0
#endif
#endif

typedef struct double_double
{
    /* double-double hi and lo */
    double hi;
    double lo;
} dd;

/******************************************************************************/
/*  ____  _  _  ____  __    __  ___                                           */
/* (  _ \/ )( \(  _ \(  )  (  )/ __)                                          */
/*  ) __/) \/ ( ) _ (/ (_/\ )(( (__                                           */
/* (__)  \____/(____/\____/(__)\___)                                          */
/*   __  __ _  ____  ____  ____  ____  __    ___  ____                        */
/*  (  )(  ( \(_  _)(  __)(  _ \(  __)/ _\  / __)(  __)                       */
/*   )( /    /  )(   ) _)  )   / ) _)/    \( (__  ) _)                        */
/*  (__)\_)__) (__) (____)(__\_)(__) \_/\_/ \___)(____)                       */
/*                                                                            */
/******************************************************************************/

/**
 * double-double = double + double
 */
static dd
Add12(
    double a,
    double b);

/**
 * double-double = double - double
 */
static dd
Sub12(
    double a,
    double b);

/**
 * double-double = double * double
 */
static dd
Mul12(
    double a,
    double b);

/**
 * double-double = sqrt(double)
 */
static dd
Sqrt12(
    double x);

/**
 * double-double = double-double + double-double
 */
static dd
Add22(
    dd a,
    dd b);

/**
 * double-double = double-double - double-double
 */
static dd
Sub22(
    dd a,
    dd b);

/**
 * double-double = double-double * double-double
 */
static dd
Mul22(
    dd a,
    dd b);

/**
 * double-double = double-double * double-double
 */
static dd
Div22(
    dd a,
    dd b);


/**
 * double-double = double * double-double
 */
static dd
Mul122(
    double a,
    dd b);

/**
 * double-double = fma(double, double-double, double-double)
 */
static dd
MulAdd212(
    double a,
    dd b,
    dd c);

/**
 * double-double = fma(double-double, double-double, double-double)
 */
static dd
MulAdd22(
    dd a,
    dd b,
    dd c);

/******************************************************************************/
/*  _  _  ____  __    ____  ____  ____  ____                                  */
/* / )( \(  __)(  )  (  _ \(  __)(  _ \/ ___)                                 */
/* ) __ ( ) _) / (_/\ ) __/ ) _)  )   /\___ \                                 */
/* \_)(_/(____)\____/(__)  (____)(__\_)(____/                                 */
/*                                                                            */
/* Helpers                                                                    */
/*                                                                            */
/******************************************************************************/

static inline dd
TwoSum(
    double a,
    double b)
{
    dd result;
    double a_prime, b_prime, delta_a, delta_b;
    result.hi = a + b;
    a_prime = result.hi - b;
    b_prime = result.hi - a_prime;
    delta_a = a - a_prime;
    delta_b = b - b_prime;
    result.lo = delta_a + delta_b;
    return result;
}

static inline dd
FastTwoSum(
    double a,
    double b)
{
    /* "... under the assumption that the exponent of a is at least as large  */
    /*  as the exponent of b" - wikipedia                                     */
    precondition(get_exponent_double(a) >= get_exponent_double(b));
    dd result;
    double z;
    result.hi = a + b;
    z = result.hi - a;
    result.lo = b - z;
    return result;
}

static inline dd
DoubleSafeFastTwoSum(
    double a,
    double b)
{
    if (a >= b)
    {
        return FastTwoSum(a, b);
    }
    else
    {
        return FastTwoSum(b, a);
    }
}

static inline dd
IntegerSafeFastTwoSum(
    double a,
    double b)
{
    /* "Note that if it is more efficient on a given architecture, the test   */
    /*  can be replaced with a test on the exponents of a and b" - CRLibm     */
    if (get_exponent_double(a) >= get_exponent_double(b))
    {
        return FastTwoSum(a, b);
    }
    else
    {
        return FastTwoSum(b, a);
    }
}

static inline dd
UsedTwoSum(
    double a,
    double b)
{
#ifndef TWO_SUM_ALGO
#error "TWO_SUM_ALGO must be set"
#elif TWO_SUM_ALGO == 0
    return TwoSum(a, b);
#elif TWO_SUM_ALGO == 1
#ifndef TWO_SUM_ONE_COND
#error "Since TWO_SUM_ALGO == 1, TWO_SUM_ONE_COND must be set"
#elif TWO_SUM_ONE_COND == 0
    return DoubleSafeFastTwoSum(a, b);
#elif TWO_SUM_ONE_COND == 1
    return IntegerSafeFastTwoSum(a, b);
#else
#error "Invalid TWO_SUM_ONE_COND selection"
#endif /* ifndef TWO_SUM_ONE_COND */
#else
#error "Invalid TWO_SUM_ALGO selection"
#endif /* ifndef TWO_SUM_ALGO */
}

static inline dd
Split(
    double a)
{
    dd res;
    double t, u;
    t = 134217729.0 * a; /* 2**27 + 1 */
    u = t - a;
    res.hi = t - u;
    res.lo = a - res.hi;
    return res;
}

static inline dd
TwoProd(
    double a,
    double b)
{
    dd result, a_sp, b_sp;
    double F, O, I, L, combine_0, combine_1, combine_2;
    result.hi = a * b;
    a_sp = Split(a);
    b_sp = Split(b);
    F = a_sp.hi * b_sp.hi;
    O = a_sp.hi * b_sp.lo;
    I = a_sp.lo * b_sp.hi;
    L = a_sp.lo * b_sp.lo;
    combine_0 = F - result.hi;
    combine_1 = combine_0 + O;
    combine_2 = combine_1 + I;
    result.lo = combine_2 + L;
    return result;
}

static inline dd
FastTwoProd(
    double a,
    double b)
{
    dd result;
    double neg_prod;
    result.hi = a * b;
    neg_prod = -(result.hi);
    result.lo = fma(a, b, neg_prod);
    return result;
}

static inline dd
UsedTwoProd(
    double a,
    double b)
{
#ifndef TWO_PROD_ALGO
#error "TWO_PROD_ALGO must be set"
#elif TWO_PROD_ALGO == 0
    return TwoProd(a, b);
#elif TWO_PROD_ALGO == 1
    return FastTwoProd(a, b);
#else
#error "Invalid TWO_PROD_ALGO selection"
#endif
}

static inline dd
FastAdd22(
    dd a,
    dd b)
{
    precondition(helper_abs(a.hi) > helper_abs(b.hi));
    dd result;
    double r, s;
    r = a.hi + b.hi;
    s = a.hi - r + b.hi + b.lo + a.lo;
    result.hi = r + s;
    result.lo = r - (result.hi) + s;
    return result;
}

/******************************************************************************/
/*  ____  _  _  __ _   ___  ____  __  __   __ _  ____                         */
/* (  __)/ )( \(  ( \ / __)(_  _)(  )/  \ (  ( \/ ___)                        */
/*  ) _) ) \/ (/    /( (__   )(   )((  O )/    /\___ \                        */
/* (__)  \____/\_)__) \___) (__) (__)\__/ \_)__)(____/                        */
/*                                                                            */
/* Functions                                                                  */
/*                                                                            */
/******************************************************************************/

static inline dd
Add12(
    double a,
    double b)
{
    return UsedTwoSum(a, b);
}

static inline dd
Sub12(
    double a,
    double b)
{
    return UsedTwoSum(a, -b);
}

static inline dd
Mul12(
    double a,
    double b)
{
    return UsedTwoProd(a, b);
}

static inline dd
Sqrt12(
    double x)
{
    double s, s2_hi, s2_lo, e;
    s = sqrt(x);
    e = (x - s * s) / (x + s);
    return UsedTwoSum(s, e);
}

static inline dd
Add22(
    dd a,
    dd b)
{
    if (helper_abs(a.hi) > helper_abs(b.hi))
    {
        return FastAdd22(a, b);
    }
    else
    {
        return FastAdd22(b, a);
    }
}

static inline dd
Sub22(
    dd a,
    dd b)
{
    b.hi = -b.hi;
    b.lo = -b.lo;
    return Add22(a, b);
}

static inline dd
Mul22(
    dd a,
    dd b)
{
    dd m, result;
    m = FastTwoProd(a.hi, b.hi);
    m.lo += a.hi * b.lo + a.lo * b.hi;
    result.hi = m.hi + m.lo;
    result.lo = m.hi - (result.hi) + m.lo;
    return result;
}

static inline dd
Div22(
    dd a,
    dd b)
{
    double ch, cl;
    dd u, result;
    ch = (a.hi) / (b.hi);
    u = Mul12(ch, b.hi);
    cl = ((((a.hi - u.hi) - u.lo) + a.lo) - ch*(b.lo))/(b.hi);
    result.hi = ch + cl;
    result.lo = (ch - (result.hi)) + cl;
    return result;
}

static inline dd
Mul122(
    double a,
    dd b)
{
    dd result, t;
    double t3, t4;
    t = Mul12(a, b.hi);
    t3 = a * b.lo;
    t4 = t.lo + t3;
    result = Add12(t.hi, t4);
    return result;
}

static inline dd
MulAdd212(
    double a,
    dd b,
    dd c)
{
    dd fma, t, t1;
    double t5, t6, t7, t8;
    t = Mul12(a, b.hi);
    t1 = Add12(c.hi, t.hi);
    t5 = b.lo * a;
    t6 = c.lo + t.lo;
    t7 = t5 + t6;
    t8 = t7 + t1.lo;
    fma = Add12(t1.hi, t8);
    return fma;
}

static inline dd
MulAdd22(
    dd a,
    dd b,
    dd c)
{
    dd fma, t, t1;
    double t5, t6, t7, t8, t9, t10;
    t = Mul12(a.hi, b.hi);
    t1 = Add12(c.hi, t.hi);
    t5 = a.hi * b.lo;
    t6 = a.lo * b.hi;
    t7 = t.lo + c.lo;
    t8 = t1.lo + t7;
    t9 = t5 + t6;
    t10 = t8 + t9;
    fma = Add12(t1.hi, t10);
    return fma;
}

#endif /* #ifndef DOUBLE_DOUBLE_H */