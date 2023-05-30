/*
 * Heavily modified source from the VDT math library
 * Modifications were made to allow the file to be compiled on its own.
 */

/*
 * exp.h
 * The basic idea is to exploit Pade polynomials.
 * A lot of ideas were inspired by the cephes math library (by Stephen L. Moshier
 * moshier@na-net.ornl.gov) as well as actual code.
 * The Cephes library can be found here:  http://www.netlib.org/cephes/
 *
 *  Created on: Jun 23, 2012
 *      Author: Danilo Piparo, Thomas Hauth, Vincenzo Innocente
 */

/*
 * VDT is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser Public License for more details.
 *
 * You should have received a copy of the GNU Lesser Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
#include <stdint.h>
#include <math.h>

// #include "vdtcore_common.h"
/// Used to switch between different type of interpretations of the data (64 bits)
typedef union {
  double d;
  float f[2];
  uint32_t i[2];
  uint64_t ll;
  uint16_t s[4];
} ieee754;
//------------------------------------------------------------------------------
/// Converts a float to an int
inline uint32_t sp2uint32(float x) {
    ieee754 tmp;
    tmp.f[0]=x;
    return tmp.i[0];
  }
//------------------------------------------------------------------------------
/**
 * A vectorisable floor implementation, not only triggered by fast-math.
 * These functions do not distinguish between -0.0 and 0.0, so are not IEC6509
 * compliant for argument -0.0
 **/
inline double fpfloor(const double x)
{
    // no problem since exp is defined between -708 and 708. Int is enough for it!
    int32_t ret = (int32_t) x;
    ret -= (sp2uint32((float)x) >> 31);
    return ret;
}
/// Converts an unsigned long long to a double
inline double uint642dp(uint64_t ll)
{
    ieee754 tmp;
    tmp.ll = ll;
    return tmp.d;
}
// #include <limits>

const double EXP_LIMIT = 708;

const double PX1exp = 1.26177193074810590878E-4;
const double PX2exp = 3.02994407707441961300E-2;
const double PX3exp = 9.99999999999999999910E-1;
const double QX1exp = 3.00198505138664455042E-6;
const double QX2exp = 2.52448340349684104192E-3;
const double QX3exp = 2.27265548208155028766E-1;
const double QX4exp = 2.00000000000000000009E0;

const double LOG2E = 1.4426950408889634073599; // 1/log(2)

const float MAXLOGF = 88.72283905206835f;
const float MINLOGF = -88.f;

const float C1F = 0.693359375f;
const float C2F = -2.12194440e-4f;

const float PX1expf = 1.9875691500E-4f;
const float PX2expf = 1.3981999507E-3f;
const float PX3expf = 8.3334519073E-3f;
const float PX4expf = 4.1665795894E-2f;
const float PX5expf = 1.6666665459E-1f;
const float PX6expf = 5.0000001201E-1f;

const float LOG2EF = 1.44269504088896341f;

// }

// Exp double precision --------------------------------------------------------

/// Exponential Function double precision
double vdt_exp(double initial_x)
{

    double x = initial_x;
    double px = fpfloor(LOG2E * x + 0.5);

    const int32_t n = (int32_t)px;

    x -= px * 6.93145751953125E-1;
    x -= px * 1.42860682030941723212E-6;

    const double xx = x * x;

    // px = x * P(x**2).
    px = PX1exp;
    px *= xx;
    px += PX2exp;
    px *= xx;
    px += PX3exp;
    px *= x;

    // Evaluate Q(x**2).
    double qx = QX1exp;
    qx *= xx;
    qx += QX2exp;
    qx *= xx;
    qx += QX3exp;
    qx *= xx;
    qx += QX4exp;

    // e**x = 1 + 2x P(x**2)/( Q(x**2) - P(x**2) )
    x = px / (qx - px);
    x = 1.0 + 2.0 * x;

    // Build 2^n in double.
    x *= uint642dp((((uint64_t)n) + 1023) << 52);

    if (initial_x > EXP_LIMIT)
        x = INFINITY;
    if (initial_x < -EXP_LIMIT)
        x = 0.;

    return x;
}