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
static void
Add12(double *sum, double *error,
      double a,
      double b);

/**
 * double-double = double - double
 */
static void
Sub12(double *diff, double *error,
      double a,
      double b);

/**
 * double-double = double * double
 */
static void
Mul12(double *prod, double *error,
      double a,
      double b);

/**
 * double-double = sqrt(double)
 */
static void
Sqrt12(double *ans, double *error,
       double x);

/**
 * double-double = double-double + double-double
 */
static void
Add22(double *sum_hi, double *sum_lo,
      double a_hi, double a_lo,
      double b_hi, double b_lo);

/**
 * double-double = double-double - double-double
 */
static void
Sub22(double *diff_hi, double *diff_lo,
      double a_hi, double a_lo,
      double b_hi, double b_lo);

/**
 * double-double = double-double * double-double
 */
static void
Mul22(double *prod_hi, double *prod_lo,
      double a_hi, double a_lo,
      double b_hi, double b_lo);

/**
 * double-double = double * double-double
 */
static void
Mul122(double *prod_hi, double *prod_lo,
       double a,
       double b_hi, double b_lo);

/**
 * double-double = fma(double, double-double, double-double)
 */
static void
MulAdd212(double *fma_hi, double *fma_lo,
          double a,
          double b_hi, double b_lo,
          double c_hi, double c_lo);

/**
 * double-double = fma(double-double, double-double, double-double)
 */
static void
MulAdd22(double *fma_hi, double *fma_lo,
         double a_hi, double a_lo,
         double b_hi, double b_lo,
         double c_hi, double c_lo);

/******************************************************************************/
/*  _  _  ____  __    ____  ____  ____  ____                                  */
/* / )( \(  __)(  )  (  _ \(  __)(  _ \/ ___)                                 */
/* ) __ ( ) _) / (_/\ ) __/ ) _)  )   /\___ \                                 */
/* \_)(_/(____)\____/(__)  (____)(__\_)(____/                                 */
/*                                                                            */
/* Helpers                                                                    */
/*                                                                            */
/******************************************************************************/

static inline void
TwoSum(double *sum, double *error,
       double a,
       double b)
{
    double a_prime, b_prime, delta_a, delta_b;
    *sum = a + b;
    a_prime = *sum - b;
    b_prime = *sum - a_prime;
    delta_a = a - a_prime;
    delta_b = b - b_prime;
    *error = delta_a + delta_b;
}

static inline void
FastTwoSum(double *sum, double *error,
           double a,
           double b)
{
    /* "... under the assumption that the exponent of a is at least as large  */
    /*  as the exponent of b" - wikipedia                                     */
    precondition(get_exponent_double(a) >= get_exponent_double(b));
    double z;
    *sum = a + b;
    z = *sum - a;
    *error = b - z;
}

static inline void
DoubleSafeFastTwoSum(double *sum, double *error,
                     double a,
                     double b)
{
    if (a >= b)
    {
        FastTwoSum(sum, error, a, b);
    }
    else
    {
        FastTwoSum(sum, error, b, a);
    }
}

static inline void
IntegerSafeFastTwoSum(double *sum, double *error,
                      double a,
                      double b)
{
    /* "Note that if it is more efficient on a given architecture, the test   */
    /*  can be replaced with a test on the exponents of a and b" - CRLibm     */
    if (get_exponent_double(a) >= get_exponent_double(b))
    {
        FastTwoSum(sum, error, a, b);
    }
    else
    {
        FastTwoSum(sum, error, b, a);
    }
}

static inline void
UsedTwoSum(double *sum, double *error,
           double a,
           double b)
{
#ifndef TWO_SUM_ALGO
#error "TWO_SUM_ALGO must be set"
#elif TWO_SUM_ALGO == 0
    TwoSum(sum, error, a, b);
#elif TWO_SUM_ALGO == 1
#ifndef TWO_SUM_ONE_COND
#error "Since TWO_SUM_ALGO == 1, TWO_SUM_ONE_COND must be set"
#elif TWO_SUM_ONE_COND == 0
    DoubleSafeFastTwoSum(sum, error, a, b);
#elif TWO_SUM_ONE_COND == 1
    IntegerSafeFastTwoSum(sum, error, a, b);
#else
#error "Invalid TWO_SUM_ONE_COND selection"
#endif /* ifndef TWO_SUM_ONE_COND */
#else
#error "Invalid TWO_SUM_ALGO selection"
#endif /* ifndef TWO_SUM_ALGO */
}

static inline void
Split(double *hi, double *lo,
      double a)
{
    double t, u;
    t = 134217729.0 * a; /* 2**27 + 1 */
    u = t - a;
    *hi = t - u;
    *lo = a - *hi;
}

