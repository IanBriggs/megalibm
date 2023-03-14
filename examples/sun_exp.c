/*
 * Modified source from Sun's math library as updated by freemint
 * Modifications were made to allow the file to be compiled on its own.
 * The function has been renamed to sun_exp.
 */

/* @(#)e_exp.c 1.3 95/01/18 */
/*
 * ====================================================
 * Copyright (C) 1993 by Sun Microsystems, Inc. All rights reserved.
 *
 * Developed at SunSoft, a Sun Microsystems, Inc. business.
 * Permission to use, copy, modify, and distribute this
 * software is freely granted, provided that this notice
 * is preserved.
 * ====================================================
 */

/* __ieee754_exp(x)
 * Returns the exponential of x.
 *
 * Method
 *   1. Argument reduction:
 *      Reduce x to an r so that |r| <= 0.5*ln2 ~ 0.34658.
 *	Given x, find r and integer k such that
 *
 *               x = k*ln2 + r,  |r| <= 0.5*ln2.
 *
 *      Here r will be represented as r = hi-lo for better
 *	accuracy.
 *
 *   2. Approximation of exp(r) by a special rational function on
 *	the interval [0,0.34658]:
 *	Write
 *	    R(r**2) = r*(exp(r)+1)/(exp(r)-1) = 2 + r*r/6 - r**4/360 + ...
 *      We use a special Reme algorithm on [0,0.34658] to generate
 * 	a polynomial of degree 5 to approximate R. The maximum error
 *	of this polynomial approximation is bounded by 2**-59. In
 *	other words,
 *	    R(z) ~ 2.0 + P1*z + P2*z**2 + P3*z**3 + P4*z**4 + P5*z**5
 *  	(where z=r*r, and the values of P1 to P5 are listed below)
 *	and
 *	    |                  5          |     -59
 *	    | 2.0+P1*z+...+P5*z   -  R(z) | <= 2
 *	    |                             |
 *	The computation of exp(r) thus becomes
 *                             2*r
 *		exp(r) = 1 + -------
 *		              R - r
 *                                 r*R1(r)
 *		       = 1 + r + ----------- (for better accuracy)
 *		                  2 - R1(r)
 *	where
 *			         2       4             10
 *		R1(r) = r - (P1*r  + P2*r  + ... + P5*r   ).
 *
 *   3. Scale back to obtain exp(x):
 *	From step 1, we have
 *	   exp(x) = 2^k * exp(r)
 *
 * Special cases:
 *	exp(INF) is INF, exp(NaN) is NaN;
 *	exp(-INF) is 0, and
 *	for finite argument, only exp(0)=1 is exact.
 *
 * Accuracy:
 *	according to an error analysis, the error is always less than
 *	1 ulp (unit in the last place).
 *
 * Misc. info.
 *	For IEEE double
 *	    if x >  7.09782712893383973096e+02 then exp(x) overflow
 *	    if x < -7.45133219101941108420e+02 then exp(x) underflow
 *
 * Constants:
 * The hexadecimal values are the intended ones for the following
 * constants. The decimal values may be used, provided that the
 * compiler will convert from decimal to binary accurately enough
 * to produce the hexadecimal values shown.
 */

// #ifndef __FDLIBM_H__
// #include "fdlibm.h"
// #endif

#include <stdint.h>

typedef union
{
  double value;
  struct
  {
    uint32_t lsw;
    uint32_t msw;
  } parts;
} ieee_double_shape_type;

#if INT_MAX > 32767
#  define IC(x) ((int32_t) x)
#  define UC(x) ((uint32_t) x)
#else
#  define IC(x) ((int32_t) x##L)
#  define UC(x) ((uint32_t) x##UL)
#endif

#define GET_HIGH_WORD(i,d)					\
{								\
  const ieee_double_shape_type *gh_u = (const ieee_double_shape_type *)&(d);					\
  (i) = gh_u->parts.msw;						\
}
#define GET_LOW_WORD(i,d)					\
{								\
  const ieee_double_shape_type *gl_u = (const ieee_double_shape_type *)&(d);					\
  (i) = gl_u->parts.lsw;						\
}
#define SET_HIGH_WORD(d,v)                                      \
{                                                               \
  ieee_double_shape_type *sh_u = (ieee_double_shape_type *)&(d);\
  sh_u->parts.msw = (v);                                        \
}

/* NYI */
#define feraiseexcept(x)

#define FE_UNDERFLOW        0x0008
#define FE_OVERFLOW         0x0004

#if defined(__GNUC__)
#   define    HUGE_VAL     __builtin_huge_val()
#   define    HUGE_VALF    __builtin_huge_valf()
#   define    HUGE_VALL    __builtin_huge_vall()
#   define    NAN          __builtin_nanf("0x7fc00000")
#else
#   define    HUGE_VAL     1e500
#   define    HUGE_VALF    1e50f
#   define    HUGE_VALL    1e5000L
#   define    NAN          __nan()
#endif

#define IEEE754_DOUBLE_SHIFT 20

// #ifndef __have_fpu_exp

