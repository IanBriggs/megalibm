#include "funcs.h"
#include "table_generation.h"
#include <assert.h>
#include <math.h>

double libm_core_function_tan(double x)
{
    return tan(x);
}

int mpfr_core_function_tan(mpfr_t out, double dx)
{
  static int init_called = 0;
  static mpfr_t x;
  if (!init_called) {
    mpfr_init2(x, ORACLE_PREC);
    init_called = 1;
  }
  mpfr_set_d(x, dx, MPFR_RNDN);
  mpfr_tan(out, x, MPFR_RNDN);
  return 0;
}

double my_core_function_tan_0(double in_83)
{
// (periodic PI (Horner (MinimaxPolynomial (tan x) [0.0 PI])))
    int k_28 = (int) floor((((double)in_83)-((double)0.0))*((double)0.3183098861837907));
    double in_82 = ((double)in_83) - k_28*((double)3.141592653589793);
    double out_30 = (((double)in_82)*(((double)-0x1.8531570957eca098c40b0111f75abd62p14) 
        + ((double)in_82)*(((double)0x1.16ebd173f70889e86dcf71a849ab0e06p19) 
        + ((double)in_82)*(((double)-0x1.17626c5029c9fe3ba6c2ad01163ed2a2p22) 
        + ((double)in_82)*(((double)0x1.19a635c622e80f9b77fb49b8723e4c8ap24) 
        + ((double)in_82)*(((double)-0x1.4e7cdb464ef174b547e01849dcb52526p25) 
        + ((double)in_82)*(((double)0x1.fd8c250cfe62446d0871e9983fb44694p25) 
        + ((double)in_82)*(((double)-0x1.0584eac3c394bb8e492a4fa1aa5d9be4p26) 
        + ((double)in_82)*(((double)0x1.73d5d91700f75018aefcff04d161bc88p25) 
        + ((double)in_82)*(((double)-0x1.723ea46b928d164cb03f60760a3ebd9cp24) 
        + ((double)in_82)*(((double)0x1.0120883d57756edf1f57cd2e6fde9008p23) 
        + ((double)in_82)*(((double)-0x1.e74a2e081fc8414d126aaa1d0d9b02e8p20) 
        + ((double)in_82)*(((double)0x1.2bb24c3c16457120cd111744fbc2cdf2p18) 
        + ((double)in_82)*(((double)-0x1.ae53dd2396bb34cff536eabf2a6c4d3ap14) 
        + ((double)in_82)*((double)0x1.10ea8d4a5cee56611394dde1651c5a68p10)))))))))))))));
    return out_30;
}

double my_core_function_tan_1(double in_85)
{
// (periodic PI (Horner (MinimaxPolynomial (tan x) [(/ (- PI) 2) (/ PI 2)])))
    int k_29 = (int) floor((((double)in_85)-((double)-1.5707963267948966))*((double)0.3183098861837907));
    double in_84 = ((double)in_85) - k_29*((double)3.141592653589793);
    double out_31 = (((double)in_84)*(((double)-0x1.5eeae539da8c09ea6f1c0d5d8c0afc1p126) 
        + ((double)in_84)*(((double)-0x1.b574f82a013c956f6e9f46101b7b9aaap130) 
        + ((double)in_84)*(((double)0x1.4e73322a15458a7810bebdbfb0c14f92p130) 
        + ((double)in_84)*(((double)0x1.a233900ca3a949d87d2144975f35fc56p133) 
        + ((double)in_84)*(((double)-0x1.3f3212b991ff3abb962336d9da2aaad6p132) 
        + ((double)in_84)*(((double)-0x1.0a9df9ae8fd59dcf219c3cb30062cd98p135) 
        + ((double)in_84)*(((double)0x1.f278818010c8f7cbcd4c06d243932642p132) 
        + ((double)in_84)*(((double)0x1.38f2048f4baae3439acb1ac746b78596p135) 
        + ((double)in_84)*(((double)-0x1.71330331c2435dcdeb1311f06103bdd2p132) 
        + ((double)in_84)*(((double)-0x1.73cbae626a47f292a941b6a111d47b3ep134) 
        + ((double)in_84)*(((double)0x1.026898e19d5b7888ad7e55163dec79e2p131) 
        + ((double)in_84)*(((double)0x1.b2fc0a97e3fff2a3dfb338cd333781cp132) 
        + ((double)in_84)*(((double)-0x1.13267ffbc7fc481b3ef81f34a2a5ceecp128) 
        + ((double)in_84)*((double)-0x1.8e55db93724017c9e5e0452be46d0472p129)))))))))))))));
    return out_31;
}

