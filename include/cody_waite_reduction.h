#ifndef CODY_WAITE_REDUCE_H
#define CODY_WAITE_REDUCE_H

#include "double_helpers.h"

#include <math.h>


static inline double
fast_cody_waite_reduce(double x,
                       const double inv_C,
                       const size_t C_len,
                       const double *C,
                       int *ptr_k,
                       double *ptr_error)
{
    const double shifted = inv_C * x + 0.5;
    const double dk = ((int)shifted) - ((int)signbit(shifted));
    const int ik = (int) dk;
    *ptr_k = ik;
    double r = x;
    for (size_t i = 0; i < C_len; i++)
    {
        r -= ik * C[i];
    }
    return r;
}

// Based on the extended Cody-Waite style reduction by in Nelson Beebe in
// "The Mathematical-Function Computation Handbook"

static inline double
cody_waite_reduce(double x,
                  const double inv_C,
                  const size_t C_len,
                  const double *C,
                  int *ptr_k,
                  double *ptr_error)
{
    double shifted = inv_C * x + 0.5;
    double dk = ((int)shifted) - ((int)signbit(shifted));
    double error = 0;
    double retval;
    if (dk == 0.0)
    {
        retval = x;
    }
    else
    {
        int k;
        double sum = x - dk * C[0];
        double period_hi = C[0];
        double period_lo = 0.0;
        error = 0.0;

        for (k = 1; k < C_len; ++k)
        {
            double t, new_sum;

            t = -dk * C[k];
            new_sum = sum + t;
            error += sum - new_sum;
            error += t;
            sum = new_sum;
            period_lo += C[k];
        }

        double retval_hi = sum;
        double retval_lo = error;

        double period_half = 0.5 * (period_hi + period_lo);
        retval = retval_hi + retval_lo;
        error = retval_hi - retval;
        error += retval_lo;

        if (retval < -period_half)
        {
            dk--;
            retval += period_hi;
            retval += period_lo;
            if (retval > period_half)
            {
                retval = period_half;
            }
        }
        else if (period_half < retval)
        {
            dk++;
            retval -= period_hi;
            retval -= period_lo;
            if (retval < -period_half)
            {
                retval = -period_half;
            }
        }
    }

    if (ptr_error != NULL)
    {
        *ptr_error = error;
    }

    if (ptr_k != NULL)
    {
        *ptr_k = (int)dk;
    }

    return retval;
}

#endif // #ifndef CODY_WAITE_REDUCE_H
