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

double my_core_function_asin_0(double in_5)
{
// (Horner (MinimaxPolynomial (asin x) [(- 1) 1]))
    double out_3 = (((double)in_5)*(((double)0x1.4874e667d7a1eb92a59a46327af653bap0) 
        + ((double)in_5)*(((double)0x1.bc3b5c77c4cd1f6a3f02dfe260e1cfp-16) 
        + ((double)in_5)*(((double)-0x1.003d5bd766d671d4a6a772663c5990e6p3) 
        + ((double)in_5)*(((double)-0x1.c7aa5af1735b26401e724c776b3ccb2ep-12) 
        + ((double)in_5)*(((double)0x1.0e22fd0a090801b5dd6c55c215aeabfcp6) 
        + ((double)in_5)*(((double)0x1.42b14265a50ec7e67ed15d806c6e0b88p-9) 
        + ((double)in_5)*(((double)-0x1.dd407317964b21cf8405f36edc8d344p7) 
        + ((double)in_5)*(((double)-0x1.af9d0dc481ac1f2b5f81ac3c6ad22112p-8) 
        + ((double)in_5)*(((double)0x1.9abb54827bc1d42ca5a14102200e070cp8) 
        + ((double)in_5)*(((double)0x1.296c24fbf6a2790a9fa573869ee21518p-7) 
        + ((double)in_5)*(((double)-0x1.53810a50849461f07c245cb8e652c1f4p8) 
        + ((double)in_5)*(((double)-0x1.98d75aa6111b23b84ec441a51dfb865cp-8) 
        + ((double)in_5)*(((double)0x1.b08d23463f2d4786652a4b911a0c5f8ep6) 
        + ((double)in_5)*((double)0x1.bc079e49c9af487f1ce9e7eea495897cp-10)))))))))))))));
    return out_3;
}

double my_core_function_asin_1(double in_7)
{
// (MirrorLeft (- x) (Horner (MinimaxPolynomial (asin x) [0 1])))
    double in_6 = in_7 < 0.0 ? (0.0 - in_7) : in_7;
    double out_4 = (((double)in_6)*(((double)-0x1.9d2073304db4ea5624936b370390f9cp0) 
        + ((double)in_6)*(((double)0x1.cfe3fcfe193511970147b8ca6d65b0bcp7) 
        + ((double)in_6)*(((double)-0x1.a9039c62858b9a5fedbfb9f70f0763aap12) 
        + ((double)in_6)*(((double)0x1.7fd7abca52c2b82551ce43583599e776p16) 
        + ((double)in_6)*(((double)-0x1.949e4a4c047a70a8cb00713c15fd722cp19) 
        + ((double)in_6)*(((double)0x1.106df328f3dd3e561fa4d8ac99b97244p22) 
        + ((double)in_6)*(((double)-0x1.edbc37cd13aa2f3d6d6e7b765ca2d572p23) 
        + ((double)in_6)*(((double)0x1.3605b12461c294f1f07ff179d30c5bd4p25) 
        + ((double)in_6)*(((double)-0x1.112dadcf8b77557049d567c8f66af77p26) 
        + ((double)in_6)*(((double)0x1.50d9269350fa196a6a30c23a1a095ebcp26) 
        + ((double)in_6)*(((double)-0x1.1ca1c28bde669b1a44e2807cbfee171ap26) 
        + ((double)in_6)*(((double)0x1.3a0ec57b2ff88a9091179a9231f9bfe4p25) 
        + ((double)in_6)*(((double)-0x1.9799736a00b898525076cc3b895ff564p23) 
        + ((double)in_6)*((double)0x1.d7e58cc89c66b57822abd16f7aefc6f8p20)))))))))))))));
    double recons_2 = in_7 < 0.0 ? (-out_4) : out_4;
    return recons_2;
}

double my_core_function_asin_2(double in_9)
{
// (MirrorRight (- x) (Horner (MinimaxPolynomial (asin x) [(- 1) 0])))
    double in_8 = in_9 < 0.0 ? in_9 : (0.0 - in_9);
    double out_5 = (((double)in_8)*(((double)-0x1.9d2075a9ba39a75b257d4eeb206f501p0) 
        + ((double)in_8)*(((double)-0x1.cfe403e7942b0af8b317d2459102265cp7) 
        + ((double)in_8)*(((double)-0x1.a903a41baeb06f5c27fd218d471e21cap12) 
        + ((double)in_8)*(((double)-0x1.7fd7b30e41fe08add7eb734c8386916ap16) 
        + ((double)in_8)*(((double)-0x1.949e51c06b2c5f36a85723840214eeap19) 
        + ((double)in_8)*(((double)-0x1.106df7e0e58792a0b2fb949dd8657dcp22) 
        + ((double)in_8)*(((double)-0x1.edbc3fb187ec3276b879739de1269f36p23) 
        + ((double)in_8)*(((double)-0x1.3605b5ac20c0e73b12f4cf40d3ae63dcp25) 
        + ((double)in_8)*(((double)-0x1.112db171663320101fe2bf52928c7708p26) 
        + ((double)in_8)*(((double)-0x1.50d92aa47a58ff775c1df7d51d915a46p26) 
        + ((double)in_8)*(((double)-0x1.1ca1c5aa1e36fea74b590243b45222e6p26) 
        + ((double)in_8)*(((double)-0x1.3a0ec89a0cfdf04c125e3b99bd45887cp25) 
        + ((double)in_8)*(((double)-0x1.97997715f5801f8f308fc616e1c99234p23) 
        + ((double)in_8)*((double)-0x1.d7e590a25f4e7e7d6a890fe6df9f53e2p20)))))))))))))));
    double recons_3 = in_9 < 0.0 ? out_5 : (-out_5);
    return recons_3;
}
