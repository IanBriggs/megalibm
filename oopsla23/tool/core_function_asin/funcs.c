#include "funcs.h"
#include "table_generation.h"
#include <assert.h>
#include <math.h>

double libm_core_function_asin(double x)
{
    return asin(x);
}

int mpfr_core_function_asin(mpfr_t out, double dx)
{
  static int init_called = 0;
  static mpfr_t x;
  if (!init_called) {
    mpfr_init2(x, ORACLE_PREC);
    init_called = 1;
  }
  mpfr_set_d(x, dx, MPFR_RNDN);
  mpfr_asin(out, x, MPFR_RNDN);
  return 0;
}

double my_core_function_asin_0(double in_1)
{
// (Horner (MinimaxPolynomial (asin x) [(- 1) 1]))
    double out_1 = (((double)in_1)*(((double)0x1.4874e667d7a1eb92a59a46327af653bap0) 
        + ((double)in_1)*(((double)0x1.bc3b5c77c4cd1f6a3f02dfe260e1cfp-16) 
        + ((double)in_1)*(((double)-0x1.003d5bd766d671d4a6a772663c5990e6p3) 
        + ((double)in_1)*(((double)-0x1.c7aa5af1735b26401e724c776b3ccb2ep-12) 
        + ((double)in_1)*(((double)0x1.0e22fd0a090801b5dd6c55c215aeabfcp6) 
        + ((double)in_1)*(((double)0x1.42b14265a50ec7e67ed15d806c6e0b88p-9) 
        + ((double)in_1)*(((double)-0x1.dd407317964b21cf8405f36edc8d344p7) 
        + ((double)in_1)*(((double)-0x1.af9d0dc481ac1f2b5f81ac3c6ad22112p-8) 
        + ((double)in_1)*(((double)0x1.9abb54827bc1d42ca5a14102200e070cp8) 
        + ((double)in_1)*(((double)0x1.296c24fbf6a2790a9fa573869ee21518p-7) 
        + ((double)in_1)*(((double)-0x1.53810a50849461f07c245cb8e652c1f4p8) 
        + ((double)in_1)*(((double)-0x1.98d75aa6111b23b84ec441a51dfb865cp-8) 
        + ((double)in_1)*(((double)0x1.b08d23463f2d4786652a4b911a0c5f8ep6) 
        + ((double)in_1)*((double)0x1.bc079e49c9af487f1ce9e7eea495897cp-10)))))))))))))));
    return out_1;
}
