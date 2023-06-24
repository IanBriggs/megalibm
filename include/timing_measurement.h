#include <assert.h>
#include <math.h>
#include <mpfr.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>



typedef double (*unop_fp64)(double);
typedef int (*unop_mpfr_fp64)(mpfr_t, double);

#define MULT_ROUNDING_FACTOR 1e9



static void
init_random_double()
{
    srand(42);
}

static double
random_double()
{
    return ((double)rand()) / ((double)RAND_MAX);
}

static void
time_function_fp64(unop_fp64 func,
                    double low,
                    double high,
                    size_t samples,
                    size_t iters)
{
    assert(isfinite(low));
    assert(isfinite(high));
    assert(low < high);
    assert(samples > 0);

    double span = high - low;
    init_random_double();

    clock_t start, end;
    double cpu_time_used, avg_time_per_sample;

    start = clock();

    for (size_t iter = 0; iter < iters; iter++)
    {
        for (size_t i = 0; i < samples; i++)
        {
            double sample = low + span * random_double();
            double value = func(sample);
            
        }
    }
    end = clock();
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    avg_time_per_sample = (double)((cpu_time_used / (iters * samples)) * MULT_ROUNDING_FACTOR);
    printf("%a", avg_time_per_sample);
}