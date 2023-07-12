#include "funcs.h"
#include "table_generation.h"
#include <assert.h>
#include <math.h>

double libm_core_function_sin(double x)
{
    return sin(x);
}

int mpfr_core_function_sin(mpfr_t out, double dx)
{
  static int init_called = 0;
  static mpfr_t x;
  if (!init_called) {
    mpfr_init2(x, ORACLE_PREC);
    init_called = 1;
  }
  mpfr_set_d(x, dx, MPFR_RNDN);
  mpfr_sin(out, x, MPFR_RNDN);
  return 0;
}

double my_core_function_sin_0(double in_55)
{
// (periodic (+ PI PI) (Horner (MinimaxPolynomial (sin x) [0.0 (+ PI PI)])))
    int k_18 = (int) floor((((double)in_55)-((double)0.0))*((double)0.15915494309189535));
    double in_54 = ((double)in_55) - k_18*((double)6.283185307179586);
    double out_20 = (((double)in_54)*(((double)0x1.fffffe2f8a0046652e2bfaa63bbbd214p-1) 
        + ((double)in_54)*(((double)0x1.a12d9703db57edc2478240add6f8302ap-21) 
        + ((double)in_54)*(((double)-0x1.55576219c1a5ba1b0e311b4034036286p-3) 
        + ((double)in_54)*(((double)0x1.4d4a9f3a92460453f452b2a6388522fcp-17) 
        + ((double)in_54)*(((double)0x1.1093c69f4d261306e7ca5c9423717a3cp-7) 
        + ((double)in_54)*(((double)0x1.e672d75c0494c66f1874c22b687387dep-17) 
        + ((double)in_54)*(((double)-0x1.b42652015f5d05c3193bcaeafce74fc6p-13) 
        + ((double)in_54)*(((double)0x1.27ee727c4e19da9d7a927f7d444efa62p-18) 
        + ((double)in_54)*(((double)0x1.60d9bf29b135881f577b2775d02bd8fcp-20) 
        + ((double)in_54)*(((double)0x1.653184dae8e937829eb7cbcbb2690098p-22) 
        + ((double)in_54)*(((double)-0x1.4ec2a0c2fc99a4e7e062a9252573f7e6p-24) 
        + ((double)in_54)*(((double)0x1.74344215a0c4a4832b8a548b3baa1f08p-28) 
        + ((double)in_54)*(((double)-0x1.1f75197e8def097c835edf2cc2351af2p-33) 
        + ((double)in_54)*((double)-0x1.777b24606dd83bb52a5e865a2a7f7292p-44)))))))))))))));
    return out_20;
}

