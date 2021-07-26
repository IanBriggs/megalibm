

#include "oracle_functions.h"
#include "table_generation.h"

#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>




double libm_versin(double x) {
  return 1.0 - cos(x);
}

double my_versin_16(double in_3)
{
  int sign_0 = signbit(((double)in_3));
  double in_2 = fabs(((double)in_3));
  int k_0 = (int) floor(((double)in_2)*((double)(1/M_PI)));
  double out_1 = ((double)in_2) - k_0*((double)M_PI);
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
  double out_0 = ((double)0x1.f34280f054cbap-34) +((double)in_0)*((double)in_0)*(((double)0x1.ffffffe69a5fcp-2) + ((double)in_0)*((double)in_0)*(((double)-0x1.555553a329323p-5) + ((double)in_0)*((double)in_0)*(((double)0x1.6c16953694176p-10) + ((double)in_0)*((double)in_0)*(((double)-0x1.a015945b651a5p-16) + ((double)in_0)*((double)in_0)*(((double)0x1.27a73528b7755p-22) + ((double)in_0)*((double)in_0)*(((double)-0x1.1b2d8d6fcd352p-29) + ((double)in_0)*((double)in_0)*((double)0x1.561ca21503f52p-37)))))));
  return out_0;
}

double my_versin_18(double in_3)
{
  int sign_0 = signbit(((double)in_3));
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
  double out_0 = ((double)0x1.05a6b27c7455bp-40) +((double)in_0)*((double)in_0)*(((double)0x1.ffffffffbcb29p-2) + ((double)in_0)*((double)in_0)*(((double)-0x1.5555554fa2251p-5) + ((double)in_0)*((double)in_0)*(((double)0x1.6c16c0adb4f69p-10) + ((double)in_0)*((double)in_0)*(((double)-0x1.a019e8b915813p-16) + ((double)in_0)*((double)in_0)*(((double)0x1.27e3267d62f47p-22) + ((double)in_0)*((double)in_0)*(((double)-0x1.1ec4ef9a41fadp-29) + ((double)in_0)*((double)in_0)*(((double)0x1.8f787d9d12946p-37) + ((double)in_0)*((double)in_0)*((double)-0x1.74230d0b77d93p-45))))))));
  return out_0;
}

double my_versin_20(double in_3)
{
  int sign_0 = signbit(((double)in_3));
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
  double out_0 = ((double)0x1.b87126c572758p-48) +((double)in_0)*((double)in_0)*(((double)0x1.ffffffffff744p-2) + ((double)in_0)*((double)in_0)*(((double)-0x1.5555555546b2fp-5) + ((double)in_0)*((double)in_0)*(((double)0x1.6c16c169b5f03p-10) + ((double)in_0)*((double)in_0)*(((double)-0x1.a01a013b941e2p-16) + ((double)in_0)*((double)in_0)*(((double)0x1.27e4f1ed7a862p-22) + ((double)in_0)*((double)in_0)*(((double)-0x1.1eec748624d13p-29) + ((double)in_0)*((double)in_0)*(((double)0x1.936ec3c83067dp-37) + ((double)in_0)*((double)in_0)*(((double)-0x1.aaf80b8d8be83p-45) + ((double)in_0)*((double)in_0)*((double)0x1.3c2b7da7aac37p-53)))))))));
  return out_0;
}


double my_versin_22(double in_3)
{
  int sign_0 = signbit(((double)in_3));
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
  double out_0 = ((double)0x1.4003df3b14eecp-55) +((double)in_0)*((double)in_0)*(((double)0x1.ffffffffffff1p-2) + ((double)in_0)*((double)in_0)*(((double)-0x1.5555555555373p-5) + ((double)in_0)*((double)in_0)*(((double)0x1.6c16c16c10d25p-10) + ((double)in_0)*((double)in_0)*(((double)-0x1.a01a019ee69e3p-16) + ((double)in_0)*((double)in_0)*(((double)0x1.27e4fb5333cadp-22) + ((double)in_0)*((double)in_0)*(((double)-0x1.1eed89a2d9645p-29) + ((double)in_0)*((double)in_0)*(((double)0x1.939646000f081p-37) + ((double)in_0)*((double)in_0)*(((double)-0x1.ae5f68b9d44aep-45) + ((double)in_0)*((double)in_0)*(((double)0x1.65bac67a33825p-53) + ((double)in_0)*((double)in_0)*((double)-0x1.af4f8e258be9fp-62))))))))));
  return out_0;
}