static inline void
TwoProd(double *prod, double *error,
        double a,
        double b)
{
    double a_hi, a_lo, b_hi, b_lo, F, O, I, L, combine_0, combine_1, combine_2;
    *prod = a * b;
    Split(&a_hi, &a_lo, a);
    Split(&b_hi, &b_lo, b);
    F = a_hi * b_hi;
    O = a_hi * b_lo;
    I = a_lo * b_hi;
    L = a_lo * b_lo;
    combine_0 = F - *prod;
    combine_1 = combine_0 + O;
    combine_2 = combine_1 + I;
    *error = combine_2 + L;
}

static inline void
FastTwoProd(double *prod, double *error,
            double a,
            double b)
{
    double neg_prod;
    *prod = a * b;
    neg_prod = -(*prod);
    *error = fma(a, b, neg_prod);
}

static inline void
UsedTwoProd(double *prod, double *error,
            double a,
            double b)
{
#ifndef TWO_PROD_ALGO
#error "TWO_PROD_ALGO must be set"
#elif TWO_PROD_ALGO == 0
    TwoPROD(prod, error, a, b);
#elif TWO_PROD_ALGO == 1
    FastTwoProd(prod, error, a, b);
#else
#error "Invalid TWO_PROD_ALGO selection"
#endif
}

static inline void
FastAdd22(double *sum_hi, double *sum_lo,
          double a_hi, double a_lo,
          double b_hi, double b_lo)
{
    precondition(helper_abs(a_hi) > helper_abs(b_hi));
    double r, s;
    r = a_hi + b_hi;
    s = a_hi - r + b_hi + b_lo + a_lo;
    *sum_hi = r + s;
    *sum_lo = r - (*sum_hi) + s;
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

static inline void
Add12(double *sum, double *error,
      double a,
      double b)
{
    UsedTwoSum(sum, error, a, b);
}

static inline void
Sub12(double *diff, double *error,
      double a,
      double b)
{
    UsedTwoSum(diff, error, a, -b);
}

static inline void
Mul12(double *prod, double *error,
      double a,
      double b)
{
    UsedTwoProd(prod, error, a, b);
}

static inline void
Sqrt12(double *ans, double *error,
       double x)
{
    double s, s2_hi, s2_lo, e;
    s = sqrt(x);
    e = (x - s * s) / (x + s);
    UsedTwoSum(ans, error, s, e);
}

static inline void
Add22(double *sum_hi, double *sum_lo,
      double a_hi, double a_lo,
      double b_hi, double b_lo)
{
    if (helper_abs(a_hi) > helper_abs(b_hi))
    {
        FastAdd22(sum_hi, sum_lo, a_hi, a_lo, b_hi, b_lo);
    }
    else
    {
        FastAdd22(sum_hi, sum_lo, b_hi, b_lo, a_hi, a_lo);
    }
}

static inline void
Sub22(double *diff_hi, double *diff_lo,
      double a_hi, double a_lo,
      double b_hi, double b_lo)
{
    Add22(diff_hi, diff_lo, a_hi, a_lo, -b_hi, -b_lo);
}

static inline void
Mul22(double *prod_hi, double *prod_lo,
      double a_hi, double a_lo,
      double b_hi, double b_lo)
{
    double m_hi, m_lo;
    FastTwoProd(&m_hi, &m_lo, a_hi, b_hi);
    m_lo += a_hi * b_lo + a_lo * b_hi;
    *prod_hi = m_hi + m_lo;
    *prod_lo = m_hi - (*prod_hi) + m_lo;
}

static inline void
Mul122(double *prod_hi, double *prod_lo,
       double a,
       double b_hi, double b_lo)
{
    double t1, t2, t3, t4;
    Mul12(&t1, &t2, a, b_hi);
    t3 = a * b_lo;
    t4 = t2 + t3;
    Add12(prod_hi, prod_lo, t1, t4);
}

static inline void
MulAdd212(double *fma_hi, double *fma_lo,
          double a,
          double b_hi, double b_lo,
          double c_hi, double c_lo)
{
    double t1, t2, t3, t4, t5, t6, t7, t8;
    Mul12(&t1, &t2, a, b_hi);
    Add12(&t3, &t4, c_hi, t1);
    t5 = b_lo * a;
    t6 = c_lo + t2;
    t7 = t5 + t6;
    t8 = t7 + t4;
    Add12(fma_hi, fma_lo, t3, t8);
}

static inline void
MulAdd22(double *fma_hi, double *fma_lo,
         double a_hi, double a_lo,
         double b_hi, double b_lo,
         double c_hi, double c_lo)
{
    double t1, t2, t3, t4, t5, t6, t7, t8, t9, t10;
    Mul12(&t1, &t2, a_hi, b_hi);
    Add12(&t3, &t4, c_hi, t1);
    t5 = a_hi * b_lo;
    t6 = a_lo * b_hi;
    t7 = t2 + c_lo;
    t8 = t4 + t7;
    t9 = t5 + t6;
    t10 = t8 + t9;
    Add12(fma_hi, fma_lo, t3, t10);
}

#endif /* #ifndef DOUBLE_DOUBLE_H */