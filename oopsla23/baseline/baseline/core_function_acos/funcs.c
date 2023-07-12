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

double my_core_function_acos_1(double in_2)
{
// (MirrorLeft (- PI x) (Horner (MinimaxPolynomial (acos x) [0 1])))
    double in_1 = in_2 < 0.0 ? (0.0 - in_2) : in_2;
    double out_1 = (((double)0x1.8e813ba61dc1e6f5d89660aedd9d3b5ep0) 
        +((double)in_1)*(((double)0x1.251da10dfcedcf4882061eaeba7ce678p2) 
        + ((double)in_1)*(((double)-0x1.6d336fef8b186f3e9a69ad73861b208ap8) 
        + ((double)in_1)*(((double)0x1.262c9fa9da49bf891984d7817bfe63ep13) 
        + ((double)in_1)*(((double)-0x1.ee921c617e0fb5408630a395500cbe22p16) 
        + ((double)in_1)*(((double)0x1.f1fe41defba268f51b7b2b0e9801ff36p19) 
        + ((double)in_1)*(((double)-0x1.44cc6cb0c9d576e7eeedc49dca0ddff2p22) 
        + ((double)in_1)*(((double)0x1.1f84aa0ea64468cdcb840c2141ab24b8p24) 
        + ((double)in_1)*(((double)-0x1.62a85d5586dc64018c11d1cfda78f70cp25) 
        + ((double)in_1)*(((double)0x1.341c2e394070f78679335d924c21ee74p26) 
        + ((double)in_1)*(((double)-0x1.77943cb7a7781eac23faa48769251558p26) 
        + ((double)in_1)*(((double)0x1.3a5ad4eabb697f99a2fbca1eab525114p26) 
        + ((double)in_1)*(((double)-0x1.5816e2591d98402602c7e9da5bfe5704p25) 
        + ((double)in_1)*(((double)0x1.bb89cb5293fe022c17aefa7fd2ed2be4p23) 
        + ((double)in_1)*((double)-0x1.fe7cd523b5f2748f27f90a15f8f4dd9p20)))))))))))))));
    double recons_0 = in_2 < 0.0 ? (M_PI-out_1) : out_1;
    return recons_0;
}

double my_core_function_acos_2(double in_4)
{
// (MirrorRight (- PI x) (Horner (MinimaxPolynomial (acos x) [(- 1) 0])))
    double in_3 = in_4 < 0.0 ? in_4 : (0.0 - in_4);
    double out_2 = (((double)0x1.95be2ee2e45e86741380bafcd84c789p0) 
        +((double)in_3)*(((double)0x1.251da13c3c54f364465f925c7d56d7a2p2) 
        + ((double)in_3)*(((double)0x1.6d33701d0fe8b5e168918ab1229fc94p8) 
        + ((double)in_3)*(((double)0x1.262c9fcc6fd9ea753b263f81e008d42ap13) 
        + ((double)in_3)*(((double)0x1.ee921c96cedeeee0fd8faa35ccfd11a8p16) 
        + ((double)in_3)*(((double)0x1.f1fe420e91b38483ebeeabea473c69dep19) 
        + ((double)in_3)*(((double)0x1.44cc6ccb2868cb07602f9f6cab9e441ap22) 
        + ((double)in_3)*(((double)0x1.1f84aa215e4866056337766dd12b9b86p24) 
        + ((double)in_3)*(((double)0x1.62a85d667505cc85976778dc0f5c7ffcp25) 
        + ((double)in_3)*(((double)0x1.341c2e425838b8ba909ecbfd62ca3f2ap26) 
        + ((double)in_3)*(((double)0x1.77943cbbb951b312af08ac2824821324p26) 
        + ((double)in_3)*(((double)0x1.3a5ad4e83dc09a46cb9028b9f847af2p26) 
        + ((double)in_3)*(((double)0x1.5816e2500383d5f4c8429af6862a4e1ap25) 
        + ((double)in_3)*(((double)0x1.bb89cb3ed81def132087140a0ffd8484p23) 
        + ((double)in_3)*((double)0x1.fe7cd50423f060df329daaa028f1f1a2p20)))))))))))))));
    double recons_1 = in_4 < 0.0 ? out_2 : (M_PI-out_2);
    return recons_1;
}