//double __ieee754_exp(double x)			/* default IEEE double exp */
double sun_exp(double x)
{
	double y, hi, lo, c, t;
	int32_t k, xsb;
	uint32_t hx;

	static const double one = 1.0;
	static const double halF[2] = { 0.5, -0.5 };

	static const double hugeval = 1.0e+300;
	static const double twom1000 = 9.33263618503218878990e-302;		/* 2**-1000=0x01700000,0 */
	static const double o_threshold = 7.09782712893383973096e+02;	/* 0x40862E42, 0xFEFA39EF */
	static const double u_threshold = -7.45133219101941108420e+02;	/* 0xc0874910, 0xD52D3051 */
	static const double ln2HI[2] = {
		6.93147180369123816490e-01,	/* 0x3fe62e42, 0xfee00000 */
		-6.93147180369123816490e-01	/* 0xbfe62e42, 0xfee00000 */
	};

	static const double ln2LO[2] = {
		1.90821492927058770002e-10,	/* 0x3dea39ef, 0x35793c76 */
		-1.90821492927058770002e-10	/* 0xbdea39ef, 0x35793c76 */
	};

	static const double invln2 = 1.44269504088896338700e+00;	/* 0x3ff71547, 0x652b82fe */
	static const double P1 = 1.66666666666666019037e-01;		/* 0x3FC55555, 0x5555553E */
	static const double P2 = -2.77777777770155933842e-03;		/* 0xBF66C16C, 0x16BEBD93 */
	static const double P3 = 6.61375632143793436117e-05;		/* 0x3F11566A, 0xAF25DE2C */
	static const double P4 = -1.65339022054652515390e-06;		/* 0xBEBBBD41, 0xC5D26BF1 */
	static const double P5 = 4.13813679705723846039e-08;		/* 0x3E663769, 0x72BEA4D0 */

	GET_HIGH_WORD(hx, x);				/* high word of x */
	xsb = (hx >> 31) & 1;				/* sign bit of x */
	hx &= IC(0x7fffffff);				/* high word of |x| */

	/* filter out non-finite argument */
	if (hx >= IC(0x40862E42))
	{									/* if |x|>=709.78... */
		if (hx >= IC(0x7ff00000))
		{
			GET_LOW_WORD(k, x);
			if (((hx & IC(0xfffff)) | k) != 0)
				return x;				/* NaN */
			return (xsb == 0) ? x : 0.0;	/* exp(+-inf)={inf,0} */
		}
		if (x > o_threshold)			/* overflow */
		{
			feraiseexcept(FE_OVERFLOW);
			return HUGE_VAL;
		}
		if (x < u_threshold)			/* underflow */
		{
			feraiseexcept(FE_UNDERFLOW);
			return 0;
		}
	}

	/* argument reduction */
	if (hx > IC(0x3fd62e42))
	{									/* if  |x| > 0.5 ln2 */
		if (hx < IC(0x3FF0A2B2))
		{								/* and |x| < 1.5 ln2 */
			hi = x - ln2HI[xsb];
			lo = ln2LO[xsb];
			k = 1 - xsb - xsb;
		} else
		{
			k = invln2 * x + halF[xsb];
			t = k;
			hi = x - t * ln2HI[0];		/* t*ln2HI is exact here */
			lo = t * ln2LO[0];
		}
		x = hi - lo;
	} else if (hx < IC(0x3e300000))
	{									/* when |x|<2**-28 */
		if (hugeval + x > one)
			return one + x;				/* trigger inexact */
		return one;
	} else
	{
		k = 0;
		lo = 0;
		hi = 0;
	}

	/* x is now in primary range */
	t = x * x;
	c = x - t * (P1 + t * (P2 + t * (P3 + t * (P4 + t * P5))));
	if (k == 0)
		return one - ((x * c) / (c - 2.0) - x);
	y = one - ((lo - (x * c) / (2.0 - c)) - hi);
	GET_HIGH_WORD(hx, y);
	if (k >= -1021)
	{
		hx += (k << IEEE754_DOUBLE_SHIFT);			/* add k to y's exponent */
		SET_HIGH_WORD(y, hx);
		return y;
	} else
	{
		hx += ((k + 1000) << IEEE754_DOUBLE_SHIFT);	/* add k to y's exponent */
		SET_HIGH_WORD(y, hx);
		return y * twom1000;
	}
}

// #endif

// /* wrapper exp */
// double __exp(double x)
// {
// 	double z = __ieee754_exp(x);

// 	if (_LIB_VERSION != _IEEE_ && (!isfinite(z) || z == 0.0) && isfinite(x))
// 		return __kernel_standard(x, x, z, signbit(x) ? KMATHERR_EXP_UNDERFLOW : KMATHERR_EXP_OVERFLOW);

// 	return z;
// }

// __typeof(__exp) exp __attribute__((weak, alias("__exp")));
// #ifdef __NO_LONG_DOUBLE_MATH
// long double __expl(long double x) __attribute__((alias("__exp")));
// __typeof(__expl) expl __attribute__((weak, alias("__exp")));
// #endif