double my_core_function_sin_1(double in_57)
{
// (periodic (+ PI PI) (Horner (MinimaxPolynomial (sin x) [(/ (* PI (- 2)) 2) (/ (+ PI PI) 2)])))
    int k_19 = (int) floor((((double)in_57)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_56 = ((double)in_57) - k_19*((double)6.283185307179586);
    double out_21 = (((double)in_56)*(((double)0x1.ffffffd0e481647e3f9c9be1bc259952p-1) 
        + ((double)in_56)*(((double)0x1.3dec852a8b43e0ba9c993fbe4d55302p-50) 
        + ((double)in_56)*(((double)-0x1.55555288fd2b1aa54cb3007ad5ef35dep-3) 
        + ((double)in_56)*(((double)-0x1.405c1ede9482117e5876306417234318p-49) 
        + ((double)in_56)*(((double)0x1.1110dfcd141aa39f5c1c44488a182a84p-7) 
        + ((double)in_56)*(((double)0x1.adc69484391738914c43770dfec5c38cp-50) 
        + ((double)in_56)*(((double)-0x1.a01405e324e691e115829bb3642d8408p-13) 
        + ((double)in_56)*(((double)-0x1.07502f79741b852cae32ca3cb2f925aep-51) 
        + ((double)in_56)*(((double)0x1.717e7c1dc0f2ccf6a6bfef1db7ff10e2p-19) 
        + ((double)in_56)*(((double)0x1.44852c407ab32e51fd8849f3b490bf44p-54) 
        + ((double)in_56)*(((double)-0x1.a7f277288e7d347e5eb215bad3874fe6p-26) 
        + ((double)in_56)*(((double)-0x1.874de95194bdc2e1fbc7bb5a2d9a50ep-58) 
        + ((double)in_56)*(((double)0x1.27cd1ba9351d29e52726e25c714240fcp-33) 
        + ((double)in_56)*((double)0x1.6f01852465a4d8f227369e10e8f82db4p-63)))))))))))))));
    return out_21;
}

double my_core_function_sin_2(double in_60)
{
// (periodic (+ PI PI) (MirrorLeft x (Horner (MinimaxPolynomial (sin x) [PI (+ PI PI)]))))
    int k_20 = (int) floor((((double)in_60)-((double)0.0))*((double)0.15915494309189535));
    double in_59 = ((double)in_60) - k_20*((double)6.283185307179586);
    double in_58 = in_59 < 3.141592653589793 ? (3.141592653589793 - in_59) : in_59;
    double out_22 = (((double)in_58)*(((double)0x1.ffa7a0a3cf8e671f6bb66a249223aaaep-1) 
        + ((double)in_58)*(((double)0x1.1d1ec26d0d533709853e23cb901ece48p-9) 
        + ((double)in_58)*(((double)-0x1.5bfd403edc8c9b8383e355f327a8adbap-3) 
        + ((double)in_58)*(((double)0x1.86ac2f2a62bccdd371a0c97d3c600ebep-9) 
        + ((double)in_58)*(((double)0x1.a744f6b838920b5e31e9e9ff6de7511ap-8) 
        + ((double)in_58)*(((double)0x1.c081fb18e99eafa9b204cfe2eda6e7a6p-11) 
        + ((double)in_58)*(((double)-0x1.0115d7b45d3fe5cb92d12e24d2cdbd28p-11) 
        + ((double)in_58)*(((double)0x1.3d35017ef2ba9828aed6a51722082ee6p-14) 
        + ((double)in_58)*(((double)-0x1.97ff5475c00294b7f527727b5f30d6dcp-17) 
        + ((double)in_58)*(((double)0x1.29c04deceb4fe3898321370d7f0e4d98p-19) 
        + ((double)in_58)*(((double)-0x1.1f281f4feb4e3a9d612931769c4e354p-22) 
        + ((double)in_58)*(((double)0x1.3b25d5002d3338449dc24bd437d65848p-26) 
        + ((double)in_58)*(((double)-0x1.6e88e803182b2c56cbc7806a1a489deep-31) 
        + ((double)in_58)*((double)0x1.63921baca2652b0abd799ce872d336eep-37)))))))))))))));
    double recons_16 = in_59 < 3.141592653589793 ? out_22 : out_22;
    return recons_16;
}

double my_core_function_sin_3(double in_63)
{
// (periodic (+ PI PI) (MirrorRight x (Horner (MinimaxPolynomial (sin x) [0.0 PI]))))
    int k_21 = (int) floor((((double)in_63)-((double)0.0))*((double)0.15915494309189535));
    double in_62 = ((double)in_63) - k_21*((double)6.283185307179586);
    double in_61 = in_62 < 3.141592653589793 ? in_62 : (6.283185307179586 - in_62);
    double out_23 = (((double)in_61)*(((double)0x1.00000000003cb0067f0b6b796e0cbe92p0) 
        + ((double)in_61)*(((double)-0x1.f1539b1f3a373d06687bd16d8984fe6cp-38) 
        + ((double)in_61)*(((double)-0x1.555555528a598cfe96aadd9753a86a38p-3) 
        + ((double)in_61)*(((double)-0x1.04782924118d1beb073006b4e67b9bccp-31) 
        + ((double)in_61)*(((double)0x1.11111498c02e48b35de474de478e1a8ap-7) 
        + ((double)in_61)*(((double)-0x1.fe05eedd7b9e1e063b04d8ad5249aca2p-29) 
        + ((double)in_61)*(((double)-0x1.a016eaa2be2170df3598e5288a938d34p-13) 
        + ((double)in_61)*(((double)-0x1.b3de4606534174c0a84776e9920c73p-28) 
        + ((double)in_61)*(((double)0x1.728c5043d2d7e69c4b039bc9c5463c44p-19) 
        + ((double)in_61)*(((double)-0x1.969990b39d0b49f83a08d0090f92cb12p-29) 
        + ((double)in_61)*(((double)-0x1.98c0b15a5d4d407845606168ce54cac2p-26) 
        + ((double)in_61)*(((double)-0x1.a73226a8e63d5f9f7c5d326d9422d7a8p-32) 
        + ((double)in_61)*(((double)0x1.0a103bbcaf5f953c518ff0b1b139ad58p-32) 
        + ((double)in_61)*((double)-0x1.8328374a2e9c269a98c1628fee33e2e4p-37)))))))))))))));
    double recons_17 = in_62 < 3.141592653589793 ? out_23 : out_23;
    return recons_17;
}

double my_core_function_sin_4(double in_66)
{
// (periodic (+ PI PI) (MirrorLeft (+ x (* x (- 2))) (Horner (MinimaxPolynomial (sin x) [0 (/ (+ PI PI) 2)]))))
    int k_22 = (int) floor((((double)in_66)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_65 = ((double)in_66) - k_22*((double)6.283185307179586);
    double in_64 = in_65 < 0.0 ? (0.0 - in_65) : in_65;
    double out_24 = (((double)in_64)*(((double)0x1.00000000003cb0067f0b6b796e0cbe92p0) 
        + ((double)in_64)*(((double)-0x1.f1539b1f3a373d06687bd16d8984fe6cp-38) 
        + ((double)in_64)*(((double)-0x1.555555528a598cfe96aadd9753a86a38p-3) 
        + ((double)in_64)*(((double)-0x1.04782924118d1beb073006b4e67b9bccp-31) 
        + ((double)in_64)*(((double)0x1.11111498c02e48b35de474de478e1a8ap-7) 
        + ((double)in_64)*(((double)-0x1.fe05eedd7b9e1e063b04d8ad5249aca2p-29) 
        + ((double)in_64)*(((double)-0x1.a016eaa2be2170df3598e5288a938d34p-13) 
        + ((double)in_64)*(((double)-0x1.b3de4606534174c0a84776e9920c73p-28) 
        + ((double)in_64)*(((double)0x1.728c5043d2d7e69c4b039bc9c5463c44p-19) 
        + ((double)in_64)*(((double)-0x1.969990b39d0b49f83a08d0090f92cb12p-29) 
        + ((double)in_64)*(((double)-0x1.98c0b15a5d4d407845606168ce54cac2p-26) 
        + ((double)in_64)*(((double)-0x1.a73226a8e63d5f9f7c5d326d9422d7a8p-32) 
        + ((double)in_64)*(((double)0x1.0a103bbcaf5f953c518ff0b1b139ad58p-32) 
        + ((double)in_64)*((double)-0x1.8328374a2e9c269a98c1628fee33e2e4p-37)))))))))))))));
    double recons_18 = in_65 < 0.0 ? (out_24+(out_24*(-2))) : out_24;
    return recons_18;
}

double my_core_function_sin_5(double in_69)
{
// (periodic (+ PI PI) (MirrorLeft (- x) (Horner (MinimaxPolynomial (sin x) [0 (/ (+ PI PI) 2)]))))
    int k_23 = (int) floor((((double)in_69)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_68 = ((double)in_69) - k_23*((double)6.283185307179586);
    double in_67 = in_68 < 0.0 ? (0.0 - in_68) : in_68;
    double out_25 = (((double)in_67)*(((double)0x1.00000000003cb0067f0b6b796e0cbe92p0) 
        + ((double)in_67)*(((double)-0x1.f1539b1f3a373d06687bd16d8984fe6cp-38) 
        + ((double)in_67)*(((double)-0x1.555555528a598cfe96aadd9753a86a38p-3) 
        + ((double)in_67)*(((double)-0x1.04782924118d1beb073006b4e67b9bccp-31) 
        + ((double)in_67)*(((double)0x1.11111498c02e48b35de474de478e1a8ap-7) 
        + ((double)in_67)*(((double)-0x1.fe05eedd7b9e1e063b04d8ad5249aca2p-29) 
        + ((double)in_67)*(((double)-0x1.a016eaa2be2170df3598e5288a938d34p-13) 
        + ((double)in_67)*(((double)-0x1.b3de4606534174c0a84776e9920c73p-28) 
        + ((double)in_67)*(((double)0x1.728c5043d2d7e69c4b039bc9c5463c44p-19) 
        + ((double)in_67)*(((double)-0x1.969990b39d0b49f83a08d0090f92cb12p-29) 
        + ((double)in_67)*(((double)-0x1.98c0b15a5d4d407845606168ce54cac2p-26) 
        + ((double)in_67)*(((double)-0x1.a73226a8e63d5f9f7c5d326d9422d7a8p-32) 
        + ((double)in_67)*(((double)0x1.0a103bbcaf5f953c518ff0b1b139ad58p-32) 
        + ((double)in_67)*((double)-0x1.8328374a2e9c269a98c1628fee33e2e4p-37)))))))))))))));
    double recons_19 = in_68 < 0.0 ? (-out_25) : out_25;
    return recons_19;
}

double my_core_function_sin_6(double in_72)
{
// (periodic (+ PI PI) (MirrorLeft (/ (* x (- 2)) 2) (Horner (MinimaxPolynomial (sin x) [0 (/ (+ PI PI) 2)]))))
    int k_24 = (int) floor((((double)in_72)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_71 = ((double)in_72) - k_24*((double)6.283185307179586);
    double in_70 = in_71 < 0.0 ? (0.0 - in_71) : in_71;
    double out_26 = (((double)in_70)*(((double)0x1.00000000003cb0067f0b6b796e0cbe92p0) 
        + ((double)in_70)*(((double)-0x1.f1539b1f3a373d06687bd16d8984fe6cp-38) 
        + ((double)in_70)*(((double)-0x1.555555528a598cfe96aadd9753a86a38p-3) 
        + ((double)in_70)*(((double)-0x1.04782924118d1beb073006b4e67b9bccp-31) 
        + ((double)in_70)*(((double)0x1.11111498c02e48b35de474de478e1a8ap-7) 
        + ((double)in_70)*(((double)-0x1.fe05eedd7b9e1e063b04d8ad5249aca2p-29) 
        + ((double)in_70)*(((double)-0x1.a016eaa2be2170df3598e5288a938d34p-13) 
        + ((double)in_70)*(((double)-0x1.b3de4606534174c0a84776e9920c73p-28) 
        + ((double)in_70)*(((double)0x1.728c5043d2d7e69c4b039bc9c5463c44p-19) 
        + ((double)in_70)*(((double)-0x1.969990b39d0b49f83a08d0090f92cb12p-29) 
        + ((double)in_70)*(((double)-0x1.98c0b15a5d4d407845606168ce54cac2p-26) 
        + ((double)in_70)*(((double)-0x1.a73226a8e63d5f9f7c5d326d9422d7a8p-32) 
        + ((double)in_70)*(((double)0x1.0a103bbcaf5f953c518ff0b1b139ad58p-32) 
        + ((double)in_70)*((double)-0x1.8328374a2e9c269a98c1628fee33e2e4p-37)))))))))))))));
    double recons_20 = in_71 < 0.0 ? ((out_26*(-2))/2) : out_26;
    return recons_20;
}

double my_core_function_sin_7(double in_75)
{
// (periodic (+ PI PI) (MirrorRight (+ x (* x (- 2))) (Horner (MinimaxPolynomial (sin x) [(/ (* PI (- 2)) 2) 0]))))
    int k_25 = (int) floor((((double)in_75)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_74 = ((double)in_75) - k_25*((double)6.283185307179586);
    double in_73 = in_74 < 0.0 ? in_74 : (0.0 - in_74);
    double out_27 = (((double)in_73)*(((double)0x1.00000000003cb0067f0b6b57b15ba676p0) 
        + ((double)in_73)*(((double)0x1.f1539b1f3a3700e4af203ba7fbf5c912p-38) 
        + ((double)in_73)*(((double)-0x1.555555528a598cfe96aae1ebf8325784p-3) 
        + ((double)in_73)*(((double)0x1.04782924118d26ef2e7dc7239cc3dc46p-31) 
        + ((double)in_73)*(((double)0x1.11111498c02e48b35e1b9d912bbc85c8p-7) 
        + ((double)in_73)*(((double)0x1.fe05eedd7b9e3e4667e39d7d1a32babep-29) 
        + ((double)in_73)*(((double)-0x1.a016eaa2be2170df08c562e0f084a754p-13) 
        + ((double)in_73)*(((double)0x1.b3de4606534188ef11f41bef731092aep-28) 
        + ((double)in_73)*(((double)0x1.728c5043d2d7e6a267e29b7ac0ea490cp-19) 
        + ((double)in_73)*(((double)0x1.969990b39d0b540aae96c76e9c11b7f2p-29) 
        + ((double)in_73)*(((double)-0x1.98c0b15a5d4d401f24fb1e551a791a5cp-26) 
        + ((double)in_73)*(((double)0x1.a73226a8e63d63956a70a69ee2444684p-32) 
        + ((double)in_73)*(((double)0x1.0a103bbcaf5f95a5061f84025821a9d6p-32) 
        + ((double)in_73)*((double)0x1.8328374a2e9c2733614929013e076826p-37)))))))))))))));
    double recons_21 = in_74 < 0.0 ? out_27 : (out_27+(out_27*(-2)));
    return recons_21;
}

double my_core_function_sin_8(double in_78)
{
// (periodic (+ PI PI) (MirrorRight (- x) (Horner (MinimaxPolynomial (sin x) [(/ (* PI (- 2)) 2) 0]))))
    int k_26 = (int) floor((((double)in_78)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_77 = ((double)in_78) - k_26*((double)6.283185307179586);
    double in_76 = in_77 < 0.0 ? in_77 : (0.0 - in_77);
    double out_28 = (((double)in_76)*(((double)0x1.00000000003cb0067f0b6b57b15ba676p0) 
        + ((double)in_76)*(((double)0x1.f1539b1f3a3700e4af203ba7fbf5c912p-38) 
        + ((double)in_76)*(((double)-0x1.555555528a598cfe96aae1ebf8325784p-3) 
        + ((double)in_76)*(((double)0x1.04782924118d26ef2e7dc7239cc3dc46p-31) 
        + ((double)in_76)*(((double)0x1.11111498c02e48b35e1b9d912bbc85c8p-7) 
        + ((double)in_76)*(((double)0x1.fe05eedd7b9e3e4667e39d7d1a32babep-29) 
        + ((double)in_76)*(((double)-0x1.a016eaa2be2170df08c562e0f084a754p-13) 
        + ((double)in_76)*(((double)0x1.b3de4606534188ef11f41bef731092aep-28) 
        + ((double)in_76)*(((double)0x1.728c5043d2d7e6a267e29b7ac0ea490cp-19) 
        + ((double)in_76)*(((double)0x1.969990b39d0b540aae96c76e9c11b7f2p-29) 
        + ((double)in_76)*(((double)-0x1.98c0b15a5d4d401f24fb1e551a791a5cp-26) 
        + ((double)in_76)*(((double)0x1.a73226a8e63d63956a70a69ee2444684p-32) 
        + ((double)in_76)*(((double)0x1.0a103bbcaf5f95a5061f84025821a9d6p-32) 
        + ((double)in_76)*((double)0x1.8328374a2e9c2733614929013e076826p-37)))))))))))))));
    double recons_22 = in_77 < 0.0 ? out_28 : (-out_28);
    return recons_22;
}

double my_core_function_sin_9(double in_81)
{
// (periodic (+ PI PI) (MirrorRight (/ (* x (- 2)) 2) (Horner (MinimaxPolynomial (sin x) [(/ (* PI (- 2)) 2) 0]))))
    int k_27 = (int) floor((((double)in_81)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_80 = ((double)in_81) - k_27*((double)6.283185307179586);
    double in_79 = in_80 < 0.0 ? in_80 : (0.0 - in_80);
    double out_29 = (((double)in_79)*(((double)0x1.00000000003cb0067f0b6b57b15ba676p0) 
        + ((double)in_79)*(((double)0x1.f1539b1f3a3700e4af203ba7fbf5c912p-38) 
        + ((double)in_79)*(((double)-0x1.555555528a598cfe96aae1ebf8325784p-3) 
        + ((double)in_79)*(((double)0x1.04782924118d26ef2e7dc7239cc3dc46p-31) 
        + ((double)in_79)*(((double)0x1.11111498c02e48b35e1b9d912bbc85c8p-7) 
        + ((double)in_79)*(((double)0x1.fe05eedd7b9e3e4667e39d7d1a32babep-29) 
        + ((double)in_79)*(((double)-0x1.a016eaa2be2170df08c562e0f084a754p-13) 
        + ((double)in_79)*(((double)0x1.b3de4606534188ef11f41bef731092aep-28) 
        + ((double)in_79)*(((double)0x1.728c5043d2d7e6a267e29b7ac0ea490cp-19) 
        + ((double)in_79)*(((double)0x1.969990b39d0b540aae96c76e9c11b7f2p-29) 
        + ((double)in_79)*(((double)-0x1.98c0b15a5d4d401f24fb1e551a791a5cp-26) 
        + ((double)in_79)*(((double)0x1.a73226a8e63d63956a70a69ee2444684p-32) 
        + ((double)in_79)*(((double)0x1.0a103bbcaf5f95a5061f84025821a9d6p-32) 
        + ((double)in_79)*((double)0x1.8328374a2e9c2733614929013e076826p-37)))))))))))))));
    double recons_23 = in_80 < 0.0 ? out_29 : ((out_29*(-2))/2);
    return recons_23;
}
