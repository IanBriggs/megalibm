#ifndef ORACLE_FUNCTIONS
#define ORACLE_FUNCTIONS


#include <mpfr.h>


typedef void(*oracle_func)(double, mpfr_t*);

void init_oracle(mpfr_t* xp);
void clear_oracle(mpfr_t* xp);
void compare_oracle(double actual_fp, mpfr_t* expected_p,
                    double* absdiff_fp_p, double* reldiff_fp_p);

void versin_oracle(double x, mpfr_t* frxp);
void sin_oracle(double x, mpfr_t* frxp);
void cos_oracle(double x, mpfr_t* frxp);
void tan_oracle(double x, mpfr_t* frxp);
void exp_oracle(double x, mpfr_t* frxp);
void log_oracle(double x, mpfr_t* frxp);
void asin_oracle(double x, mpfr_t* frxp);
void acos_oracle(double x, mpfr_t* frxp);
void atan_oracle(double x, mpfr_t* frxp);


#endif
