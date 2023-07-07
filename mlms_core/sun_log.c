/*
 * Modified source from Sun's math library as updated by freemint
 * Modifications were made to allow the file to be compiled on its own.
 * The function has been renamed to sun_log.
 */

/* @(#)e_log.c 1.3 95/01/18 */
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

/* __ieee754_log(x)
 * Return the logrithm of x
 *
 * Method :
 *   1. Argument Reduction: find k and f such that
 *			x = 2^k * (1+f),
 *	   where  sqrt(2)/2 < 1+f < sqrt(2) .
 *
 *   2. Approximation of log(1+f).
 *	Let s = f/(2+f) ; based on log(1+f) = log(1+s) - log(1-s)
 *		 = 2s + 2/3 s**3 + 2/5 s**5 + .....,
 *	     	 = 2s + s*R
 *      We use a special Reme algorithm on [0,0.1716] to generate
 * 	a polynomial of degree 14 to approximate R The maximum error
 *	of this polynomial approximation is bounded by 2**-58.45. In
 *	other words,
 *    		        2      4      6      8      10      12      14
 *	    R(z) ~ Lg1*s +Lg2*s +Lg3*s +Lg4*s +Lg5*s  +Lg6*s  +Lg7*s
 *  	(the values of Lg1 to Lg7 are listed in the program)
 *	and
 *	    |      2          14          |     -58.45
 *	    | Lg1*s +...+Lg7*s    -  R(z) | <= 2
 *	    |                             |
 *	Note that 2s = f - s*f = f - hfsq + s*hfsq, where hfsq = f*f/2.
 *	In order to guarantee error in log below 1ulp, we compute log
 *	by
 *		log(1+f) = f - s*(f - R)	(if f is not too large)
 *		log(1+f) = f - (hfsq - s*(hfsq+R)).	(better accuracy)
 *
 *	3. Finally,  log(x) = k*ln2 + log(1+f).
 *			    = k*ln2_hi+(f-(hfsq-(s*(hfsq+R)+k*ln2_lo)))
 *	   Here ln2 is split into two floating point number:
 *			ln2_hi + ln2_lo,
 *	   where n*ln2_hi is always exact for |n| < 2000.
 *
 * Special cases:
 *	log(x) is NaN with signal if x < 0 (including -INF) ;
 *	log(+INF) is +INF; log(0) is -INF with signal;
 *	log(NaN) is that NaN with no signal.
 *
 * Accuracy:
 *	according to an error analysis, the error is always less than
 *	1 ulp (unit in the last place).
 *
 * Constants:
 * The hexadecimal values are the intended ones for the following
 * constants. The decimal values may be used, provided that the
 * compiler will convert from decimal to binary accurately enough
 * to produce the hexadecimal values shown.
 */

#include <stdio.h>

#include <stdint.h>

// #ifndef __FDLIBM_H__
// #include "fdlibm.h"
// #endif

#define IC(x) ((int32_t) x)
#define UC(x) ((uint32_t) x)

typedef union
{
  double value;
  struct
  {
    uint32_t lsw;
    uint32_t msw;
  } parts;
} ieee_double_shape_type;

/* Get two 32 bit ints from a double.  */
#define GET_DOUBLE_WORDS(ix0,ix1,d)				\
{								\
  const ieee_double_shape_type *ew_u = (const ieee_double_shape_type *)&(d);					\
  (ix0) = (typeof(ix0)) ew_u->parts.msw;					\
  (ix1) = (typeof(ix1)) ew_u->parts.lsw;					\
}
/* Set the more significant 32 bits of a double from an int.  */
#define SET_HIGH_WORD(d,v)                                      \
{                                                               \
  ieee_double_shape_type *sh_u = (ieee_double_shape_type *)&(d);\
  sh_u->parts.msw = (uint32_t) (v);                                        \
}
/* Get the more significant 32 bit int from a double.  */
#define GET_HIGH_WORD(i,d)					\
{								\
  const ieee_double_shape_type *gh_u = (const ieee_double_shape_type *)&(d);					\
  (i) = (typeof(i)) gh_u->parts.msw;						\
}

// #ifndef __have_fpu_log

