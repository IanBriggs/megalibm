

#include "oracle_functions.h"




#define PREC (500)


void init_oracle(mpfr_t* xp)
{
  mpfr_init2(*xp, PREC);
}


void clear_oracle(mpfr_t* xp)
{
  mpfr_clear(*xp);
}


void compare_oracle(double actual_fp, mpfr_t* expected_p,
                    double* absdiff_fp_p, double* reldiff_fp_p)
{
  mpfr_t actual, difference;
  mpfr_inits2(PREC, actual, difference, (mpfr_ptr) NULL);
  mpfr_set_d(actual, actual_fp, MPFR_RNDN);
  mpfr_sub(difference, *expected_p, actual, MPFR_RNDN);
  *absdiff_fp_p = mpfr_get_d(difference, MPFR_RNDN);
  mpfr_div(difference, difference, *expected_p, MPFR_RNDN);
  *reldiff_fp_p = mpfr_get_d(difference, MPFR_RNDN);
  mpfr_clear(actual);
}


void versin_oracle(double x, mpfr_t* frxp)
{
  mpfr_set_d(*frxp, x, MPFR_RNDN);
  mpfr_cos(*frxp, *frxp, MPFR_RNDN);
  mpfr_ui_sub(*frxp, (unsigned long int) 1, *frxp, MPFR_RNDN);
}

void sin_oracle(double x, mpfr_t* frxp)
{
  mpfr_set_d(*frxp, x, MPFR_RNDN);
  mpfr_sin(*frxp, *frxp, MPFR_RNDN);
}


void cos_oracle(double x, mpfr_t* frxp)
{
  mpfr_set_d(*frxp, x, MPFR_RNDN);
  mpfr_cos(*frxp, *frxp, MPFR_RNDN);
}


void tan_oracle(double x, mpfr_t* frxp)
{
  mpfr_set_d(*frxp, x, MPFR_RNDN);
  mpfr_tan(*frxp, *frxp, MPFR_RNDN);
}


void exp_oracle(double x, mpfr_t* frxp)
{
  mpfr_set_d(*frxp, x, MPFR_RNDN);
  mpfr_exp(*frxp, *frxp, MPFR_RNDN);
}


void log_oracle(double x, mpfr_t* frxp)
{
  mpfr_set_d(*frxp, x, MPFR_RNDN);
  mpfr_log(*frxp, *frxp, MPFR_RNDN);
}


void asin_oracle(double x, mpfr_t* frxp)
{
  mpfr_set_d(*frxp, x, MPFR_RNDN);
  mpfr_asin(*frxp, *frxp, MPFR_RNDN);
}


void acos_oracle(double x, mpfr_t* frxp)
{
  mpfr_set_d(*frxp, x, MPFR_RNDN);
  mpfr_acos(*frxp, *frxp, MPFR_RNDN);
}


void atan_oracle(double x, mpfr_t* frxp)
{
  mpfr_set_d(*frxp, x, MPFR_RNDN);
  mpfr_atan(*frxp, *frxp, MPFR_RNDN);
}

