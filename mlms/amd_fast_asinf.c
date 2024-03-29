/*
 * Heavily modified source from AMD's AOCL math library.
 * Modifications were made to allow the file to be compiled on its own.
 * In addition the kernel call to sqrt was replaced with a system level sqrt
 */

/*
 * Copyright (C) 2021 Advanced Micro Devices, Inc. All rights reserved.
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
 * The term asin(f) is approximated by using a polynomial where the inputs lie in the
 * interval [0 1/2]
 */

#include <math.h>
#include <stdint.h>
// #include <libm_util_amd.h>
#define NEG_QNAN_F32 0xfff00000
// #include <libm/alm_special.h>
// #include <libm_macros.h>
// #include <libm/typehelper.h>
typedef    float               f32_t;
typedef union {
    f32_t    f;
    int32_t  i;
    uint32_t u;
} flt32_t;
static inline float
asfloat(uint32_t i)
{
	flt32_t fl = {.u = i};
	return fl.f;
}
// #include <libm/amd_funcs_internal.h>
// #include <libm/compiler.h>
// #include <libm/poly.h>
/*
 * poly = C1 + C2*r + C3*r^2 + C4*r^3 + C5 *r^4
 *      = (C1 + C2*r) + r^2(C3 + C4*r) + r^4*C5
 */
#define POLY_EVAL_5(r, c0, c1, c2, c3, c4) ({   \
            __typeof(r) t1, t2, r2, q;          \
            t1 = c0 + c1*r;                     \
            t2 = c2 + c3*r;                     \
            r2 = r * r;                         \
            q = t1 + r2 * t2;                   \
            q = q + r2 * r2 * c4;               \
            q;                                  \
        })

// #include <libm/alm_special.h>
// #include "kern/sqrtf_pos.c"

static struct {
    float  half ;
    float a[2], b[2], poly_asinf[5];
} asinf_data = {
    .half = 0x1p-1,
    // Values of factors of pi required to calculate asin
    .a = {
        0,
        0x1.921fb6p0,
    },
    .b = {
        0x1.921fb6p0,
        0x1.921fb6p-1,
    },
    // Polynomial coefficients obtained using fpminimax algorithm from Sollya
    .poly_asinf = {
        0x1.5555fcp-3,
        0x1.32f8d8p-4,
        0x1.7525aap-5,
        0x1.86e46ap-6,
        0x1.5d456cp-5,
    },
};

#define HALF asinf_data.half

#define A asinf_data.a
#define B asinf_data.b

#define C1 asinf_data.poly_asinf[0]
#define C2 asinf_data.poly_asinf[1]
#define C3 asinf_data.poly_asinf[2]
#define C4 asinf_data.poly_asinf[3]
#define C5 asinf_data.poly_asinf[4]

// float
// ALM_PROTO_FAST(asinf)
float
amd_fast_asinf(float x)
{
    float Y, G, poly, result, sign =1;
    int32_t n = 0;

    // Include check for inf, -inf, nan here
    //  asin(NaN) = NaN

    if (x < 0)
        sign = -1;
    Y = x*sign;			// Make x positive, if it is negative

    if(Y>1.0f)
        return asfloat(NEG_QNAN_F32);

    if (Y > HALF) {
        n = 1;
        G = HALF*(1.0f-Y);
        // Y = -2.0f*ALM_PROTO_KERN(sqrtf)(G);
        Y = -2.0f*sqrtf(G);

        poly = Y + Y*G *POLY_EVAL_5(G,C1,C2,C3,C4,C5);

        result =  (A[n]+poly);

        return sign*result;
    }

    G = Y*Y;

    result= Y + Y*G *POLY_EVAL_5(G,C1,C2,C3,C4,C5);

    return sign*result;
}

// strong_alias (__asinf_finite, ALM_PROTO_FAST(asinf))
// weak_alias (amd_asinf, ALM_PROTO_FAST(asinf))
// weak_alias (asinf, ALM_PROTO_FAST(asinf))