// double __ieee754_log(double x)
double sun_log(double x)
{
	double hfsq, f, s, z, R, w, t1, t2, dk;
	int32_t k, hx, i, j;
	uint32_t lx;

	static const double ln2_hi = 6.93147180369123816490e-01;	/* 3fe62e42 fee00000 */
	static const double ln2_lo = 1.90821492927058770002e-10;	/* 3dea39ef 35793c76 */
	static const double two54 = 1.80143985094819840000e+16;	/* 43500000 00000000 */
	static const double Lg1 = 6.666666666666735130e-01;		/* 3FE55555 55555593 */
	static const double Lg2 = 3.999999999940941908e-01;		/* 3FD99999 9997FA04 */
	static const double Lg3 = 2.857142874366239149e-01;		/* 3FD24924 94229359 */
	static const double Lg4 = 2.222219843214978396e-01;		/* 3FCC71C5 1D8E78AF */
	static const double Lg5 = 1.818357216161805012e-01;		/* 3FC74664 96CB03DE */
	static const double Lg6 = 1.531383769920937332e-01;		/* 3FC39A09 D078C69F */
	static const double Lg7 = 1.479819860511658591e-01;		/* 3FC2F112 DF3E5244 */

	static const double zero = 0.0;

	GET_DOUBLE_WORDS(hx, lx, x);

	k = 0; // IB: k tracks the reduction constant
	if (hx < IC(0x00100000)) // IB: if x is denormal or zero
	{									/* x < 2**-1022  */
		if (((hx & IC(0x7fffffff)) | lx) == 0) // IB: check that all but the sign but is zero
			return -two54 / zero;		/* log(+-0)=-inf */
		if (hx < 0)
			return (x - x) / zero;		/* log(-#) = NaN */
		// IB: move k down to bring x out of denormals
        k -= 54;
		x *= two54;						/* subnormal number, scale up x */
		GET_HIGH_WORD(hx, x);
	}

	if (hx >= IC(0x7ff00000)) // IB: if x is inf or Nan
		return x + x;
    // IB: x is now positive, finite, and normal
	k += (hx >> 20) - 1023; // IB: add exponent to k
	hx &= IC(0x000fffff); // IB: keep upper part of mantissa
    // IB: ??? i is zero if the add doesn't carry the 19th bit and 0x100000 if it does
    /* Pavel says
    if (x > sqrt(2)) {
        x = x/2;
    }
    */
	i = (hx + IC(0x95f64)) & IC(0x100000); // Pavel claims it sqrt(2)
    // IB: ??? if i is zero x is on [0.5, 1.0] if i is nonzero x is on [1.0, 2.0]
	SET_HIGH_WORD(x, hx | (i ^ IC(0x3ff00000)));	/* normalize x or x/2 */
	k += (i >> 20); // IB: account for this division by 2
	f = x - 1.0;
	if ((IC(0x000fffff) & (2 + hx)) < 3) // IB: if bits 33-51 are all set or none are set
	{									/* |f| < 2**-20 */ // IB: not sure about this bound...
		if (f == zero)
		{
			if (k == 0)
				return zero;
			dk = (double) k;
			return dk * ln2_hi + dk * ln2_lo;
		}
        // IB: Tiny polynomial in f
        // x = 2^k * (1+f)
        // log(1+f) \approx f - (f^2)/2 + f/3 = R
        //                  note: taylor log(1+x) at point 0.0
        // log(x) \approx k*log(2) + f - R
		R = f * f * (0.5 - 0.33333333333333333 * f);
		if (k == 0)
			return f - R;
		dk = (double) k;
		return dk * ln2_hi - ((R - dk * ln2_lo) - f);
	}
	s = f / (2.0 + f);
	dk = (double) k;
	z = s * s;
	i = hx - IC(0x6147a); // IB: ???
	w = z * z;
	j = IC(0x6b851) - hx; // IB: ???
    // IB: split the polynomial into odd and even then add
	t1 = w * (Lg2 + w * (Lg4 + w * Lg6));
	t2 = z * (Lg1 + w * (Lg3 + w * (Lg5 + w * Lg7)));
	i |= j;
	R = t2 + t1;
	if (i > 0)
	{
		hfsq = 0.5 * f * f;
		if (k == 0)
			return f - (hfsq - s * (hfsq + R));
		return dk * ln2_hi - ((hfsq - (s * (hfsq + R) + dk * ln2_lo)) - f);
	}
	if (k == 0)
		return f - s * (f - R);
	return dk * ln2_hi - ((s * (f - R) - dk * ln2_lo) - f);
}

// #endif


// /* wrapper log(x) */
// double __log(double x)
// {
// 	if (_LIB_VERSION != _IEEE_ && islessequal(x, 0.0))
// 	{
// 		if (x == 0.0)
// 		{
// 			feraiseexcept(FE_DIVBYZERO);
// 			return __kernel_standard(x, x, -HUGE_VAL, KMATHERR_LOG_ZERO);	/* log(0) */
// 		} else
// 		{
// 			feraiseexcept(FE_INVALID);
// 			return __kernel_standard(x, x, __builtin_nan(""), KMATHERR_LOG_MINUS);	/* log(x<0) */
// 		}
// 	}

// 	return __ieee754_log(x);
// }

// __typeof(__log) log __attribute__((weak, alias("__log")));
// #ifdef __NO_LONG_DOUBLE_MATH
// __typeof(__logl) __logl __attribute__((alias("__log")));
// __typeof(__logl) logl __attribute__((weak, alias("__log")));
// #endif