double my_core_function_tan_2(double in_87)
{
// (periodic (- (* PI (- 2))) (Horner (MinimaxPolynomial (tan x) [0.0 (+ PI PI)])))
    int k_30 = (int) floor((((double)in_87)-((double)0.0))*((double)0.15915494309189535));
    double in_86 = ((double)in_87) - k_30*((double)6.283185307179586);
    double out_32 = (((double)in_86)*(((double)-0x1.9fb18f1908e39d1a6881d38498970e6cp12) 
        + ((double)in_86)*(((double)0x1.163f282128ec1d4bad37ac191624af54p16) 
        + ((double)in_86)*(((double)-0x1.0390b05a1cbdaa33c1663839f9f115dap18) 
        + ((double)in_86)*(((double)0x1.e509c293d9cbfd4a06ac9382643d05fep18) 
        + ((double)in_86)*(((double)-0x1.08fa837566305cd6b29d2d739a52ec3ap19) 
        + ((double)in_86)*(((double)0x1.6f6c62e16db216ed3ff61bd5063c39fp18) 
        + ((double)in_86)*(((double)-0x1.5207eded0d2b46a5d00bd9b96273cc1ep17) 
        + ((double)in_86)*(((double)0x1.a50b6cf4311a2dec5a5170db21c89966p15) 
        + ((double)in_86)*(((double)-0x1.6289239a4b15b3516ed18e10857c5872p13) 
        + ((double)in_86)*(((double)0x1.88934ab195318efa9ec3921b6aca79ap10) 
        + ((double)in_86)*(((double)-0x1.08d6736ea5eba6dc99b02347227e2fb2p7) 
        + ((double)in_86)*(((double)0x1.5af35e02db281964acaedf83479f0afp2) 
        + ((double)in_86)*(((double)0x1.24f4f7c4e3d9d44f12c50dbc06e8a582p-7) 
        + ((double)in_86)*((double)-0x1.98175b83b4f08c823f66b1c15ff0336ap-8)))))))))))))));
    return out_32;
}

