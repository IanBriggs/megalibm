

#include "table_generation.h"
#include "versin.h"

#include <assert.h>
#include <math.h>




int oracle_versin(mpfr_t out, double dx) {
  static int init_called = 0;
  static mpfr_t x;
  
  if (!init_called) {
    mpfr_init2(x, ORACLE_PREC);
    init_called = 1;
  }

  mpfr_set_d(x, dx, MPFR_RNDN);                          // x = dx
  mpfr_cos(x, x, MPFR_RNDN);                             // x = cos(x)
  mpfr_ui_sub(out, (unsigned long int) 1, x, MPFR_RNDN); // x = 1 - x
  return 0; // todo: catch errors
}


double libm_versin(double x) {
  return 1.0 - cos(x);
}


double my_versin_26(double in_3)
{
  double in_2 = fabs(((double)in_3));
  int k_1 = (int) floor(((double)in_2)*((double)(1/(2*M_PI))));
  double in_1 = ((double)in_2) - k_1*((double)(2*M_PI));
  int k_0 = (int) floor(((double)in_1)*((double)(1/M_PI)));
  double out_1 = ((double)in_1) - k_0*((double)M_PI);
  double in_0;
  switch (k_0%2) {
  case 0:
    in_0 = out_1;
    break;
  case 1:
    in_0 = M_PI-out_1;
    break;
  default:
    assert(0);
    return NAN;
  }
  double out_0 = (((double)in_0)*((double)in_0)*(((double)0x1p-1)
        + ((double)in_0)*((double)in_0)*(((double)-0x1.5555555555555p-5)
        + ((double)in_0)*((double)in_0)*(((double)0x1.6c16c16c16bf1p-10)
        + ((double)in_0)*((double)in_0)*(((double)-0x1.a01a01a019361p-16)
        + ((double)in_0)*((double)in_0)*(((double)0x1.27e4fb77660a4p-22)
        + ((double)in_0)*((double)in_0)*(((double)-0x1.1eed8ef7fea05p-29)
        + ((double)in_0)*((double)in_0)*(((double)0x1.93974886de927p-37)
        + ((double)in_0)*((double)in_0)*(((double)-0x1.ae7ee4445fdf5p-45)
        + ((double)in_0)*((double)in_0)*(((double)0x1.681d46c704a91p-53)
        + ((double)in_0)*((double)in_0)*(((double)-0x1.e3cae15a6a0edp-62)
        + ((double)in_0)*((double)in_0)*(((double)0x1.faaccb5ca913ep-71)
        + ((double)in_0)*((double)in_0)*((double)-0x1.88ea73637facbp-81)))))))))))));
  return out_0;
}
