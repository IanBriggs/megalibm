
#include <assert.h>
#include <math.h>
#include <mpfr.h>
#include <stdio.h>
#include <stdlib.h>

static mpfr_prec_t ORACLE_PREC = 106 + 10;

typedef double (*unop_fp64)(double);
typedef int (*unop_mpfr_fp64)(mpfr_t, double);

static void
init_random_double()
{
    srand(42);
}

static double
random_double()
{
    // TODO: this is a _really_ bad fp rng
    return ((double)rand()) / ((double)RAND_MAX);
}

static void
generate_oracle_values_fp64(unop_mpfr_fp64 oracle,
                            double low,
                            double high,
                            size_t samples)
{
    assert(isfinite(low));
    assert(isfinite(high));
    assert(low < high);
    assert(samples > 0);

    double span = high - low;
    mpfr_t y_R;
    mpfr_t err_R;

    mpfr_init2(y_R, ORACLE_PREC);
    mpfr_init2(err_R, ORACLE_PREC);

    printf("input\tcorrectly_rounded\tdiff\n");
    init_random_double();
    for (size_t i = 0; i < samples; i++)
    {
        double x = low + span * random_double();

        // Run oracle
        oracle(y_R, x);

        // Closest double
        double y = mpfr_get_d(y_R, MPFR_RNDN);

        // Error from real to double
        mpfr_sub_d(err_R, y_R, y, MPFR_RNDN);
        double err = mpfr_get_d(err_R, MPFR_RNDN);

        printf("%a\t%a\t%a\n", x, y, err);
    }
}

static void
generate_function_values_fp64(unop_fp64 func,
                            double low,
                            double high,
                            size_t samples)
{
    assert(isfinite(low));
    assert(isfinite(high));
    assert(low < high);
    assert(samples > 0);

    double span = high - low;

    printf("input\tfunction\n");
    init_random_double();
    for (size_t i = 0; i < samples; i++)
    {
        double x = low + span * random_double();
        double y = func(x);
        printf("%a\t%a\n", x, y);
    }
}


typedef float (*unop_fp32)(float);
typedef int (*unop_mpfr_fp32)(mpfr_t, float);

static void
generate_oracle_values_fp32(unop_mpfr_fp32 oracle,
                            float low,
                            float high,
                            size_t samples)
{
    assert(isfinite(low));
    assert(isfinite(high));
    assert(low < high);
    assert(samples > 0);

    float span = high - low;
    mpfr_t y_R;
    mpfr_t err_R;

    mpfr_init2(y_R, ORACLE_PREC);
    mpfr_init2(err_R, ORACLE_PREC);

    printf("input\tcorrectly_rounded\tdiff\n");
    init_random_double();
    for (size_t i = 0; i < samples; i++)
    {
        float x = low + span * ((float) random_double());

        // Run oracle
        oracle(y_R, x);

        // Closest float
        float y = mpfr_get_flt(y_R, MPFR_RNDN);

        // Error from real to float
        mpfr_sub_d(err_R, y_R, y, MPFR_RNDN);
        float err = mpfr_get_flt(err_R, MPFR_RNDN);

        printf("%a\t%a\t%a\n", x, y, err);
    }
}

static void
generate_function_values_fp32(unop_fp32 func,
                            float low,
                            float high,
                            size_t samples)
{
    assert(isfinite(low));
    assert(isfinite(high));
    assert(low < high);
    assert(samples > 0);

    float span = high - low;

    printf("input\tfunction\n");
    init_random_double();
    for (size_t i = 0; i < samples; i++)
    {
        float x = low + span * ((float) random_double());
        float y = func(x);
        printf("%a\t%a\n", x, y);
    }
}