#include "funcs.h"
#include "table_generation.h"
#include <assert.h>
#include <math.h>

double libm_core_function_acos(double x)
{
    return acos(x);
}

int mpfr_core_function_acos(mpfr_t out, double dx)
{
  static int init_called = 0;
  static mpfr_t x;
  if (!init_called) {
    mpfr_init2(x, ORACLE_PREC);
    init_called = 1;
  }
  mpfr_set_d(x, dx, MPFR_RNDN);
  mpfr_acos(out, x, MPFR_RNDN);
  return 0;
}

double my_core_function_acos_0(double in_0)
{
// (Horner (MinimaxPolynomial (acos x) [(- 1) 1]))
    double out_0 = (((double)0x1.921fb544433f622b31725f9e537f30c6p0) 
        +((double)in_0)*(((double)-0x1.487520be119ac484ff8b12b06f791dfap0) 
        + ((double)in_0)*(((double)-0x1.251f35918c70a6db6dacc422f3c4028p-39) 
        + ((double)in_0)*(((double)0x1.003dd65f8a2ad9f619465975f7f3bcf4p3) 
        + ((double)in_0)*(((double)-0x1.7aa188abd15c31cbe5a309d1e9c3c7d6p-33) 
        + ((double)in_0)*(((double)-0x1.0e2353ef8e112d1931dbe25013e37b9ep6) 
        + ((double)in_0)*(((double)0x1.abb1f367208d5f8e8016d0c398d50b0ep-30) 
        + ((double)in_0)*(((double)0x1.dd40e7ddc309c59a10b91800ff49c0ccp7) 
        + ((double)in_0)*(((double)-0x1.627ab2d53e6946af094d2ce87d1f8338p-28) 
        + ((double)in_0)*(((double)-0x1.9abba5a874f384af8376518d56bc1dp8) 
        + ((double)in_0)*(((double)0x1.15b44b03a0d77270a6660f3aef96e9a6p-27) 
        + ((double)in_0)*(((double)0x1.538142a6001ad877ffb59652f991abd2p8) 
        + ((double)in_0)*(((double)-0x1.9fda65c1ed39828d7ef62295ea19bc7cp-28) 
        + ((double)in_0)*(((double)-0x1.b08d6110d3e532e85ff883c354cd3d38p6) 
        + ((double)in_0)*((double)0x1.dfcb6018603a89c983bf6db35d9d4d42p-30)))))))))))))));
    return out_0;
}
