#ifndef CODY_WAITE_REDUCE_H
#define CODY_WAITE_REDUCE_H

#include "double_helpers.h"

static inline double
fast_cody_waite_reduce(double x,
                       const double inv_C,
                       const size_t C_len,
                       const double *C,
                       int *ptr_k)
{
    *ptr_k = (int)(x * inv_C + 0.5) - ((int)get_sign_double(x));
    const double dk = (double)(*ptr_k);
    double r = x;
    for (size_t i = 0; i < C_len; i++)
    {
        r -= dk * C[i];
    }
    return r;
}

static inline double
cody_waite_reduce(double x,
                  const double inv_period,
                  int period_c,
                  double *period,
                  int *pn,
                  double *perror)
{
    double xn = (int)(x * inv_period + 0.5) - ((int)get_sign_double(x));
    double error = 0;
    double retval;
    if (xn == 0.0)
    {
        retval = x;
    }
    else
    {
        int k;
        double sum = x - xn * period[0];
        double period_hi = period[0];
        double period_lo = 0.0;
        error = 0.0;

        for (k = 1; k < period_c; ++k)
        {
            double t, new_sum;

            t = -xn * period[k];
            new_sum = sum + t;
            error += sum - new_sum;
            error += t;
            sum = new_sum;
            period_lo += period[k];
        }

        double retval_hi = sum;
        double retval_lo = error;

        double period_half = 0.5 * (period_hi + period_lo);
        retval = retval_hi + retval_lo;
        error = retval_hi - retval;
        error += retval_lo;

        if (retval < -period_half)
        {
            xn--;
            retval += period_hi;
            retval += period_lo;
            if (retval > period_half)
            {
                retval = period_half;
            }
        }
        else if (period_half < retval)
        {
            xn++;
            retval -= period_hi;
            retval -= period_lo;
            if (retval < -period_half)
            {
                retval = -period_half;
            }
        }
    }

    if (perror != NULL)
    {
        *perror = error;
    }

    if (pn != NULL)
    {
        *pn = (int)xn;
    }

    return retval;
}

#endif // #ifndef CODY_WAITE_REDUCE_H