double my_core_function_tan_3(double in_89)
{
// (periodic (- (* PI (- 2))) (Horner (MinimaxPolynomial (tan x) [(/ (* PI (- 2)) 2) (/ (+ PI PI) 2)])))
    int k_31 = (int) floor((((double)in_89)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_88 = ((double)in_89) - k_31*((double)6.283185307179586);
    double out_33 = (((double)in_88)*(((double)-0x1.8e011d99c2129c10c74470ef8d0b9a7p11) 
        + ((double)in_88)*(((double)-0x1.00359aa09a973a94cd83122ea55501bp12) 
        + ((double)in_88)*(((double)0x1.459fd8e7ba359093a2d81a2f8b28b4dap13) 
        + ((double)in_88)*(((double)0x1.bbb343cc3e70d554e5d6c1d8b05792b6p12) 
        + ((double)in_88)*(((double)-0x1.19676b95cfcf4ac6909d6e5fd9ded44cp13) 
        + ((double)in_88)*(((double)-0x1.058078d7ec4954293c16a5d22185e0c6p12) 
        + ((double)in_88)*(((double)0x1.963fbc3850ae06e48d55aebb685eb7f2p11) 
        + ((double)in_88)*(((double)0x1.1f8d2bc64e6e284f2a94e1043a2ef1d8p10) 
        + ((double)in_88)*(((double)-0x1.19a651fa3e00fdb9c0a76e7eee1be0ecp9) 
        + ((double)in_88)*(((double)-0x1.432652855c1c4c056c1c62f1764d1c86p7) 
        + ((double)in_88)*(((double)0x1.74581e84851bedef1bafe713c2aa161ep5) 
        + ((double)in_88)*(((double)0x1.6849aa0d51978d134e652b5bc6d0a7e6p3) 
        + ((double)in_88)*(((double)-0x1.79029812f4ab4b805073964795c75c86p0) 
        + ((double)in_88)*((double)-0x1.3c472802f4604ca6b5216f3395a1758ep-2)))))))))))))));
    return out_33;
}

double my_core_function_tan_4(double in_92)
{
// (periodic PI (MirrorLeft (- x) (Horner (MinimaxPolynomial (tan x) [0 (/ PI 2)]))))
    int k_32 = (int) floor((((double)in_92)-((double)-1.5707963267948966))*((double)0.3183098861837907));
    double in_91 = ((double)in_92) - k_32*((double)3.141592653589793);
    double in_90 = in_91 < 0.0 ? (0.0 - in_91) : in_91;
    double out_34 = (((double)in_90)*(((double)0x1.697aff02e0da589f82d5d245c8ffeb9p133) 
        + ((double)in_90)*(((double)-0x1.1c322cdf50294b9abab08f1959d4ecf4p139) 
        + ((double)in_90)*(((double)0x1.38794f870c4955b54778eac55f806e7cp143) 
        + ((double)in_90)*(((double)-0x1.5a1abf42b78113a6c314ee913d61eccp146) 
        + ((double)in_90)*(((double)0x1.c43b2b501a620df8ef0707863cf65472p148) 
        + ((double)in_90)*(((double)-0x1.7bac1e825c4df53de46d5c1b2d18c66ep150) 
        + ((double)in_90)*(((double)0x1.ae91fe829712ba82c6f146e0e9594922p151) 
        + ((double)in_90)*(((double)-0x1.5329d46f3bb7d56b5bd7767bc0c0f4c8p152) 
        + ((double)in_90)*(((double)0x1.7788432edfd7523537016c59b0ae1cd8p152) 
        + ((double)in_90)*(((double)-0x1.2346b530e64805c1eb8e22b6f89b70fp152) 
        + ((double)in_90)*(((double)0x1.35e8c29eef8ccc70fa9c972f62f85p151) 
        + ((double)in_90)*(((double)-0x1.aeda1becb0bfb7d2b0918d2f7c9d4444p149) 
        + ((double)in_90)*(((double)0x1.6075fdeede8f4d43d3ea3d52be01c26p147) 
        + ((double)in_90)*((double)-0x1.014f22c70590e888f660cd8be306384ep144)))))))))))))));
    double recons_24 = in_91 < 0.0 ? (-out_34) : out_34;
    return recons_24;
}

double my_core_function_tan_5(double in_95)
{
// (periodic PI (MirrorRight (- x) (Horner (MinimaxPolynomial (tan x) [(/ (- PI) 2) 0]))))
    int k_33 = (int) floor((((double)in_95)-((double)-1.5707963267948966))*((double)0.3183098861837907));
    double in_94 = ((double)in_95) - k_33*((double)3.141592653589793);
    double in_93 = in_94 < 0.0 ? in_94 : (0.0 - in_94);
    double out_35 = (((double)in_93)*(((double)0x1.e5a29dcf968e6f3594f26dfe8ee0de92p132) 
        + ((double)in_93)*(((double)0x1.7ea795ec6eaeb8bdfcd834af870240cap138) 
        + ((double)in_93)*(((double)0x1.a5a9f31c24233620dd9a6d59a1432102p142) 
        + ((double)in_93)*(((double)0x1.d41570f3ec17cffbf01de4abcbf86942p145) 
        + ((double)in_93)*(((double)0x1.327c62d033f667a3be85002c173b232ap148) 
        + ((double)in_93)*(((double)0x1.01e209e5d9b829401b9ee093c8a48dbep150) 
        + ((double)in_93)*(((double)0x1.251a918fc3aa61d4fef8f686b2ba62f4p151) 
        + ((double)in_93)*(((double)0x1.cec92934e054f436db7217b0bea05914p151) 
        + ((double)in_93)*(((double)0x1.00c648edeed2b4ec42aff361a5f00c54p152) 
        + ((double)in_93)*(((double)0x1.8f363907d02e81ea382215432c32c68ap151) 
        + ((double)in_93)*(((double)0x1.a9b16a730d787d5f564eaad5a2ef3af8p150) 
        + ((double)in_93)*(((double)0x1.28915359cca7007a1d410fa54e86d4d2p149) 
        + ((double)in_93)*(((double)0x1.e64babb8aee3418838b8149fe56d5368p146) 
        + ((double)in_93)*((double)0x1.63cd4781c11d55c852196f8c3b95f0c2p143)))))))))))))));
    double recons_25 = in_94 < 0.0 ? out_35 : (-out_35);
    return recons_25;
}

double my_core_function_tan_6(double in_98)
{
// (periodic (- (* PI (- 2))) (MirrorLeft (- x) (Horner (MinimaxPolynomial (tan x) [0 (/ (+ PI PI) 2)]))))
    int k_34 = (int) floor((((double)in_98)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_97 = ((double)in_98) - k_34*((double)6.283185307179586);
    double in_96 = in_97 < 0.0 ? (0.0 - in_97) : in_97;
    double out_36 = (((double)in_96)*(((double)-0x1.8531570957eca098c40b0111f75abd62p14) 
        + ((double)in_96)*(((double)0x1.16ebd173f70889e86dcf71a849ab0e06p19) 
        + ((double)in_96)*(((double)-0x1.17626c5029c9fe3ba6c2ad01163ed2a2p22) 
        + ((double)in_96)*(((double)0x1.19a635c622e80f9b77fb49b8723e4c8ap24) 
        + ((double)in_96)*(((double)-0x1.4e7cdb464ef174b547e01849dcb52526p25) 
        + ((double)in_96)*(((double)0x1.fd8c250cfe62446d0871e9983fb44694p25) 
        + ((double)in_96)*(((double)-0x1.0584eac3c394bb8e492a4fa1aa5d9be4p26) 
        + ((double)in_96)*(((double)0x1.73d5d91700f75018aefcff04d161bc88p25) 
        + ((double)in_96)*(((double)-0x1.723ea46b928d164cb03f60760a3ebd9cp24) 
        + ((double)in_96)*(((double)0x1.0120883d57756edf1f57cd2e6fde9008p23) 
        + ((double)in_96)*(((double)-0x1.e74a2e081fc8414d126aaa1d0d9b02e8p20) 
        + ((double)in_96)*(((double)0x1.2bb24c3c16457120cd111744fbc2cdf2p18) 
        + ((double)in_96)*(((double)-0x1.ae53dd2396bb34cff536eabf2a6c4d3ap14) 
        + ((double)in_96)*((double)0x1.10ea8d4a5cee56611394dde1651c5a68p10)))))))))))))));
    double recons_26 = in_97 < 0.0 ? (-out_36) : out_36;
    return recons_26;
}

double my_core_function_tan_7(double in_101)
{
// (periodic (- (* PI (- 2))) (MirrorRight (- x) (Horner (MinimaxPolynomial (tan x) [(/ (* PI (- 2)) 2) 0]))))
    int k_35 = (int) floor((((double)in_101)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_100 = ((double)in_101) - k_35*((double)6.283185307179586);
    double in_99 = in_100 < 0.0 ? in_100 : (0.0 - in_100);
    double out_37 = (((double)in_99)*(((double)-0x1.073b6f56a759c1ab92f3bda021d6895p15) 
        + ((double)in_99)*(((double)-0x1.8164b81e32b2a8e4fce9eb7d52119e3p19) 
        + ((double)in_99)*(((double)-0x1.8a7166833d05c154987a734057e632d8p22) 
        + ((double)in_99)*(((double)-0x1.96856c047adcdc9722039a801b5484d4p24) 
        + ((double)in_99)*(((double)-0x1.edf44a4329d862f87e1353dee639be4ep25) 
        + ((double)in_99)*(((double)-0x1.81588acbdc5cbebb54cb44d117b40a98p26) 
        + ((double)in_99)*(((double)-0x1.95adb8f2301b6e6ce27d705559f9f9f8p26) 
        + ((double)in_99)*(((double)-0x1.284d269c48d944ebe93c907fcc6e1dbp26) 
        + ((double)in_99)*(((double)-0x1.2fc60def4879c0ff646ff8ac395a97dp25) 
        + ((double)in_99)*(((double)-0x1.b39c1fe0532cd2c9993840f31daaea74p23) 
        + ((double)in_99)*(((double)-0x1.ab9b73ed8645b022b097a19a791dc994p21) 
        + ((double)in_99)*(((double)-0x1.119df85a29d04642ee14b9e3effdaf9ap19) 
        + ((double)in_99)*(((double)-0x1.9b0081cb84d1d52c2e9c9c264d34aef4p15) 
        + ((double)in_99)*((double)-0x1.129fb343298fb8003c7929dc16c74654p11)))))))))))))));
    double recons_27 = in_100 < 0.0 ? out_37 : (-out_37);
    return recons_27;
}