double my_versin_24(double in_3)
{
  int sign_0 = signbit(((double)in_3));
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
  double out_0 = ((double)-0x1.c5c43822986bbp-63) +((double)in_0)*((double)in_0)*(((double)0x1p-1) + ((double)in_0)*((double)in_0)*(((double)-0x1.5555555555554p-5) + ((double)in_0)*((double)in_0)*(((double)0x1.6c16c16c16bap-10) + ((double)in_0)*((double)in_0)*(((double)-0x1.a01a01a017ddep-16) + ((double)in_0)*((double)in_0)*(((double)0x1.27e4fb77336d8p-22) + ((double)in_0)*((double)in_0)*(((double)-0x1.1eed8eeecacb1p-29) + ((double)in_0)*((double)in_0)*(((double)0x1.93974658f699ap-37) + ((double)in_0)*((double)in_0)*(((double)-0x1.ae7e8c86aac7p-45) + ((double)in_0)*((double)in_0)*(((double)0x1.68142d1e3e146p-53) + ((double)in_0)*((double)in_0)*(((double)-0x1.e2986fc7f56f4p-62) + ((double)in_0)*((double)in_0)*((double)0x1.e380a92d64e31p-71)))))))))));
  return out_0;
}

double my_versin_26(double in_3)
{
  int sign_0 = signbit(((double)in_3));
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
  double out_0 = ((double)-0x1.12157f9d2768cp-64) +((double)in_0)*((double)in_0)*(((double)0x1p-1) + ((double)in_0)*((double)in_0)*(((double)-0x1.5555555555555p-5) + ((double)in_0)*((double)in_0)*(((double)0x1.6c16c16c16bfbp-10) + ((double)in_0)*((double)in_0)*(((double)-0x1.a01a01a019886p-16) + ((double)in_0)*((double)in_0)*(((double)0x1.27e4fb77779fap-22) + ((double)in_0)*((double)in_0)*(((double)-0x1.1eed8efc1f0f4p-29) + ((double)in_0)*((double)in_0)*(((double)0x1.939749b5813e3p-37) + ((double)in_0)*((double)in_0)*(((double)-0x1.ae7f1b8673aa7p-45) + ((double)in_0)*((double)in_0)*(((double)0x1.6823bec218891p-53) + ((double)in_0)*((double)in_0)*(((double)-0x1.e4bbbcae3581p-62) + ((double)in_0)*((double)in_0)*(((double)0x1.07405032619b2p-70) + ((double)in_0)*((double)in_0)*((double)-0x1.7940672ced682p-80))))))))))));
  return out_0;
}




#define ENTRY_COUNT (2)

entry ENTRIES[ENTRY_COUNT] = \
  {
    {libm_versin, "libm_versin"},
    /* {my_versin_16, "my_versin_16"}, */
    /* {my_versin_18, "my_versin_18"}, */
    /* {my_versin_20, "my_versin_20"}, */
    /* {my_versin_22, "my_versin_22"}, */
    /* {my_versin_24, "my_versin_24"}, */
    {my_versin_26, "my_versin_26"},
  };




int main(int argc, char** argv)
{
  long int choice = 0;
  if (argc == 2) {
    choice = strtol(argv[1], NULL, 10);
  }

  double low, high, step;
  switch (choice) {
  case 0:
    low = -M_PI/8;
    high = M_PI/8;
    step = 0.0000015;
    break;

  case 1:
    low = -M_PI/4;
    high = M_PI/4;
    step = 0.000003;
    break;

  case 2:
    low = -M_PI/2;
    high = M_PI/2;
    step = 0.000006;
    break;

  case 3:
    low = -M_PI;
    high = M_PI;
    step = 0.00001;
    break;

  case 4:
    low = -20*M_PI;
    high = 20*M_PI;
    step = 0.0002;
    break;

  case 5:
    low = -200*M_PI;
    high = 200*M_PI;
    step = 0.002;
    break;

  default:
    exit(1);
  }

  generate_table(low, high, step, versin_oracle, "versin", ENTRY_COUNT, ENTRIES);
}
