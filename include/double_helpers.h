#ifndef DOUBLE_HELPERS_H
#define DOUBLE_HELPERS_H

#include "double_access.h"

static inline double
helper_abs(double x)
{
    return set_sign_double(x, 0);
}

#endif // #ifndef DOUBLE_HELPERS_H