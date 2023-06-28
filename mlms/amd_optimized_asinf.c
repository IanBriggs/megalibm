/*
 * Heavily modified source from AMD's AOCL math library.
 * Modifications were made to allow the file to be compiled on its own.
 * In addition the kernel call to sqrt was replaced with a system level sqrt
 */

/*
 * Copyright (C) 2008-2022 Advanced Micro Devices, Inc. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 * 3. Neither the name of the copyright holder nor the names of its contributors
 *    may be used to endorse or promote products derived from this software without
 *    specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 * INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
 * OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 */

/*
 * ISO-IEC-10967-2: Elementary Numerical Functions
 * Signature:
 *   float asinf(float x)
 *

 * Contains implementation of float asinf(float x)
 *
 * The input domain should be in the [-1, +1] else a domain error is displayed
 *
 * asin(-x) = -asin(x)
 * asin(x) = pi/2-2*asin(sqrt(1/2*(1-x)))  when x > 1/2
 *
 * y = abs(x)
 * asinf(y) = asinf(g)  when y <= 0.5,  where g = y*y
 *		    = pi/2-asinf(g)  when y > 0.5, where g = 1/2*(1-y), y = -2*sqrt(g)
 * The term asin(f) is approximated by using a polynomial where the inputs lie in the interval [0 1/2]
 */

#include <math.h>
#include <stdint.h>
// #include <libm_util_amd.h>
#define	AMD_F_NONE		  0x0
#define AMD_F_OVERFLOW 0x00000008
#define AMD_F_UNDERFLOW 0x00000010
#define AMD_F_DIVBYZERO 0x00000004
#define AMD_F_INVALID 0x00000001
#define AMD_F_INEXACT 0x00000020
// #include <libm/alm_special.h>
// #include <libm_macros.h>
// #include <libm/types.h>
typedef    float               f32_t;
typedef union {
    f32_t    f;
    int32_t  i;
    uint32_t u;
} flt32_t;
// #include <libm/typehelper.h>
// #include <libm/amd_funcs_internal.h>
// #include <libm/compiler.h>
// #include <libm/poly.h>
/*
 * poly = C0 + C1*r + C2*r^2 + C3*r^3 + C4 *r^4 + C5*r^5 + C6*r^6 + C7*r^7 + C8*r^8
 *
 *      = (C0 + C1*r) + r2(C2 + C3*r) + r4((C4+ C5*r) + r2(C6 + C7*r)) + C8*r^8
 *
 *      = ((C6+C7*x)*x2 + (C4+C5*x))*x4 +
 *                      (C8+C9*x)*x8) +
 *                      ((C2+C3*x)*x2 + (C0+C1*x));
 */
#define POLY_EVAL_9_0(r, c0, c1, c2, c3, c4, c5, c6, c7, c8) ({ \
                        __typeof(r) a1, a2, a3, a4, b1, q;      \
                         __typeof(r) r2, r4;                    \
                        a1 = c1*r + c0;                         \
                        a2 = c3*r + c2;                         \
                        r2 = r * r;                             \
                        a3 = c5*r + c4;                         \
                        r4 = r2 * r2;                           \
                        a4 = c7*r + c6 +c8*r2;                  \
                                                                \
                        b1 = (a4*r2 + a3)*r4 + a2*r2;           \
                        q = b1 +a1;                             \
                         q;                                     \
                 })
// #include <libm/alm_special.h>
enum {
        ALM_E_IN_X_NEG  = 1<<8,         /* is a ZERO */
        ALM_E_IN_X_NAN  = 1<<7,         /* first arg is a NaN or QNaN */
        ALM_E_IN_X_INF  = 1<<6,         /* is '+/- INF' */
        ALM_E_IN_X_ZERO = 1<<5,         /* is a ZERO */
        ALM_E_DIV_BY_ZER0 = 1 << 2,

        /* For functions with 2 args */
        ALM_E_IN_Y_NAN  = 1<<4,         /*  */
        ALM_E_IN_Y_INF  = 1<<3,
        ALM_E_IN_Y_ZERO = 1<<2,
        ALM_E_IN_Y_NEG  = 1<<0,         /* is a ZERO */


        ALM_E_OUT_NAN  = 1<<16,
        ALM_E_OUT_INF  = 1<<17,
        ALM_E_OUT_ZERO = 1<<18,

        ALM_E_OVERFLOW = 1<<19,        /*overflow flag*/

};
#define QNAN_MASK_32        0x00400000
#define INDEFBITPATT_SP32 0xffc00000
#define PUT_BITS_SP32(ux, x) \
  { \
    volatile union {float f; unsigned int i;} _bitsy; \
    _bitsy.i = (unsigned int)(ux); \
     x = _bitsy.f; \
  }
static inline void __amd_raise_fp_exc(int flags)
{
    if ((flags & AMD_F_UNDERFLOW) == AMD_F_UNDERFLOW) {
        volatile double a = 0x1.0p-1022;
        // __asm __volatile("mulsd %1, %0":"+x"(a):"x"(a));
    }
    if ((flags & AMD_F_OVERFLOW) == AMD_F_OVERFLOW) {
        volatile double a = 0x1.fffffffffffffp1023;
        // __asm __volatile("mulsd %1, %0":"+x"(a):"x"(a));
    }
    if ((flags & AMD_F_DIVBYZERO) == AMD_F_DIVBYZERO) {
        volatile double a = 1.0, b = 0.0;
        // __asm __volatile("divsd %1, %0":"+x"(a):"x"(b));
    }
    if ((flags & AMD_F_INVALID) == AMD_F_INVALID) {
        volatile double a = 0.0;
        // __asm __volatile("divsd %1, %0":"+x"(a):"x"(a));
    }
}
float __alm_handle_errorf(uint64_t value, int flags)
{
    float z;

    PUT_BITS_SP32(value, z);
    __amd_raise_fp_exc(flags);
    return z;
}
float
alm_asinf_special(float x, uint32_t code)
{
    flt32_t fl = {.f = x};
    if (code == ALM_E_IN_X_NAN)
    {
        /* Return invalid if it's a NaN */
        if (fl.u & QNAN_MASK_32)
            return __alm_handle_errorf(fl.u|0x00400000,
                                       AMD_F_NONE);
        else
            return  __alm_handle_errorf(fl.u|0x00400000,
                                        AMD_F_INVALID
                                        );
    }
    else
        return  __alm_handle_errorf(INDEFBITPATT_SP32,
                                    AMD_F_INVALID);
}
// #include "kern/sqrt_pos.c"

static struct {
    double THEEPS, HALF ;
    double A[2], B[2], poly_asinf[12];
} asinf_data = {
    .THEEPS = 0x1.6a09e667f3bcdp-27,
    .HALF = 0x1p-1,
    // Values of factors of pi required to calculate asin
    .A = {
        0,
        0x1.921fb54442d18p0,
    },
    .B = {
        0x1.921fb54442d18p0,
        0x1.921fb54442d18p-1,
    },
    // Polynomial coefficients obtained using fpminimax algorithm from Sollya
    .poly_asinf = {
        0x1.55555555552aap-3,
        0x1.333333337cbaep-4,
        0x1.6db6db3c0984p-5,
        0x1.f1c72dd86cbafp-6,
        0x1.6e89d3ff33aa4p-6,
        0x1.1c6d83ae664b6p-6,
        0x1.c6e1568b90518p-7,
        0x1.8f6a58977fe49p-7,
        0x1.a6ab10b3321bp-8,
        0x1.43305ebb2428fp-6,
        -0x1.0e874ec5e3157p-6,
        0x1.06eec35b3b142p-5,
    },
};
#define HALF asinf_data.HALF

#define A asinf_data.A
#define B asinf_data.B

#define C1 asinf_data.poly_asinf[0]
#define C2 asinf_data.poly_asinf[1]
#define C3 asinf_data.poly_asinf[2]
#define C4 asinf_data.poly_asinf[3]
#define C5 asinf_data.poly_asinf[4]
#define C6 asinf_data.poly_asinf[5]
#define C7 asinf_data.poly_asinf[6]
#define C8 asinf_data.poly_asinf[7]
#define C9 asinf_data.poly_asinf[8]
#define C10 asinf_data.poly_asinf[9]
#define C11 asinf_data.poly_asinf[10]
#define C12 asinf_data.poly_asinf[12]


//float
// ALM_PROTO_OPT(asinf)
float
amd_optimized_asinf(float x)
{
    double Y, G, poly, result, sign =1;
    int32_t n = 0;

    // Include check for inf, -inf, nan here
    //  asin(NaN) = NaN

    if (x < 0)
        sign = -1;
    Y = ((double)(x))*sign;			// Make x positive, if it is negative

    if(Y>1.0)
            return alm_asinf_special(x, ALM_E_OUT_NAN);

    if (Y > HALF)
    {
        n = 1;
        G = HALF*(1.0-Y);
        // Y = -2.0*ALM_PROTO_KERN(sqrt)(G);
        Y = -2.0*sqrt(G);

        poly = Y + Y*G *POLY_EVAL_9_0(G,C1,C2,C3,C4,C5,C6,C7,C8,C9);

        result =  (A[n]+poly);

        return (float)(sign*result);
    }
    G = Y*Y;
    result = Y + Y*G *POLY_EVAL_9_0(G,C1,C2,C3,C4,C5,C6,C7,C8,C9);

    return (float)(sign*result);
}
