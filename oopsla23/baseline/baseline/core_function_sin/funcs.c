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
// (periodic (* PI 6) (Horner (MinimaxPolynomial (sin x) [0.0 (* PI 6)])))
    int k_16 = (int) floor((((double)in_55)-((double)0.0))*((double)0.05305164769729845));
    double in_54 = ((double)in_55) - k_16*((double)18.84955592153876);
    double out_22 = (((double)in_54)*(((double)0x1.dd5280668eb68dfd86e3ac16af54f6bap-1) 
        + ((double)in_54)*(((double)0x1.3cacd0055567f64125385a38b783054ep-2) 
        + ((double)in_54)*(((double)-0x1.5128a2a51e2159c74e7c490ac9f2cb2ap-1) 
        + ((double)in_54)*(((double)0x1.90bb027a619085566743b631756ba8a4p-2) 
        + ((double)in_54)*(((double)-0x1.62ecd2b195f45dc166c1c1be209fbe88p-3) 
        + ((double)in_54)*(((double)0x1.b41663a07ea1438414f73664be985698p-5) 
        + ((double)in_54)*(((double)-0x1.565ea5e3609eacc4c14817c5cb1bdb52p-7) 
        + ((double)in_54)*(((double)0x1.5787941d139fea87fc46de95992f822p-10) 
        + ((double)in_54)*(((double)-0x1.bdefbb9747eef7683bdb98835befe772p-14) 
        + ((double)in_54)*(((double)0x1.746f5f01132849598358580c3a22f9dp-18) 
        + ((double)in_54)*(((double)-0x1.80c1709f0e2af8757ba70ab429410e7ep-23) 
        + ((double)in_54)*(((double)0x1.b8600d33ee4ca1848beaea6da56b6a6cp-29) 
        + ((double)in_54)*(((double)-0x1.850495820fef029d48d1f8c41966a018p-36) 
        + ((double)in_54)*((double)-0x1.0a4390695749ab1a1b752400a6467844p-44)))))))))))))));
    return out_22;
}

double my_core_function_sin_1(double in_57)
{
// (periodic (* PI 6) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) (* PI 3)])))
    int k_17 = (int) floor((((double)in_57)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_56 = ((double)in_57) - k_17*((double)18.84955592153876);
    double out_23 = (((double)in_56)*(((double)0x1.fc3373f49b114406d5df0a9ea051dad4p-1) 
        + ((double)in_56)*(((double)0x1.0b22dfb4686f971fc9378239fefc007cp-29) 
        + ((double)in_56)*(((double)-0x1.4e96d7598c7140bafbc6278ff6940da8p-3) 
        + ((double)in_56)*(((double)-0x1.bd9e43680fb542dd8f0ef2272e975d98p-32) 
        + ((double)in_56)*(((double)0x1.0320423526f769e0c12c038954b57b32p-7) 
        + ((double)in_56)*(((double)0x1.c66a642282fdeaa4eb3f6675b131eb8p-36) 
        + ((double)in_56)*(((double)-0x1.6c8a41a14a563243856c99ca79267d88p-13) 
        + ((double)in_56)*(((double)-0x1.accbca7614eb813b1b65588d89d22eb2p-41) 
        + ((double)in_56)*(((double)0x1.0d291d1aa8b515e9ec49c90b1718f1p-19) 
        + ((double)in_56)*(((double)0x1.a0aedc989c499384cf99dabe92aa606ep-47) 
        + ((double)in_56)*(((double)-0x1.9ea40743b0e0b11971e2a59bf7079182p-27) 
        + ((double)in_56)*(((double)-0x1.951d2446ac82b42b2bf515b5b37e7b32p-54) 
        + ((double)in_56)*(((double)0x1.09bb1ee36ceb09eb86dc1405d5ba910ap-35) 
        + ((double)in_56)*((double)0x1.38225fb30413e430c110987522cdf3e4p-62)))))))))))))));
    return out_23;
}

double my_core_function_sin_2(double in_59)
{
// (periodic (* PI 4) (Horner (MinimaxPolynomial (sin x) [0.0 (* PI 4)])))
    int k_18 = (int) floor((((double)in_59)-((double)0.0))*((double)0.07957747154594767));
    double in_58 = ((double)in_59) - k_18*((double)12.566370614359172);
    double out_24 = (((double)in_58)*(((double)0x1.00238c7505bf07bbccefb6c3962ca5a2p0) 
        + ((double)in_58)*(((double)-0x1.f670d717eba139d308a34ebd4b076126p-9) 
        + ((double)in_58)*(((double)-0x1.41f1eef9bf54e807d34f88c9a509f71p-3) 
        + ((double)in_58)*(((double)-0x1.81854bfb2a1e20ecdced7bf94d9d5b7ep-7) 
        + ((double)in_58)*(((double)0x1.159227bf77d757001564b6b8224a885p-6) 
        + ((double)in_58)*(((double)-0x1.084af1d7c5b2ace42e63b25c74bc2c0cp-8) 
        + ((double)in_58)*(((double)0x1.184687416e5d784c59a5bd2929ab0d9ap-10) 
        + ((double)in_58)*(((double)-0x1.1e8a59580bc03fd689b30b42c549375cp-12) 
        + ((double)in_58)*(((double)0x1.69e98cb96b035d55baf09fd45e14ca76p-15) 
        + ((double)in_58)*(((double)-0x1.0a59ba64297b79cb96c6d3dd1aea73f8p-18) 
        + ((double)in_58)*(((double)0x1.c50f7d4d99a3662be4d1510ac26ff42cp-23) 
        + ((double)in_58)*(((double)-0x1.9d4bbaf41291054473af050d0d5538eap-28) 
        + ((double)in_58)*(((double)0x1.3014a481a5b5f4e53b03a5ef86b40df2p-34) 
        + ((double)in_58)*((double)0x1.bbf881259d56dfe6af072d028537dbb4p-44)))))))))))))));
    return out_24;
}

double my_core_function_sin_3(double in_61)
{
// (periodic (* PI 4) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) (+ PI PI)])))
    int k_19 = (int) floor((((double)in_61)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_60 = ((double)in_61) - k_19*((double)12.566370614359172);
    double out_25 = (((double)in_60)*(((double)0x1.fff8989b79af2bff4e0a54a980043728p-1) 
        + ((double)in_60)*(((double)0x1.0c5f19ceee8c1e24439992144ca12b94p-35) 
        + ((double)in_60)*(((double)-0x1.5538b8639a49156b076690bf77a5ac7ap-3) 
        + ((double)in_60)*(((double)-0x1.e2d94b9502a0604123410ffb2ce64e96p-37) 
        + ((double)in_60)*(((double)0x1.1090cd4ad59084a54cec09f70aa61d2p-7) 
        + ((double)in_60)*(((double)0x1.05f9a498ebd0102f8d687dd0899ba352p-39) 
        + ((double)in_60)*(((double)-0x1.9c1e3b48ca66bed76270843092feb394p-13) 
        + ((double)in_60)*(((double)-0x1.05a9878dcf7282d80791d1bf7b6c066ep-43) 
        + ((double)in_60)*(((double)0x1.616d94402ec80413e00bcef5e43f0abep-19) 
        + ((double)in_60)*(((double)0x1.0cceed9c98aa124d940ec2d32c8ca0d6p-48) 
        + ((double)in_60)*(((double)-0x1.64045732014a57937e78b86582088c9cp-26) 
        + ((double)in_60)*(((double)-0x1.14beaa4ea95869526f94024d0cf25e3ap-54) 
        + ((double)in_60)*(((double)0x1.5795d412527f8eb8bd29c165192cf698p-34) 
        + ((double)in_60)*((double)0x1.c51a91464850fdeb130b7f04d417d08ap-62)))))))))))))));
    return out_25;
}

double my_core_function_sin_4(double in_63)
{
// (periodic (+ PI PI) (Horner (MinimaxPolynomial (sin x) [0.0 (+ PI PI)])))
    int k_20 = (int) floor((((double)in_63)-((double)0.0))*((double)0.15915494309189535));
    double in_62 = ((double)in_63) - k_20*((double)6.283185307179586);
    double out_26 = (((double)in_62)*(((double)0x1.fffffe2f8a0046652e2bfaa63bbbd214p-1) 
        + ((double)in_62)*(((double)0x1.a12d9703db57edc2478240add6f8302ap-21) 
        + ((double)in_62)*(((double)-0x1.55576219c1a5ba1b0e311b4034036286p-3) 
        + ((double)in_62)*(((double)0x1.4d4a9f3a92460453f452b2a6388522fcp-17) 
        + ((double)in_62)*(((double)0x1.1093c69f4d261306e7ca5c9423717a3cp-7) 
        + ((double)in_62)*(((double)0x1.e672d75c0494c66f1874c22b687387dep-17) 
        + ((double)in_62)*(((double)-0x1.b42652015f5d05c3193bcaeafce74fc6p-13) 
        + ((double)in_62)*(((double)0x1.27ee727c4e19da9d7a927f7d444efa62p-18) 
        + ((double)in_62)*(((double)0x1.60d9bf29b135881f577b2775d02bd8fcp-20) 
        + ((double)in_62)*(((double)0x1.653184dae8e937829eb7cbcbb2690098p-22) 
        + ((double)in_62)*(((double)-0x1.4ec2a0c2fc99a4e7e062a9252573f7e6p-24) 
        + ((double)in_62)*(((double)0x1.74344215a0c4a4832b8a548b3baa1f08p-28) 
        + ((double)in_62)*(((double)-0x1.1f75197e8def097c835edf2cc2351af2p-33) 
        + ((double)in_62)*((double)-0x1.777b24606dd83bb52a5e865a2a7f7292p-44)))))))))))))));
    return out_26;
}

double my_core_function_sin_5(double in_65)
{
// (periodic (+ PI PI) (Horner (MinimaxPolynomial (sin x) [(- PI) PI])))
    int k_21 = (int) floor((((double)in_65)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_64 = ((double)in_65) - k_21*((double)6.283185307179586);
    double out_27 = (((double)in_64)*(((double)0x1.ffffffd0e481647e3f9c9be1bc259952p-1) 
        + ((double)in_64)*(((double)0x1.3dec852a8b43e0ba9c993fbe4d55302p-50) 
        + ((double)in_64)*(((double)-0x1.55555288fd2b1aa54cb3007ad5ef35dep-3) 
        + ((double)in_64)*(((double)-0x1.405c1ede9482117e5876306417234318p-49) 
        + ((double)in_64)*(((double)0x1.1110dfcd141aa39f5c1c44488a182a84p-7) 
        + ((double)in_64)*(((double)0x1.adc69484391738914c43770dfec5c38cp-50) 
        + ((double)in_64)*(((double)-0x1.a01405e324e691e115829bb3642d8408p-13) 
        + ((double)in_64)*(((double)-0x1.07502f79741b852cae32ca3cb2f925aep-51) 
        + ((double)in_64)*(((double)0x1.717e7c1dc0f2ccf6a6bfef1db7ff10e2p-19) 
        + ((double)in_64)*(((double)0x1.44852c407ab32e51fd8849f3b490bf44p-54) 
        + ((double)in_64)*(((double)-0x1.a7f277288e7d347e5eb215bad3874fe6p-26) 
        + ((double)in_64)*(((double)-0x1.874de95194bdc2e1fbc7bb5a2d9a50ep-58) 
        + ((double)in_64)*(((double)0x1.27cd1ba9351d29e52726e25c714240fcp-33) 
        + ((double)in_64)*((double)0x1.6f01852465a4d8f227369e10e8f82db4p-63)))))))))))))));
    return out_27;
}

double my_core_function_sin_6(double in_68)
{
// (periodic (* PI 6) (MirrorLeft (+ (- (- x 2)) (- 2)) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))
    int k_22 = (int) floor((((double)in_68)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_67 = ((double)in_68) - k_22*((double)18.84955592153876);
    double in_66 = in_67 < 0.0 ? (0.0 - in_67) : in_67;
    double out_28 = (((double)in_66)*(((double)0x1.ffffb35d7bc85fc9209dba097cfc69cp-1) 
        + ((double)in_66)*(((double)0x1.9f1cd63f17e4027947547097909455ccp-16) 
        + ((double)in_66)*(((double)-0x1.558699661a1dd85ddf798909b72fff82p-3) 
        + ((double)in_66)*(((double)0x1.7ab23ed714b2c36137f8a1551b1391eap-13) 
        + ((double)in_66)*(((double)0x1.0a50a3b4f10a9929b286c04468d8dcd4p-7) 
        + ((double)in_66)*(((double)0x1.3fa5e1086c232ab5ff9c964b7c1a36b4p-13) 
        + ((double)in_66)*(((double)-0x1.20d46d62cdf54bf05c54545ee536cb02p-12) 
        + ((double)in_66)*(((double)0x1.cc61d2ae04a7785156eab4656554cb2p-16) 
        + ((double)in_66)*(((double)-0x1.1c68103b31cd98de17eb8e6730abab2p-18) 
        + ((double)in_66)*(((double)0x1.566628c148bf18d12de522f97a437164p-20) 
        + ((double)in_66)*(((double)-0x1.94985c0b84238863c6ad9188afaaaa3p-23) 
        + ((double)in_66)*(((double)0x1.de66bf7d5694e65da70a1f3b1ae5bdc8p-27) 
        + ((double)in_66)*(((double)-0x1.1d2579519a5af9410a02018b76343ceep-31) 
        + ((double)in_66)*((double)0x1.149deb9af0ead7baf05b6209f1faa2d4p-37)))))))))))))));
    double recons_16 = in_67 < 0.0 ? ((-(out_28-2))+(-2)) : out_28;
    return recons_16;
}

double my_core_function_sin_7(double in_71)
{
// (periodic (* PI 6) (MirrorLeft (- (+ (+ PI PI) (- (* PI 4) x)) (* PI 6)) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))
    int k_23 = (int) floor((((double)in_71)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_70 = ((double)in_71) - k_23*((double)18.84955592153876);
    double in_69 = in_70 < 0.0 ? (0.0 - in_70) : in_70;
    double out_29 = (((double)in_69)*(((double)0x1.ffffb35d7bc85fc9209dba097cfc69cp-1) 
        + ((double)in_69)*(((double)0x1.9f1cd63f17e4027947547097909455ccp-16) 
        + ((double)in_69)*(((double)-0x1.558699661a1dd85ddf798909b72fff82p-3) 
        + ((double)in_69)*(((double)0x1.7ab23ed714b2c36137f8a1551b1391eap-13) 
        + ((double)in_69)*(((double)0x1.0a50a3b4f10a9929b286c04468d8dcd4p-7) 
        + ((double)in_69)*(((double)0x1.3fa5e1086c232ab5ff9c964b7c1a36b4p-13) 
        + ((double)in_69)*(((double)-0x1.20d46d62cdf54bf05c54545ee536cb02p-12) 
        + ((double)in_69)*(((double)0x1.cc61d2ae04a7785156eab4656554cb2p-16) 
        + ((double)in_69)*(((double)-0x1.1c68103b31cd98de17eb8e6730abab2p-18) 
        + ((double)in_69)*(((double)0x1.566628c148bf18d12de522f97a437164p-20) 
        + ((double)in_69)*(((double)-0x1.94985c0b84238863c6ad9188afaaaa3p-23) 
        + ((double)in_69)*(((double)0x1.de66bf7d5694e65da70a1f3b1ae5bdc8p-27) 
        + ((double)in_69)*(((double)-0x1.1d2579519a5af9410a02018b76343ceep-31) 
        + ((double)in_69)*((double)0x1.149deb9af0ead7baf05b6209f1faa2d4p-37)))))))))))))));
    double recons_17 = in_70 < 0.0 ? (((M_PI+M_PI)+((M_PI*4)-out_29))-(M_PI*6)) : out_29;
    return recons_17;
}

double my_core_function_sin_8(double in_74)
{
// (periodic (* PI 6) (MirrorLeft (- (* PI 4) (+ x (* PI 4))) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))
    int k_24 = (int) floor((((double)in_74)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_73 = ((double)in_74) - k_24*((double)18.84955592153876);
    double in_72 = in_73 < 0.0 ? (0.0 - in_73) : in_73;
    double out_30 = (((double)in_72)*(((double)0x1.ffffb35d7bc85fc9209dba097cfc69cp-1) 
        + ((double)in_72)*(((double)0x1.9f1cd63f17e4027947547097909455ccp-16) 
        + ((double)in_72)*(((double)-0x1.558699661a1dd85ddf798909b72fff82p-3) 
        + ((double)in_72)*(((double)0x1.7ab23ed714b2c36137f8a1551b1391eap-13) 
        + ((double)in_72)*(((double)0x1.0a50a3b4f10a9929b286c04468d8dcd4p-7) 
        + ((double)in_72)*(((double)0x1.3fa5e1086c232ab5ff9c964b7c1a36b4p-13) 
        + ((double)in_72)*(((double)-0x1.20d46d62cdf54bf05c54545ee536cb02p-12) 
        + ((double)in_72)*(((double)0x1.cc61d2ae04a7785156eab4656554cb2p-16) 
        + ((double)in_72)*(((double)-0x1.1c68103b31cd98de17eb8e6730abab2p-18) 
        + ((double)in_72)*(((double)0x1.566628c148bf18d12de522f97a437164p-20) 
        + ((double)in_72)*(((double)-0x1.94985c0b84238863c6ad9188afaaaa3p-23) 
        + ((double)in_72)*(((double)0x1.de66bf7d5694e65da70a1f3b1ae5bdc8p-27) 
        + ((double)in_72)*(((double)-0x1.1d2579519a5af9410a02018b76343ceep-31) 
        + ((double)in_72)*((double)0x1.149deb9af0ead7baf05b6209f1faa2d4p-37)))))))))))))));
    double recons_18 = in_73 < 0.0 ? ((M_PI*4)-(out_30+(M_PI*4))) : out_30;
    return recons_18;
}

double my_core_function_sin_9(double in_77)
{
// (periodic (* PI 6) (MirrorLeft (/ (* 2 x) (- 2)) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))
    int k_25 = (int) floor((((double)in_77)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_76 = ((double)in_77) - k_25*((double)18.84955592153876);
    double in_75 = in_76 < 0.0 ? (0.0 - in_76) : in_76;
    double out_31 = (((double)in_75)*(((double)0x1.ffffb35d7bc85fc9209dba097cfc69cp-1) 
        + ((double)in_75)*(((double)0x1.9f1cd63f17e4027947547097909455ccp-16) 
        + ((double)in_75)*(((double)-0x1.558699661a1dd85ddf798909b72fff82p-3) 
        + ((double)in_75)*(((double)0x1.7ab23ed714b2c36137f8a1551b1391eap-13) 
        + ((double)in_75)*(((double)0x1.0a50a3b4f10a9929b286c04468d8dcd4p-7) 
        + ((double)in_75)*(((double)0x1.3fa5e1086c232ab5ff9c964b7c1a36b4p-13) 
        + ((double)in_75)*(((double)-0x1.20d46d62cdf54bf05c54545ee536cb02p-12) 
        + ((double)in_75)*(((double)0x1.cc61d2ae04a7785156eab4656554cb2p-16) 
        + ((double)in_75)*(((double)-0x1.1c68103b31cd98de17eb8e6730abab2p-18) 
        + ((double)in_75)*(((double)0x1.566628c148bf18d12de522f97a437164p-20) 
        + ((double)in_75)*(((double)-0x1.94985c0b84238863c6ad9188afaaaa3p-23) 
        + ((double)in_75)*(((double)0x1.de66bf7d5694e65da70a1f3b1ae5bdc8p-27) 
        + ((double)in_75)*(((double)-0x1.1d2579519a5af9410a02018b76343ceep-31) 
        + ((double)in_75)*((double)0x1.149deb9af0ead7baf05b6209f1faa2d4p-37)))))))))))))));
    double recons_19 = in_76 < 0.0 ? ((2*out_31)/(-2)) : out_31;
    return recons_19;
}

double my_core_function_sin_10(double in_80)
{
// (periodic (* PI 6) (MirrorLeft (+ (- (- (- (+ PI PI)) (- (* PI 4) x))) (- (* PI 6))) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))
    int k_26 = (int) floor((((double)in_80)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_79 = ((double)in_80) - k_26*((double)18.84955592153876);
    double in_78 = in_79 < 0.0 ? (0.0 - in_79) : in_79;
    double out_32 = (((double)in_78)*(((double)0x1.ffffb35d7bc85fc9209dba097cfc69cp-1) 
        + ((double)in_78)*(((double)0x1.9f1cd63f17e4027947547097909455ccp-16) 
        + ((double)in_78)*(((double)-0x1.558699661a1dd85ddf798909b72fff82p-3) 
        + ((double)in_78)*(((double)0x1.7ab23ed714b2c36137f8a1551b1391eap-13) 
        + ((double)in_78)*(((double)0x1.0a50a3b4f10a9929b286c04468d8dcd4p-7) 
        + ((double)in_78)*(((double)0x1.3fa5e1086c232ab5ff9c964b7c1a36b4p-13) 
        + ((double)in_78)*(((double)-0x1.20d46d62cdf54bf05c54545ee536cb02p-12) 
        + ((double)in_78)*(((double)0x1.cc61d2ae04a7785156eab4656554cb2p-16) 
        + ((double)in_78)*(((double)-0x1.1c68103b31cd98de17eb8e6730abab2p-18) 
        + ((double)in_78)*(((double)0x1.566628c148bf18d12de522f97a437164p-20) 
        + ((double)in_78)*(((double)-0x1.94985c0b84238863c6ad9188afaaaa3p-23) 
        + ((double)in_78)*(((double)0x1.de66bf7d5694e65da70a1f3b1ae5bdc8p-27) 
        + ((double)in_78)*(((double)-0x1.1d2579519a5af9410a02018b76343ceep-31) 
        + ((double)in_78)*((double)0x1.149deb9af0ead7baf05b6209f1faa2d4p-37)))))))))))))));
    double recons_20 = in_79 < 0.0 ? ((-((-(M_PI+M_PI))-((M_PI*4)-out_32)))+(-(M_PI*6))) : out_32;
    return recons_20;
}

double my_core_function_sin_11(double in_83)
{
// (periodic (* PI 6) (MirrorLeft (+ (- (- x 1)) (- 1)) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))
    int k_27 = (int) floor((((double)in_83)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_82 = ((double)in_83) - k_27*((double)18.84955592153876);
    double in_81 = in_82 < 0.0 ? (0.0 - in_82) : in_82;
    double out_33 = (((double)in_81)*(((double)0x1.ffffb35d7bc85fc9209dba097cfc69cp-1) 
        + ((double)in_81)*(((double)0x1.9f1cd63f17e4027947547097909455ccp-16) 
        + ((double)in_81)*(((double)-0x1.558699661a1dd85ddf798909b72fff82p-3) 
        + ((double)in_81)*(((double)0x1.7ab23ed714b2c36137f8a1551b1391eap-13) 
        + ((double)in_81)*(((double)0x1.0a50a3b4f10a9929b286c04468d8dcd4p-7) 
        + ((double)in_81)*(((double)0x1.3fa5e1086c232ab5ff9c964b7c1a36b4p-13) 
        + ((double)in_81)*(((double)-0x1.20d46d62cdf54bf05c54545ee536cb02p-12) 
        + ((double)in_81)*(((double)0x1.cc61d2ae04a7785156eab4656554cb2p-16) 
        + ((double)in_81)*(((double)-0x1.1c68103b31cd98de17eb8e6730abab2p-18) 
        + ((double)in_81)*(((double)0x1.566628c148bf18d12de522f97a437164p-20) 
        + ((double)in_81)*(((double)-0x1.94985c0b84238863c6ad9188afaaaa3p-23) 
        + ((double)in_81)*(((double)0x1.de66bf7d5694e65da70a1f3b1ae5bdc8p-27) 
        + ((double)in_81)*(((double)-0x1.1d2579519a5af9410a02018b76343ceep-31) 
        + ((double)in_81)*((double)0x1.149deb9af0ead7baf05b6209f1faa2d4p-37)))))))))))))));
    double recons_21 = in_82 < 0.0 ? ((-(out_33-1))+(-1)) : out_33;
    return recons_21;
}

double my_core_function_sin_12(double in_86)
{
// (periodic (* PI 6) (MirrorLeft (- (* PI 6) (+ (+ PI PI) (+ x (* PI 4)))) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))
    int k_28 = (int) floor((((double)in_86)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_85 = ((double)in_86) - k_28*((double)18.84955592153876);
    double in_84 = in_85 < 0.0 ? (0.0 - in_85) : in_85;
    double out_34 = (((double)in_84)*(((double)0x1.ffffb35d7bc85fc9209dba097cfc69cp-1) 
        + ((double)in_84)*(((double)0x1.9f1cd63f17e4027947547097909455ccp-16) 
        + ((double)in_84)*(((double)-0x1.558699661a1dd85ddf798909b72fff82p-3) 
        + ((double)in_84)*(((double)0x1.7ab23ed714b2c36137f8a1551b1391eap-13) 
        + ((double)in_84)*(((double)0x1.0a50a3b4f10a9929b286c04468d8dcd4p-7) 
        + ((double)in_84)*(((double)0x1.3fa5e1086c232ab5ff9c964b7c1a36b4p-13) 
        + ((double)in_84)*(((double)-0x1.20d46d62cdf54bf05c54545ee536cb02p-12) 
        + ((double)in_84)*(((double)0x1.cc61d2ae04a7785156eab4656554cb2p-16) 
        + ((double)in_84)*(((double)-0x1.1c68103b31cd98de17eb8e6730abab2p-18) 
        + ((double)in_84)*(((double)0x1.566628c148bf18d12de522f97a437164p-20) 
        + ((double)in_84)*(((double)-0x1.94985c0b84238863c6ad9188afaaaa3p-23) 
        + ((double)in_84)*(((double)0x1.de66bf7d5694e65da70a1f3b1ae5bdc8p-27) 
        + ((double)in_84)*(((double)-0x1.1d2579519a5af9410a02018b76343ceep-31) 
        + ((double)in_84)*((double)0x1.149deb9af0ead7baf05b6209f1faa2d4p-37)))))))))))))));
    double recons_22 = in_85 < 0.0 ? ((M_PI*6)-((M_PI+M_PI)+(out_34+(M_PI*4)))) : out_34;
    return recons_22;
}

double my_core_function_sin_13(double in_89)
{
// (periodic (* PI 6) (MirrorLeft (- (- (+ PI PI)) (- x (+ PI PI))) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))
    int k_29 = (int) floor((((double)in_89)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_88 = ((double)in_89) - k_29*((double)18.84955592153876);
    double in_87 = in_88 < 0.0 ? (0.0 - in_88) : in_88;
    double out_35 = (((double)in_87)*(((double)0x1.ffffb35d7bc85fc9209dba097cfc69cp-1) 
        + ((double)in_87)*(((double)0x1.9f1cd63f17e4027947547097909455ccp-16) 
        + ((double)in_87)*(((double)-0x1.558699661a1dd85ddf798909b72fff82p-3) 
        + ((double)in_87)*(((double)0x1.7ab23ed714b2c36137f8a1551b1391eap-13) 
        + ((double)in_87)*(((double)0x1.0a50a3b4f10a9929b286c04468d8dcd4p-7) 
        + ((double)in_87)*(((double)0x1.3fa5e1086c232ab5ff9c964b7c1a36b4p-13) 
        + ((double)in_87)*(((double)-0x1.20d46d62cdf54bf05c54545ee536cb02p-12) 
        + ((double)in_87)*(((double)0x1.cc61d2ae04a7785156eab4656554cb2p-16) 
        + ((double)in_87)*(((double)-0x1.1c68103b31cd98de17eb8e6730abab2p-18) 
        + ((double)in_87)*(((double)0x1.566628c148bf18d12de522f97a437164p-20) 
        + ((double)in_87)*(((double)-0x1.94985c0b84238863c6ad9188afaaaa3p-23) 
        + ((double)in_87)*(((double)0x1.de66bf7d5694e65da70a1f3b1ae5bdc8p-27) 
        + ((double)in_87)*(((double)-0x1.1d2579519a5af9410a02018b76343ceep-31) 
        + ((double)in_87)*((double)0x1.149deb9af0ead7baf05b6209f1faa2d4p-37)))))))))))))));
    double recons_23 = in_88 < 0.0 ? ((-(M_PI+M_PI))-(out_35-(M_PI+M_PI))) : out_35;
    return recons_23;
}

double my_core_function_sin_14(double in_92)
{
// (periodic (* PI 6) (MirrorLeft (* (* 2 x) (- (/ 1 2))) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))
    int k_30 = (int) floor((((double)in_92)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_91 = ((double)in_92) - k_30*((double)18.84955592153876);
    double in_90 = in_91 < 0.0 ? (0.0 - in_91) : in_91;
    double out_36 = (((double)in_90)*(((double)0x1.ffffb35d7bc85fc9209dba097cfc69cp-1) 
        + ((double)in_90)*(((double)0x1.9f1cd63f17e4027947547097909455ccp-16) 
        + ((double)in_90)*(((double)-0x1.558699661a1dd85ddf798909b72fff82p-3) 
        + ((double)in_90)*(((double)0x1.7ab23ed714b2c36137f8a1551b1391eap-13) 
        + ((double)in_90)*(((double)0x1.0a50a3b4f10a9929b286c04468d8dcd4p-7) 
        + ((double)in_90)*(((double)0x1.3fa5e1086c232ab5ff9c964b7c1a36b4p-13) 
        + ((double)in_90)*(((double)-0x1.20d46d62cdf54bf05c54545ee536cb02p-12) 
        + ((double)in_90)*(((double)0x1.cc61d2ae04a7785156eab4656554cb2p-16) 
        + ((double)in_90)*(((double)-0x1.1c68103b31cd98de17eb8e6730abab2p-18) 
        + ((double)in_90)*(((double)0x1.566628c148bf18d12de522f97a437164p-20) 
        + ((double)in_90)*(((double)-0x1.94985c0b84238863c6ad9188afaaaa3p-23) 
        + ((double)in_90)*(((double)0x1.de66bf7d5694e65da70a1f3b1ae5bdc8p-27) 
        + ((double)in_90)*(((double)-0x1.1d2579519a5af9410a02018b76343ceep-31) 
        + ((double)in_90)*((double)0x1.149deb9af0ead7baf05b6209f1faa2d4p-37)))))))))))))));
    double recons_24 = in_91 < 0.0 ? ((2*out_36)*(-(1/2))) : out_36;
    return recons_24;
}

double my_core_function_sin_15(double in_95)
{
// (periodic (* PI 6) (MirrorLeft (- x) (Horner (MinimaxPolynomial (sin x) [0 (* PI 3)]))))
    int k_31 = (int) floor((((double)in_95)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_94 = ((double)in_95) - k_31*((double)18.84955592153876);
    double in_93 = in_94 < 0.0 ? (0.0 - in_94) : in_94;
    double out_37 = (((double)in_93)*(((double)0x1.ffffb35d7bc85fc9209dba097cfc69cp-1) 
        + ((double)in_93)*(((double)0x1.9f1cd63f17e4027947547097909455ccp-16) 
        + ((double)in_93)*(((double)-0x1.558699661a1dd85ddf798909b72fff82p-3) 
        + ((double)in_93)*(((double)0x1.7ab23ed714b2c36137f8a1551b1391eap-13) 
        + ((double)in_93)*(((double)0x1.0a50a3b4f10a9929b286c04468d8dcd4p-7) 
        + ((double)in_93)*(((double)0x1.3fa5e1086c232ab5ff9c964b7c1a36b4p-13) 
        + ((double)in_93)*(((double)-0x1.20d46d62cdf54bf05c54545ee536cb02p-12) 
        + ((double)in_93)*(((double)0x1.cc61d2ae04a7785156eab4656554cb2p-16) 
        + ((double)in_93)*(((double)-0x1.1c68103b31cd98de17eb8e6730abab2p-18) 
        + ((double)in_93)*(((double)0x1.566628c148bf18d12de522f97a437164p-20) 
        + ((double)in_93)*(((double)-0x1.94985c0b84238863c6ad9188afaaaa3p-23) 
        + ((double)in_93)*(((double)0x1.de66bf7d5694e65da70a1f3b1ae5bdc8p-27) 
        + ((double)in_93)*(((double)-0x1.1d2579519a5af9410a02018b76343ceep-31) 
        + ((double)in_93)*((double)0x1.149deb9af0ead7baf05b6209f1faa2d4p-37)))))))))))))));
    double recons_25 = in_94 < 0.0 ? (-out_37) : out_37;
    return recons_25;
}

double my_core_function_sin_16(double in_98)
{
// (periodic (* PI 6) (MirrorRight (+ (- (- x 2)) (- 2)) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))
    int k_32 = (int) floor((((double)in_98)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_97 = ((double)in_98) - k_32*((double)18.84955592153876);
    double in_96 = in_97 < 0.0 ? in_97 : (0.0 - in_97);
    double out_38 = (((double)in_96)*(((double)0x1.ffffb35d7bc8634c38ea8a0ea5619fdep-1) 
        + ((double)in_96)*(((double)-0x1.9f1cd63f36fa25785a470b5b4229d342p-16) 
        + ((double)in_96)*(((double)-0x1.558699661a22a87a5c67612e020c0efep-3) 
        + ((double)in_96)*(((double)-0x1.7ab23ed73a03df7e643cb929c74b00cep-13) 
        + ((double)in_96)*(((double)0x1.0a50a3b4f06c651ee73643c73c8a06dp-7) 
        + ((double)in_96)*(((double)-0x1.3fa5e108860ed2c3a9f7a4a8ca05aa5ep-13) 
        + ((double)in_96)*(((double)-0x1.20d46d62d38f33aabfbbf176596ef2dp-12) 
        + ((double)in_96)*(((double)-0x1.cc61d2ae1f1fc02f41097a80cd4d6d24p-16) 
        + ((double)in_96)*(((double)-0x1.1c68103b4787e1f6a9951c9070f0a3aep-18) 
        + ((double)in_96)*(((double)-0x1.566628c15522d15b2a636f7f31ed2022p-20) 
        + ((double)in_96)*(((double)-0x1.94985c0b8dc4f3405d382047fbf56932p-23) 
        + ((double)in_96)*(((double)-0x1.de66bf7d6051097b57316a2c28dc990cp-27) 
        + ((double)in_96)*(((double)-0x1.1d257951a01fbf286e1e232a90f33ad6p-31) 
        + ((double)in_96)*((double)-0x1.149deb9af700032376984df4eaf67c82p-37)))))))))))))));
    double recons_26 = in_97 < 0.0 ? out_38 : ((-(out_38-2))+(-2));
    return recons_26;
}

double my_core_function_sin_17(double in_101)
{
// (periodic (* PI 6) (MirrorRight (- (+ (+ PI PI) (- (* PI 4) x)) (* PI 6)) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))
    int k_33 = (int) floor((((double)in_101)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_100 = ((double)in_101) - k_33*((double)18.84955592153876);
    double in_99 = in_100 < 0.0 ? in_100 : (0.0 - in_100);
    double out_39 = (((double)in_99)*(((double)0x1.ffffb35d7bc8634c38ea8a0ea5619fdep-1) 
        + ((double)in_99)*(((double)-0x1.9f1cd63f36fa25785a470b5b4229d342p-16) 
        + ((double)in_99)*(((double)-0x1.558699661a22a87a5c67612e020c0efep-3) 
        + ((double)in_99)*(((double)-0x1.7ab23ed73a03df7e643cb929c74b00cep-13) 
        + ((double)in_99)*(((double)0x1.0a50a3b4f06c651ee73643c73c8a06dp-7) 
        + ((double)in_99)*(((double)-0x1.3fa5e108860ed2c3a9f7a4a8ca05aa5ep-13) 
        + ((double)in_99)*(((double)-0x1.20d46d62d38f33aabfbbf176596ef2dp-12) 
        + ((double)in_99)*(((double)-0x1.cc61d2ae1f1fc02f41097a80cd4d6d24p-16) 
        + ((double)in_99)*(((double)-0x1.1c68103b4787e1f6a9951c9070f0a3aep-18) 
        + ((double)in_99)*(((double)-0x1.566628c15522d15b2a636f7f31ed2022p-20) 
        + ((double)in_99)*(((double)-0x1.94985c0b8dc4f3405d382047fbf56932p-23) 
        + ((double)in_99)*(((double)-0x1.de66bf7d6051097b57316a2c28dc990cp-27) 
        + ((double)in_99)*(((double)-0x1.1d257951a01fbf286e1e232a90f33ad6p-31) 
        + ((double)in_99)*((double)-0x1.149deb9af700032376984df4eaf67c82p-37)))))))))))))));
    double recons_27 = in_100 < 0.0 ? out_39 : (((M_PI+M_PI)+((M_PI*4)-out_39))-(M_PI*6));
    return recons_27;
}

double my_core_function_sin_18(double in_104)
{
// (periodic (* PI 6) (MirrorRight (- (* PI 4) (+ x (* PI 4))) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))
    int k_34 = (int) floor((((double)in_104)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_103 = ((double)in_104) - k_34*((double)18.84955592153876);
    double in_102 = in_103 < 0.0 ? in_103 : (0.0 - in_103);
    double out_40 = (((double)in_102)*(((double)0x1.ffffb35d7bc8634c38ea8a0ea5619fdep-1) 
        + ((double)in_102)*(((double)-0x1.9f1cd63f36fa25785a470b5b4229d342p-16) 
        + ((double)in_102)*(((double)-0x1.558699661a22a87a5c67612e020c0efep-3) 
        + ((double)in_102)*(((double)-0x1.7ab23ed73a03df7e643cb929c74b00cep-13) 
        + ((double)in_102)*(((double)0x1.0a50a3b4f06c651ee73643c73c8a06dp-7) 
        + ((double)in_102)*(((double)-0x1.3fa5e108860ed2c3a9f7a4a8ca05aa5ep-13) 
        + ((double)in_102)*(((double)-0x1.20d46d62d38f33aabfbbf176596ef2dp-12) 
        + ((double)in_102)*(((double)-0x1.cc61d2ae1f1fc02f41097a80cd4d6d24p-16) 
        + ((double)in_102)*(((double)-0x1.1c68103b4787e1f6a9951c9070f0a3aep-18) 
        + ((double)in_102)*(((double)-0x1.566628c15522d15b2a636f7f31ed2022p-20) 
        + ((double)in_102)*(((double)-0x1.94985c0b8dc4f3405d382047fbf56932p-23) 
        + ((double)in_102)*(((double)-0x1.de66bf7d6051097b57316a2c28dc990cp-27) 
        + ((double)in_102)*(((double)-0x1.1d257951a01fbf286e1e232a90f33ad6p-31) 
        + ((double)in_102)*((double)-0x1.149deb9af700032376984df4eaf67c82p-37)))))))))))))));
    double recons_28 = in_103 < 0.0 ? out_40 : ((M_PI*4)-(out_40+(M_PI*4)));
    return recons_28;
}

double my_core_function_sin_19(double in_107)
{
// (periodic (* PI 6) (MirrorRight (/ (* 2 x) (- 2)) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))
    int k_35 = (int) floor((((double)in_107)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_106 = ((double)in_107) - k_35*((double)18.84955592153876);
    double in_105 = in_106 < 0.0 ? in_106 : (0.0 - in_106);
    double out_41 = (((double)in_105)*(((double)0x1.ffffb35d7bc8634c38ea8a0ea5619fdep-1) 
        + ((double)in_105)*(((double)-0x1.9f1cd63f36fa25785a470b5b4229d342p-16) 
        + ((double)in_105)*(((double)-0x1.558699661a22a87a5c67612e020c0efep-3) 
        + ((double)in_105)*(((double)-0x1.7ab23ed73a03df7e643cb929c74b00cep-13) 
        + ((double)in_105)*(((double)0x1.0a50a3b4f06c651ee73643c73c8a06dp-7) 
        + ((double)in_105)*(((double)-0x1.3fa5e108860ed2c3a9f7a4a8ca05aa5ep-13) 
        + ((double)in_105)*(((double)-0x1.20d46d62d38f33aabfbbf176596ef2dp-12) 
        + ((double)in_105)*(((double)-0x1.cc61d2ae1f1fc02f41097a80cd4d6d24p-16) 
        + ((double)in_105)*(((double)-0x1.1c68103b4787e1f6a9951c9070f0a3aep-18) 
        + ((double)in_105)*(((double)-0x1.566628c15522d15b2a636f7f31ed2022p-20) 
        + ((double)in_105)*(((double)-0x1.94985c0b8dc4f3405d382047fbf56932p-23) 
        + ((double)in_105)*(((double)-0x1.de66bf7d6051097b57316a2c28dc990cp-27) 
        + ((double)in_105)*(((double)-0x1.1d257951a01fbf286e1e232a90f33ad6p-31) 
        + ((double)in_105)*((double)-0x1.149deb9af700032376984df4eaf67c82p-37)))))))))))))));
    double recons_29 = in_106 < 0.0 ? out_41 : ((2*out_41)/(-2));
    return recons_29;
}

double my_core_function_sin_20(double in_110)
{
// (periodic (* PI 6) (MirrorRight (+ (- (- (- (+ PI PI)) (- (* PI 4) x))) (- (* PI 6))) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))
    int k_36 = (int) floor((((double)in_110)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_109 = ((double)in_110) - k_36*((double)18.84955592153876);
    double in_108 = in_109 < 0.0 ? in_109 : (0.0 - in_109);
    double out_42 = (((double)in_108)*(((double)0x1.ffffb35d7bc8634c38ea8a0ea5619fdep-1) 
        + ((double)in_108)*(((double)-0x1.9f1cd63f36fa25785a470b5b4229d342p-16) 
        + ((double)in_108)*(((double)-0x1.558699661a22a87a5c67612e020c0efep-3) 
        + ((double)in_108)*(((double)-0x1.7ab23ed73a03df7e643cb929c74b00cep-13) 
        + ((double)in_108)*(((double)0x1.0a50a3b4f06c651ee73643c73c8a06dp-7) 
        + ((double)in_108)*(((double)-0x1.3fa5e108860ed2c3a9f7a4a8ca05aa5ep-13) 
        + ((double)in_108)*(((double)-0x1.20d46d62d38f33aabfbbf176596ef2dp-12) 
        + ((double)in_108)*(((double)-0x1.cc61d2ae1f1fc02f41097a80cd4d6d24p-16) 
        + ((double)in_108)*(((double)-0x1.1c68103b4787e1f6a9951c9070f0a3aep-18) 
        + ((double)in_108)*(((double)-0x1.566628c15522d15b2a636f7f31ed2022p-20) 
        + ((double)in_108)*(((double)-0x1.94985c0b8dc4f3405d382047fbf56932p-23) 
        + ((double)in_108)*(((double)-0x1.de66bf7d6051097b57316a2c28dc990cp-27) 
        + ((double)in_108)*(((double)-0x1.1d257951a01fbf286e1e232a90f33ad6p-31) 
        + ((double)in_108)*((double)-0x1.149deb9af700032376984df4eaf67c82p-37)))))))))))))));
    double recons_30 = in_109 < 0.0 ? out_42 : ((-((-(M_PI+M_PI))-((M_PI*4)-out_42)))+(-(M_PI*6)));
    return recons_30;
}

double my_core_function_sin_21(double in_113)
{
// (periodic (* PI 6) (MirrorRight (+ (- (- x 1)) (- 1)) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))
    int k_37 = (int) floor((((double)in_113)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_112 = ((double)in_113) - k_37*((double)18.84955592153876);
    double in_111 = in_112 < 0.0 ? in_112 : (0.0 - in_112);
    double out_43 = (((double)in_111)*(((double)0x1.ffffb35d7bc8634c38ea8a0ea5619fdep-1) 
        + ((double)in_111)*(((double)-0x1.9f1cd63f36fa25785a470b5b4229d342p-16) 
        + ((double)in_111)*(((double)-0x1.558699661a22a87a5c67612e020c0efep-3) 
        + ((double)in_111)*(((double)-0x1.7ab23ed73a03df7e643cb929c74b00cep-13) 
        + ((double)in_111)*(((double)0x1.0a50a3b4f06c651ee73643c73c8a06dp-7) 
        + ((double)in_111)*(((double)-0x1.3fa5e108860ed2c3a9f7a4a8ca05aa5ep-13) 
        + ((double)in_111)*(((double)-0x1.20d46d62d38f33aabfbbf176596ef2dp-12) 
        + ((double)in_111)*(((double)-0x1.cc61d2ae1f1fc02f41097a80cd4d6d24p-16) 
        + ((double)in_111)*(((double)-0x1.1c68103b4787e1f6a9951c9070f0a3aep-18) 
        + ((double)in_111)*(((double)-0x1.566628c15522d15b2a636f7f31ed2022p-20) 
        + ((double)in_111)*(((double)-0x1.94985c0b8dc4f3405d382047fbf56932p-23) 
        + ((double)in_111)*(((double)-0x1.de66bf7d6051097b57316a2c28dc990cp-27) 
        + ((double)in_111)*(((double)-0x1.1d257951a01fbf286e1e232a90f33ad6p-31) 
        + ((double)in_111)*((double)-0x1.149deb9af700032376984df4eaf67c82p-37)))))))))))))));
    double recons_31 = in_112 < 0.0 ? out_43 : ((-(out_43-1))+(-1));
    return recons_31;
}

double my_core_function_sin_22(double in_116)
{
// (periodic (* PI 6) (MirrorRight (- (* PI 6) (+ (+ PI PI) (+ x (* PI 4)))) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))
    int k_38 = (int) floor((((double)in_116)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_115 = ((double)in_116) - k_38*((double)18.84955592153876);
    double in_114 = in_115 < 0.0 ? in_115 : (0.0 - in_115);
    double out_44 = (((double)in_114)*(((double)0x1.ffffb35d7bc8634c38ea8a0ea5619fdep-1) 
        + ((double)in_114)*(((double)-0x1.9f1cd63f36fa25785a470b5b4229d342p-16) 
        + ((double)in_114)*(((double)-0x1.558699661a22a87a5c67612e020c0efep-3) 
        + ((double)in_114)*(((double)-0x1.7ab23ed73a03df7e643cb929c74b00cep-13) 
        + ((double)in_114)*(((double)0x1.0a50a3b4f06c651ee73643c73c8a06dp-7) 
        + ((double)in_114)*(((double)-0x1.3fa5e108860ed2c3a9f7a4a8ca05aa5ep-13) 
        + ((double)in_114)*(((double)-0x1.20d46d62d38f33aabfbbf176596ef2dp-12) 
        + ((double)in_114)*(((double)-0x1.cc61d2ae1f1fc02f41097a80cd4d6d24p-16) 
        + ((double)in_114)*(((double)-0x1.1c68103b4787e1f6a9951c9070f0a3aep-18) 
        + ((double)in_114)*(((double)-0x1.566628c15522d15b2a636f7f31ed2022p-20) 
        + ((double)in_114)*(((double)-0x1.94985c0b8dc4f3405d382047fbf56932p-23) 
        + ((double)in_114)*(((double)-0x1.de66bf7d6051097b57316a2c28dc990cp-27) 
        + ((double)in_114)*(((double)-0x1.1d257951a01fbf286e1e232a90f33ad6p-31) 
        + ((double)in_114)*((double)-0x1.149deb9af700032376984df4eaf67c82p-37)))))))))))))));
    double recons_32 = in_115 < 0.0 ? out_44 : ((M_PI*6)-((M_PI+M_PI)+(out_44+(M_PI*4))));
    return recons_32;
}

double my_core_function_sin_23(double in_119)
{
// (periodic (* PI 6) (MirrorRight (- (- (+ PI PI)) (- x (+ PI PI))) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))
    int k_39 = (int) floor((((double)in_119)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_118 = ((double)in_119) - k_39*((double)18.84955592153876);
    double in_117 = in_118 < 0.0 ? in_118 : (0.0 - in_118);
    double out_45 = (((double)in_117)*(((double)0x1.ffffb35d7bc8634c38ea8a0ea5619fdep-1) 
        + ((double)in_117)*(((double)-0x1.9f1cd63f36fa25785a470b5b4229d342p-16) 
        + ((double)in_117)*(((double)-0x1.558699661a22a87a5c67612e020c0efep-3) 
        + ((double)in_117)*(((double)-0x1.7ab23ed73a03df7e643cb929c74b00cep-13) 
        + ((double)in_117)*(((double)0x1.0a50a3b4f06c651ee73643c73c8a06dp-7) 
        + ((double)in_117)*(((double)-0x1.3fa5e108860ed2c3a9f7a4a8ca05aa5ep-13) 
        + ((double)in_117)*(((double)-0x1.20d46d62d38f33aabfbbf176596ef2dp-12) 
        + ((double)in_117)*(((double)-0x1.cc61d2ae1f1fc02f41097a80cd4d6d24p-16) 
        + ((double)in_117)*(((double)-0x1.1c68103b4787e1f6a9951c9070f0a3aep-18) 
        + ((double)in_117)*(((double)-0x1.566628c15522d15b2a636f7f31ed2022p-20) 
        + ((double)in_117)*(((double)-0x1.94985c0b8dc4f3405d382047fbf56932p-23) 
        + ((double)in_117)*(((double)-0x1.de66bf7d6051097b57316a2c28dc990cp-27) 
        + ((double)in_117)*(((double)-0x1.1d257951a01fbf286e1e232a90f33ad6p-31) 
        + ((double)in_117)*((double)-0x1.149deb9af700032376984df4eaf67c82p-37)))))))))))))));
    double recons_33 = in_118 < 0.0 ? out_45 : ((-(M_PI+M_PI))-(out_45-(M_PI+M_PI)));
    return recons_33;
}

double my_core_function_sin_24(double in_122)
{
// (periodic (* PI 6) (MirrorRight (* (* 2 x) (- (/ 1 2))) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))
    int k_40 = (int) floor((((double)in_122)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_121 = ((double)in_122) - k_40*((double)18.84955592153876);
    double in_120 = in_121 < 0.0 ? in_121 : (0.0 - in_121);
    double out_46 = (((double)in_120)*(((double)0x1.ffffb35d7bc8634c38ea8a0ea5619fdep-1) 
        + ((double)in_120)*(((double)-0x1.9f1cd63f36fa25785a470b5b4229d342p-16) 
        + ((double)in_120)*(((double)-0x1.558699661a22a87a5c67612e020c0efep-3) 
        + ((double)in_120)*(((double)-0x1.7ab23ed73a03df7e643cb929c74b00cep-13) 
        + ((double)in_120)*(((double)0x1.0a50a3b4f06c651ee73643c73c8a06dp-7) 
        + ((double)in_120)*(((double)-0x1.3fa5e108860ed2c3a9f7a4a8ca05aa5ep-13) 
        + ((double)in_120)*(((double)-0x1.20d46d62d38f33aabfbbf176596ef2dp-12) 
        + ((double)in_120)*(((double)-0x1.cc61d2ae1f1fc02f41097a80cd4d6d24p-16) 
        + ((double)in_120)*(((double)-0x1.1c68103b4787e1f6a9951c9070f0a3aep-18) 
        + ((double)in_120)*(((double)-0x1.566628c15522d15b2a636f7f31ed2022p-20) 
        + ((double)in_120)*(((double)-0x1.94985c0b8dc4f3405d382047fbf56932p-23) 
        + ((double)in_120)*(((double)-0x1.de66bf7d6051097b57316a2c28dc990cp-27) 
        + ((double)in_120)*(((double)-0x1.1d257951a01fbf286e1e232a90f33ad6p-31) 
        + ((double)in_120)*((double)-0x1.149deb9af700032376984df4eaf67c82p-37)))))))))))))));
    double recons_34 = in_121 < 0.0 ? out_46 : ((2*out_46)*(-(1/2)));
    return recons_34;
}

double my_core_function_sin_25(double in_125)
{
// (periodic (* PI 6) (MirrorRight (- x) (Horner (MinimaxPolynomial (sin x) [(- (* PI 3)) 0]))))
    int k_41 = (int) floor((((double)in_125)-((double)-9.42477796076938))*((double)0.05305164769729845));
    double in_124 = ((double)in_125) - k_41*((double)18.84955592153876);
    double in_123 = in_124 < 0.0 ? in_124 : (0.0 - in_124);
    double out_47 = (((double)in_123)*(((double)0x1.ffffb35d7bc8634c38ea8a0ea5619fdep-1) 
        + ((double)in_123)*(((double)-0x1.9f1cd63f36fa25785a470b5b4229d342p-16) 
        + ((double)in_123)*(((double)-0x1.558699661a22a87a5c67612e020c0efep-3) 
        + ((double)in_123)*(((double)-0x1.7ab23ed73a03df7e643cb929c74b00cep-13) 
        + ((double)in_123)*(((double)0x1.0a50a3b4f06c651ee73643c73c8a06dp-7) 
        + ((double)in_123)*(((double)-0x1.3fa5e108860ed2c3a9f7a4a8ca05aa5ep-13) 
        + ((double)in_123)*(((double)-0x1.20d46d62d38f33aabfbbf176596ef2dp-12) 
        + ((double)in_123)*(((double)-0x1.cc61d2ae1f1fc02f41097a80cd4d6d24p-16) 
        + ((double)in_123)*(((double)-0x1.1c68103b4787e1f6a9951c9070f0a3aep-18) 
        + ((double)in_123)*(((double)-0x1.566628c15522d15b2a636f7f31ed2022p-20) 
        + ((double)in_123)*(((double)-0x1.94985c0b8dc4f3405d382047fbf56932p-23) 
        + ((double)in_123)*(((double)-0x1.de66bf7d6051097b57316a2c28dc990cp-27) 
        + ((double)in_123)*(((double)-0x1.1d257951a01fbf286e1e232a90f33ad6p-31) 
        + ((double)in_123)*((double)-0x1.149deb9af700032376984df4eaf67c82p-37)))))))))))))));
    double recons_35 = in_124 < 0.0 ? out_47 : (-out_47);
    return recons_35;
}

double my_core_function_sin_26(double in_128)
{
// (periodic (* PI 4) (MirrorLeft (+ (- (- x 2)) (- 2)) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))
    int k_42 = (int) floor((((double)in_128)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_127 = ((double)in_128) - k_42*((double)12.566370614359172);
    double in_126 = in_127 < 0.0 ? (0.0 - in_127) : in_127;
    double out_48 = (((double)in_126)*(((double)0x1.fffffe2f8a0046652e2bfaa63bbbd214p-1) 
        + ((double)in_126)*(((double)0x1.a12d9703db57edc2478240add6f8302ap-21) 
        + ((double)in_126)*(((double)-0x1.55576219c1a5ba1b0e311b4034036286p-3) 
        + ((double)in_126)*(((double)0x1.4d4a9f3a92460453f452b2a6388522fcp-17) 
        + ((double)in_126)*(((double)0x1.1093c69f4d261306e7ca5c9423717a3cp-7) 
        + ((double)in_126)*(((double)0x1.e672d75c0494c66f1874c22b687387dep-17) 
        + ((double)in_126)*(((double)-0x1.b42652015f5d05c3193bcaeafce74fc6p-13) 
        + ((double)in_126)*(((double)0x1.27ee727c4e19da9d7a927f7d444efa62p-18) 
        + ((double)in_126)*(((double)0x1.60d9bf29b135881f577b2775d02bd8fcp-20) 
        + ((double)in_126)*(((double)0x1.653184dae8e937829eb7cbcbb2690098p-22) 
        + ((double)in_126)*(((double)-0x1.4ec2a0c2fc99a4e7e062a9252573f7e6p-24) 
        + ((double)in_126)*(((double)0x1.74344215a0c4a4832b8a548b3baa1f08p-28) 
        + ((double)in_126)*(((double)-0x1.1f75197e8def097c835edf2cc2351af2p-33) 
        + ((double)in_126)*((double)-0x1.777b24606dd83bb52a5e865a2a7f7292p-44)))))))))))))));
    double recons_36 = in_127 < 0.0 ? ((-(out_48-2))+(-2)) : out_48;
    return recons_36;
}

double my_core_function_sin_27(double in_131)
{
// (periodic (* PI 4) (MirrorLeft (- (+ (+ PI PI) (- (* PI 4) x)) (* PI 6)) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))
    int k_43 = (int) floor((((double)in_131)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_130 = ((double)in_131) - k_43*((double)12.566370614359172);
    double in_129 = in_130 < 0.0 ? (0.0 - in_130) : in_130;
    double out_49 = (((double)in_129)*(((double)0x1.fffffe2f8a0046652e2bfaa63bbbd214p-1) 
        + ((double)in_129)*(((double)0x1.a12d9703db57edc2478240add6f8302ap-21) 
        + ((double)in_129)*(((double)-0x1.55576219c1a5ba1b0e311b4034036286p-3) 
        + ((double)in_129)*(((double)0x1.4d4a9f3a92460453f452b2a6388522fcp-17) 
        + ((double)in_129)*(((double)0x1.1093c69f4d261306e7ca5c9423717a3cp-7) 
        + ((double)in_129)*(((double)0x1.e672d75c0494c66f1874c22b687387dep-17) 
        + ((double)in_129)*(((double)-0x1.b42652015f5d05c3193bcaeafce74fc6p-13) 
        + ((double)in_129)*(((double)0x1.27ee727c4e19da9d7a927f7d444efa62p-18) 
        + ((double)in_129)*(((double)0x1.60d9bf29b135881f577b2775d02bd8fcp-20) 
        + ((double)in_129)*(((double)0x1.653184dae8e937829eb7cbcbb2690098p-22) 
        + ((double)in_129)*(((double)-0x1.4ec2a0c2fc99a4e7e062a9252573f7e6p-24) 
        + ((double)in_129)*(((double)0x1.74344215a0c4a4832b8a548b3baa1f08p-28) 
        + ((double)in_129)*(((double)-0x1.1f75197e8def097c835edf2cc2351af2p-33) 
        + ((double)in_129)*((double)-0x1.777b24606dd83bb52a5e865a2a7f7292p-44)))))))))))))));
    double recons_37 = in_130 < 0.0 ? (((M_PI+M_PI)+((M_PI*4)-out_49))-(M_PI*6)) : out_49;
    return recons_37;
}

double my_core_function_sin_28(double in_134)
{
// (periodic (* PI 4) (MirrorLeft (- (* PI 4) (+ x (* PI 4))) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))
    int k_44 = (int) floor((((double)in_134)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_133 = ((double)in_134) - k_44*((double)12.566370614359172);
    double in_132 = in_133 < 0.0 ? (0.0 - in_133) : in_133;
    double out_50 = (((double)in_132)*(((double)0x1.fffffe2f8a0046652e2bfaa63bbbd214p-1) 
        + ((double)in_132)*(((double)0x1.a12d9703db57edc2478240add6f8302ap-21) 
        + ((double)in_132)*(((double)-0x1.55576219c1a5ba1b0e311b4034036286p-3) 
        + ((double)in_132)*(((double)0x1.4d4a9f3a92460453f452b2a6388522fcp-17) 
        + ((double)in_132)*(((double)0x1.1093c69f4d261306e7ca5c9423717a3cp-7) 
        + ((double)in_132)*(((double)0x1.e672d75c0494c66f1874c22b687387dep-17) 
        + ((double)in_132)*(((double)-0x1.b42652015f5d05c3193bcaeafce74fc6p-13) 
        + ((double)in_132)*(((double)0x1.27ee727c4e19da9d7a927f7d444efa62p-18) 
        + ((double)in_132)*(((double)0x1.60d9bf29b135881f577b2775d02bd8fcp-20) 
        + ((double)in_132)*(((double)0x1.653184dae8e937829eb7cbcbb2690098p-22) 
        + ((double)in_132)*(((double)-0x1.4ec2a0c2fc99a4e7e062a9252573f7e6p-24) 
        + ((double)in_132)*(((double)0x1.74344215a0c4a4832b8a548b3baa1f08p-28) 
        + ((double)in_132)*(((double)-0x1.1f75197e8def097c835edf2cc2351af2p-33) 
        + ((double)in_132)*((double)-0x1.777b24606dd83bb52a5e865a2a7f7292p-44)))))))))))))));
    double recons_38 = in_133 < 0.0 ? ((M_PI*4)-(out_50+(M_PI*4))) : out_50;
    return recons_38;
}

double my_core_function_sin_29(double in_137)
{
// (periodic (* PI 4) (MirrorLeft (/ (* 2 x) (- 2)) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))
    int k_45 = (int) floor((((double)in_137)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_136 = ((double)in_137) - k_45*((double)12.566370614359172);
    double in_135 = in_136 < 0.0 ? (0.0 - in_136) : in_136;
    double out_51 = (((double)in_135)*(((double)0x1.fffffe2f8a0046652e2bfaa63bbbd214p-1) 
        + ((double)in_135)*(((double)0x1.a12d9703db57edc2478240add6f8302ap-21) 
        + ((double)in_135)*(((double)-0x1.55576219c1a5ba1b0e311b4034036286p-3) 
        + ((double)in_135)*(((double)0x1.4d4a9f3a92460453f452b2a6388522fcp-17) 
        + ((double)in_135)*(((double)0x1.1093c69f4d261306e7ca5c9423717a3cp-7) 
        + ((double)in_135)*(((double)0x1.e672d75c0494c66f1874c22b687387dep-17) 
        + ((double)in_135)*(((double)-0x1.b42652015f5d05c3193bcaeafce74fc6p-13) 
        + ((double)in_135)*(((double)0x1.27ee727c4e19da9d7a927f7d444efa62p-18) 
        + ((double)in_135)*(((double)0x1.60d9bf29b135881f577b2775d02bd8fcp-20) 
        + ((double)in_135)*(((double)0x1.653184dae8e937829eb7cbcbb2690098p-22) 
        + ((double)in_135)*(((double)-0x1.4ec2a0c2fc99a4e7e062a9252573f7e6p-24) 
        + ((double)in_135)*(((double)0x1.74344215a0c4a4832b8a548b3baa1f08p-28) 
        + ((double)in_135)*(((double)-0x1.1f75197e8def097c835edf2cc2351af2p-33) 
        + ((double)in_135)*((double)-0x1.777b24606dd83bb52a5e865a2a7f7292p-44)))))))))))))));
    double recons_39 = in_136 < 0.0 ? ((2*out_51)/(-2)) : out_51;
    return recons_39;
}

double my_core_function_sin_30(double in_140)
{
// (periodic (* PI 4) (MirrorLeft (+ (- (- (- (+ PI PI)) (- (* PI 4) x))) (- (* PI 6))) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))
    int k_46 = (int) floor((((double)in_140)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_139 = ((double)in_140) - k_46*((double)12.566370614359172);
    double in_138 = in_139 < 0.0 ? (0.0 - in_139) : in_139;
    double out_52 = (((double)in_138)*(((double)0x1.fffffe2f8a0046652e2bfaa63bbbd214p-1) 
        + ((double)in_138)*(((double)0x1.a12d9703db57edc2478240add6f8302ap-21) 
        + ((double)in_138)*(((double)-0x1.55576219c1a5ba1b0e311b4034036286p-3) 
        + ((double)in_138)*(((double)0x1.4d4a9f3a92460453f452b2a6388522fcp-17) 
        + ((double)in_138)*(((double)0x1.1093c69f4d261306e7ca5c9423717a3cp-7) 
        + ((double)in_138)*(((double)0x1.e672d75c0494c66f1874c22b687387dep-17) 
        + ((double)in_138)*(((double)-0x1.b42652015f5d05c3193bcaeafce74fc6p-13) 
        + ((double)in_138)*(((double)0x1.27ee727c4e19da9d7a927f7d444efa62p-18) 
        + ((double)in_138)*(((double)0x1.60d9bf29b135881f577b2775d02bd8fcp-20) 
        + ((double)in_138)*(((double)0x1.653184dae8e937829eb7cbcbb2690098p-22) 
        + ((double)in_138)*(((double)-0x1.4ec2a0c2fc99a4e7e062a9252573f7e6p-24) 
        + ((double)in_138)*(((double)0x1.74344215a0c4a4832b8a548b3baa1f08p-28) 
        + ((double)in_138)*(((double)-0x1.1f75197e8def097c835edf2cc2351af2p-33) 
        + ((double)in_138)*((double)-0x1.777b24606dd83bb52a5e865a2a7f7292p-44)))))))))))))));
    double recons_40 = in_139 < 0.0 ? ((-((-(M_PI+M_PI))-((M_PI*4)-out_52)))+(-(M_PI*6))) : out_52;
    return recons_40;
}

double my_core_function_sin_31(double in_143)
{
// (periodic (* PI 4) (MirrorLeft (+ (- (- x 1)) (- 1)) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))
    int k_47 = (int) floor((((double)in_143)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_142 = ((double)in_143) - k_47*((double)12.566370614359172);
    double in_141 = in_142 < 0.0 ? (0.0 - in_142) : in_142;
    double out_53 = (((double)in_141)*(((double)0x1.fffffe2f8a0046652e2bfaa63bbbd214p-1) 
        + ((double)in_141)*(((double)0x1.a12d9703db57edc2478240add6f8302ap-21) 
        + ((double)in_141)*(((double)-0x1.55576219c1a5ba1b0e311b4034036286p-3) 
        + ((double)in_141)*(((double)0x1.4d4a9f3a92460453f452b2a6388522fcp-17) 
        + ((double)in_141)*(((double)0x1.1093c69f4d261306e7ca5c9423717a3cp-7) 
        + ((double)in_141)*(((double)0x1.e672d75c0494c66f1874c22b687387dep-17) 
        + ((double)in_141)*(((double)-0x1.b42652015f5d05c3193bcaeafce74fc6p-13) 
        + ((double)in_141)*(((double)0x1.27ee727c4e19da9d7a927f7d444efa62p-18) 
        + ((double)in_141)*(((double)0x1.60d9bf29b135881f577b2775d02bd8fcp-20) 
        + ((double)in_141)*(((double)0x1.653184dae8e937829eb7cbcbb2690098p-22) 
        + ((double)in_141)*(((double)-0x1.4ec2a0c2fc99a4e7e062a9252573f7e6p-24) 
        + ((double)in_141)*(((double)0x1.74344215a0c4a4832b8a548b3baa1f08p-28) 
        + ((double)in_141)*(((double)-0x1.1f75197e8def097c835edf2cc2351af2p-33) 
        + ((double)in_141)*((double)-0x1.777b24606dd83bb52a5e865a2a7f7292p-44)))))))))))))));
    double recons_41 = in_142 < 0.0 ? ((-(out_53-1))+(-1)) : out_53;
    return recons_41;
}

double my_core_function_sin_32(double in_146)
{
// (periodic (* PI 4) (MirrorLeft (- (* PI 6) (+ (+ PI PI) (+ x (* PI 4)))) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))
    int k_48 = (int) floor((((double)in_146)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_145 = ((double)in_146) - k_48*((double)12.566370614359172);
    double in_144 = in_145 < 0.0 ? (0.0 - in_145) : in_145;
    double out_54 = (((double)in_144)*(((double)0x1.fffffe2f8a0046652e2bfaa63bbbd214p-1) 
        + ((double)in_144)*(((double)0x1.a12d9703db57edc2478240add6f8302ap-21) 
        + ((double)in_144)*(((double)-0x1.55576219c1a5ba1b0e311b4034036286p-3) 
        + ((double)in_144)*(((double)0x1.4d4a9f3a92460453f452b2a6388522fcp-17) 
        + ((double)in_144)*(((double)0x1.1093c69f4d261306e7ca5c9423717a3cp-7) 
        + ((double)in_144)*(((double)0x1.e672d75c0494c66f1874c22b687387dep-17) 
        + ((double)in_144)*(((double)-0x1.b42652015f5d05c3193bcaeafce74fc6p-13) 
        + ((double)in_144)*(((double)0x1.27ee727c4e19da9d7a927f7d444efa62p-18) 
        + ((double)in_144)*(((double)0x1.60d9bf29b135881f577b2775d02bd8fcp-20) 
        + ((double)in_144)*(((double)0x1.653184dae8e937829eb7cbcbb2690098p-22) 
        + ((double)in_144)*(((double)-0x1.4ec2a0c2fc99a4e7e062a9252573f7e6p-24) 
        + ((double)in_144)*(((double)0x1.74344215a0c4a4832b8a548b3baa1f08p-28) 
        + ((double)in_144)*(((double)-0x1.1f75197e8def097c835edf2cc2351af2p-33) 
        + ((double)in_144)*((double)-0x1.777b24606dd83bb52a5e865a2a7f7292p-44)))))))))))))));
    double recons_42 = in_145 < 0.0 ? ((M_PI*6)-((M_PI+M_PI)+(out_54+(M_PI*4)))) : out_54;
    return recons_42;
}

double my_core_function_sin_33(double in_149)
{
// (periodic (* PI 4) (MirrorLeft (- (- (+ PI PI)) (- x (+ PI PI))) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))
    int k_49 = (int) floor((((double)in_149)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_148 = ((double)in_149) - k_49*((double)12.566370614359172);
    double in_147 = in_148 < 0.0 ? (0.0 - in_148) : in_148;
    double out_55 = (((double)in_147)*(((double)0x1.fffffe2f8a0046652e2bfaa63bbbd214p-1) 
        + ((double)in_147)*(((double)0x1.a12d9703db57edc2478240add6f8302ap-21) 
        + ((double)in_147)*(((double)-0x1.55576219c1a5ba1b0e311b4034036286p-3) 
        + ((double)in_147)*(((double)0x1.4d4a9f3a92460453f452b2a6388522fcp-17) 
        + ((double)in_147)*(((double)0x1.1093c69f4d261306e7ca5c9423717a3cp-7) 
        + ((double)in_147)*(((double)0x1.e672d75c0494c66f1874c22b687387dep-17) 
        + ((double)in_147)*(((double)-0x1.b42652015f5d05c3193bcaeafce74fc6p-13) 
        + ((double)in_147)*(((double)0x1.27ee727c4e19da9d7a927f7d444efa62p-18) 
        + ((double)in_147)*(((double)0x1.60d9bf29b135881f577b2775d02bd8fcp-20) 
        + ((double)in_147)*(((double)0x1.653184dae8e937829eb7cbcbb2690098p-22) 
        + ((double)in_147)*(((double)-0x1.4ec2a0c2fc99a4e7e062a9252573f7e6p-24) 
        + ((double)in_147)*(((double)0x1.74344215a0c4a4832b8a548b3baa1f08p-28) 
        + ((double)in_147)*(((double)-0x1.1f75197e8def097c835edf2cc2351af2p-33) 
        + ((double)in_147)*((double)-0x1.777b24606dd83bb52a5e865a2a7f7292p-44)))))))))))))));
    double recons_43 = in_148 < 0.0 ? ((-(M_PI+M_PI))-(out_55-(M_PI+M_PI))) : out_55;
    return recons_43;
}

double my_core_function_sin_34(double in_152)
{
// (periodic (* PI 4) (MirrorLeft (* (* 2 x) (- (/ 1 2))) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))
    int k_50 = (int) floor((((double)in_152)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_151 = ((double)in_152) - k_50*((double)12.566370614359172);
    double in_150 = in_151 < 0.0 ? (0.0 - in_151) : in_151;
    double out_56 = (((double)in_150)*(((double)0x1.fffffe2f8a0046652e2bfaa63bbbd214p-1) 
        + ((double)in_150)*(((double)0x1.a12d9703db57edc2478240add6f8302ap-21) 
        + ((double)in_150)*(((double)-0x1.55576219c1a5ba1b0e311b4034036286p-3) 
        + ((double)in_150)*(((double)0x1.4d4a9f3a92460453f452b2a6388522fcp-17) 
        + ((double)in_150)*(((double)0x1.1093c69f4d261306e7ca5c9423717a3cp-7) 
        + ((double)in_150)*(((double)0x1.e672d75c0494c66f1874c22b687387dep-17) 
        + ((double)in_150)*(((double)-0x1.b42652015f5d05c3193bcaeafce74fc6p-13) 
        + ((double)in_150)*(((double)0x1.27ee727c4e19da9d7a927f7d444efa62p-18) 
        + ((double)in_150)*(((double)0x1.60d9bf29b135881f577b2775d02bd8fcp-20) 
        + ((double)in_150)*(((double)0x1.653184dae8e937829eb7cbcbb2690098p-22) 
        + ((double)in_150)*(((double)-0x1.4ec2a0c2fc99a4e7e062a9252573f7e6p-24) 
        + ((double)in_150)*(((double)0x1.74344215a0c4a4832b8a548b3baa1f08p-28) 
        + ((double)in_150)*(((double)-0x1.1f75197e8def097c835edf2cc2351af2p-33) 
        + ((double)in_150)*((double)-0x1.777b24606dd83bb52a5e865a2a7f7292p-44)))))))))))))));
    double recons_44 = in_151 < 0.0 ? ((2*out_56)*(-(1/2))) : out_56;
    return recons_44;
}

double my_core_function_sin_35(double in_155)
{
// (periodic (* PI 4) (MirrorLeft (- x) (Horner (MinimaxPolynomial (sin x) [0 (+ PI PI)]))))
    int k_51 = (int) floor((((double)in_155)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_154 = ((double)in_155) - k_51*((double)12.566370614359172);
    double in_153 = in_154 < 0.0 ? (0.0 - in_154) : in_154;
    double out_57 = (((double)in_153)*(((double)0x1.fffffe2f8a0046652e2bfaa63bbbd214p-1) 
        + ((double)in_153)*(((double)0x1.a12d9703db57edc2478240add6f8302ap-21) 
        + ((double)in_153)*(((double)-0x1.55576219c1a5ba1b0e311b4034036286p-3) 
        + ((double)in_153)*(((double)0x1.4d4a9f3a92460453f452b2a6388522fcp-17) 
        + ((double)in_153)*(((double)0x1.1093c69f4d261306e7ca5c9423717a3cp-7) 
        + ((double)in_153)*(((double)0x1.e672d75c0494c66f1874c22b687387dep-17) 
        + ((double)in_153)*(((double)-0x1.b42652015f5d05c3193bcaeafce74fc6p-13) 
        + ((double)in_153)*(((double)0x1.27ee727c4e19da9d7a927f7d444efa62p-18) 
        + ((double)in_153)*(((double)0x1.60d9bf29b135881f577b2775d02bd8fcp-20) 
        + ((double)in_153)*(((double)0x1.653184dae8e937829eb7cbcbb2690098p-22) 
        + ((double)in_153)*(((double)-0x1.4ec2a0c2fc99a4e7e062a9252573f7e6p-24) 
        + ((double)in_153)*(((double)0x1.74344215a0c4a4832b8a548b3baa1f08p-28) 
        + ((double)in_153)*(((double)-0x1.1f75197e8def097c835edf2cc2351af2p-33) 
        + ((double)in_153)*((double)-0x1.777b24606dd83bb52a5e865a2a7f7292p-44)))))))))))))));
    double recons_45 = in_154 < 0.0 ? (-out_57) : out_57;
    return recons_45;
}

double my_core_function_sin_36(double in_158)
{
// (periodic (* PI 4) (MirrorRight (+ (- (- x 2)) (- 2)) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))
    int k_52 = (int) floor((((double)in_158)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_157 = ((double)in_158) - k_52*((double)12.566370614359172);
    double in_156 = in_157 < 0.0 ? in_157 : (0.0 - in_157);
    double out_58 = (((double)in_156)*(((double)0x1.fffffe2f8a002bcb311c70bda360a4ccp-1) 
        + ((double)in_156)*(((double)-0x1.a12d96f2b35bbe4767907e1014687834p-21) 
        + ((double)in_156)*(((double)-0x1.55576219c16e741401ecb22b0c9be2fap-3) 
        + ((double)in_156)*(((double)-0x1.4d4a9f0ca0cc6a795c2214ec72f3853p-17) 
        + ((double)in_156)*(((double)0x1.1093c69f5fde4e3fff3a4d7a46a8aeaep-7) 
        + ((double)in_156)*(((double)-0x1.e672d713f2cc95ccf42f1e01c9e20606p-17) 
        + ((double)in_156)*(((double)-0x1.b42651fe93b8f43b394cf42ef9d130ap-13) 
        + ((double)in_156)*(((double)-0x1.27ee7256d04d047593b4c86dee78cc2ep-18) 
        + ((double)in_156)*(((double)0x1.60d9bf5511885d0b63b9da5ae347b61ep-20) 
        + ((double)in_156)*(((double)-0x1.653184b82f1f08992b77c5409f96a862p-22) 
        + ((double)in_156)*(((double)-0x1.4ec2a0b014f9cc6c936599732c265644p-24) 
        + ((double)in_156)*(((double)-0x1.743441fae56ad662d1b462bb22939014p-28) 
        + ((double)in_156)*(((double)-0x1.1f75195244a814ffbe22afc5681ca86ep-33) 
        + ((double)in_156)*((double)0x1.777b2c88af76e732ba70372d59ce65e2p-44)))))))))))))));
    double recons_46 = in_157 < 0.0 ? out_58 : ((-(out_58-2))+(-2));
    return recons_46;
}

double my_core_function_sin_37(double in_161)
{
// (periodic (* PI 4) (MirrorRight (- (+ (+ PI PI) (- (* PI 4) x)) (* PI 6)) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))
    int k_53 = (int) floor((((double)in_161)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_160 = ((double)in_161) - k_53*((double)12.566370614359172);
    double in_159 = in_160 < 0.0 ? in_160 : (0.0 - in_160);
    double out_59 = (((double)in_159)*(((double)0x1.fffffe2f8a002bcb311c70bda360a4ccp-1) 
        + ((double)in_159)*(((double)-0x1.a12d96f2b35bbe4767907e1014687834p-21) 
        + ((double)in_159)*(((double)-0x1.55576219c16e741401ecb22b0c9be2fap-3) 
        + ((double)in_159)*(((double)-0x1.4d4a9f0ca0cc6a795c2214ec72f3853p-17) 
        + ((double)in_159)*(((double)0x1.1093c69f5fde4e3fff3a4d7a46a8aeaep-7) 
        + ((double)in_159)*(((double)-0x1.e672d713f2cc95ccf42f1e01c9e20606p-17) 
        + ((double)in_159)*(((double)-0x1.b42651fe93b8f43b394cf42ef9d130ap-13) 
        + ((double)in_159)*(((double)-0x1.27ee7256d04d047593b4c86dee78cc2ep-18) 
        + ((double)in_159)*(((double)0x1.60d9bf5511885d0b63b9da5ae347b61ep-20) 
        + ((double)in_159)*(((double)-0x1.653184b82f1f08992b77c5409f96a862p-22) 
        + ((double)in_159)*(((double)-0x1.4ec2a0b014f9cc6c936599732c265644p-24) 
        + ((double)in_159)*(((double)-0x1.743441fae56ad662d1b462bb22939014p-28) 
        + ((double)in_159)*(((double)-0x1.1f75195244a814ffbe22afc5681ca86ep-33) 
        + ((double)in_159)*((double)0x1.777b2c88af76e732ba70372d59ce65e2p-44)))))))))))))));
    double recons_47 = in_160 < 0.0 ? out_59 : (((M_PI+M_PI)+((M_PI*4)-out_59))-(M_PI*6));
    return recons_47;
}

double my_core_function_sin_38(double in_164)
{
// (periodic (* PI 4) (MirrorRight (- (* PI 4) (+ x (* PI 4))) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))
    int k_54 = (int) floor((((double)in_164)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_163 = ((double)in_164) - k_54*((double)12.566370614359172);
    double in_162 = in_163 < 0.0 ? in_163 : (0.0 - in_163);
    double out_60 = (((double)in_162)*(((double)0x1.fffffe2f8a002bcb311c70bda360a4ccp-1) 
        + ((double)in_162)*(((double)-0x1.a12d96f2b35bbe4767907e1014687834p-21) 
        + ((double)in_162)*(((double)-0x1.55576219c16e741401ecb22b0c9be2fap-3) 
        + ((double)in_162)*(((double)-0x1.4d4a9f0ca0cc6a795c2214ec72f3853p-17) 
        + ((double)in_162)*(((double)0x1.1093c69f5fde4e3fff3a4d7a46a8aeaep-7) 
        + ((double)in_162)*(((double)-0x1.e672d713f2cc95ccf42f1e01c9e20606p-17) 
        + ((double)in_162)*(((double)-0x1.b42651fe93b8f43b394cf42ef9d130ap-13) 
        + ((double)in_162)*(((double)-0x1.27ee7256d04d047593b4c86dee78cc2ep-18) 
        + ((double)in_162)*(((double)0x1.60d9bf5511885d0b63b9da5ae347b61ep-20) 
        + ((double)in_162)*(((double)-0x1.653184b82f1f08992b77c5409f96a862p-22) 
        + ((double)in_162)*(((double)-0x1.4ec2a0b014f9cc6c936599732c265644p-24) 
        + ((double)in_162)*(((double)-0x1.743441fae56ad662d1b462bb22939014p-28) 
        + ((double)in_162)*(((double)-0x1.1f75195244a814ffbe22afc5681ca86ep-33) 
        + ((double)in_162)*((double)0x1.777b2c88af76e732ba70372d59ce65e2p-44)))))))))))))));
    double recons_48 = in_163 < 0.0 ? out_60 : ((M_PI*4)-(out_60+(M_PI*4)));
    return recons_48;
}

double my_core_function_sin_39(double in_167)
{
// (periodic (* PI 4) (MirrorRight (/ (* 2 x) (- 2)) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))
    int k_55 = (int) floor((((double)in_167)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_166 = ((double)in_167) - k_55*((double)12.566370614359172);
    double in_165 = in_166 < 0.0 ? in_166 : (0.0 - in_166);
    double out_61 = (((double)in_165)*(((double)0x1.fffffe2f8a002bcb311c70bda360a4ccp-1) 
        + ((double)in_165)*(((double)-0x1.a12d96f2b35bbe4767907e1014687834p-21) 
        + ((double)in_165)*(((double)-0x1.55576219c16e741401ecb22b0c9be2fap-3) 
        + ((double)in_165)*(((double)-0x1.4d4a9f0ca0cc6a795c2214ec72f3853p-17) 
        + ((double)in_165)*(((double)0x1.1093c69f5fde4e3fff3a4d7a46a8aeaep-7) 
        + ((double)in_165)*(((double)-0x1.e672d713f2cc95ccf42f1e01c9e20606p-17) 
        + ((double)in_165)*(((double)-0x1.b42651fe93b8f43b394cf42ef9d130ap-13) 
        + ((double)in_165)*(((double)-0x1.27ee7256d04d047593b4c86dee78cc2ep-18) 
        + ((double)in_165)*(((double)0x1.60d9bf5511885d0b63b9da5ae347b61ep-20) 
        + ((double)in_165)*(((double)-0x1.653184b82f1f08992b77c5409f96a862p-22) 
        + ((double)in_165)*(((double)-0x1.4ec2a0b014f9cc6c936599732c265644p-24) 
        + ((double)in_165)*(((double)-0x1.743441fae56ad662d1b462bb22939014p-28) 
        + ((double)in_165)*(((double)-0x1.1f75195244a814ffbe22afc5681ca86ep-33) 
        + ((double)in_165)*((double)0x1.777b2c88af76e732ba70372d59ce65e2p-44)))))))))))))));
    double recons_49 = in_166 < 0.0 ? out_61 : ((2*out_61)/(-2));
    return recons_49;
}

double my_core_function_sin_40(double in_170)
{
// (periodic (* PI 4) (MirrorRight (+ (- (- (- (+ PI PI)) (- (* PI 4) x))) (- (* PI 6))) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))
    int k_56 = (int) floor((((double)in_170)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_169 = ((double)in_170) - k_56*((double)12.566370614359172);
    double in_168 = in_169 < 0.0 ? in_169 : (0.0 - in_169);
    double out_62 = (((double)in_168)*(((double)0x1.fffffe2f8a002bcb311c70bda360a4ccp-1) 
        + ((double)in_168)*(((double)-0x1.a12d96f2b35bbe4767907e1014687834p-21) 
        + ((double)in_168)*(((double)-0x1.55576219c16e741401ecb22b0c9be2fap-3) 
        + ((double)in_168)*(((double)-0x1.4d4a9f0ca0cc6a795c2214ec72f3853p-17) 
        + ((double)in_168)*(((double)0x1.1093c69f5fde4e3fff3a4d7a46a8aeaep-7) 
        + ((double)in_168)*(((double)-0x1.e672d713f2cc95ccf42f1e01c9e20606p-17) 
        + ((double)in_168)*(((double)-0x1.b42651fe93b8f43b394cf42ef9d130ap-13) 
        + ((double)in_168)*(((double)-0x1.27ee7256d04d047593b4c86dee78cc2ep-18) 
        + ((double)in_168)*(((double)0x1.60d9bf5511885d0b63b9da5ae347b61ep-20) 
        + ((double)in_168)*(((double)-0x1.653184b82f1f08992b77c5409f96a862p-22) 
        + ((double)in_168)*(((double)-0x1.4ec2a0b014f9cc6c936599732c265644p-24) 
        + ((double)in_168)*(((double)-0x1.743441fae56ad662d1b462bb22939014p-28) 
        + ((double)in_168)*(((double)-0x1.1f75195244a814ffbe22afc5681ca86ep-33) 
        + ((double)in_168)*((double)0x1.777b2c88af76e732ba70372d59ce65e2p-44)))))))))))))));
    double recons_50 = in_169 < 0.0 ? out_62 : ((-((-(M_PI+M_PI))-((M_PI*4)-out_62)))+(-(M_PI*6)));
    return recons_50;
}

double my_core_function_sin_41(double in_173)
{
// (periodic (* PI 4) (MirrorRight (+ (- (- x 1)) (- 1)) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))
    int k_57 = (int) floor((((double)in_173)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_172 = ((double)in_173) - k_57*((double)12.566370614359172);
    double in_171 = in_172 < 0.0 ? in_172 : (0.0 - in_172);
    double out_63 = (((double)in_171)*(((double)0x1.fffffe2f8a002bcb311c70bda360a4ccp-1) 
        + ((double)in_171)*(((double)-0x1.a12d96f2b35bbe4767907e1014687834p-21) 
        + ((double)in_171)*(((double)-0x1.55576219c16e741401ecb22b0c9be2fap-3) 
        + ((double)in_171)*(((double)-0x1.4d4a9f0ca0cc6a795c2214ec72f3853p-17) 
        + ((double)in_171)*(((double)0x1.1093c69f5fde4e3fff3a4d7a46a8aeaep-7) 
        + ((double)in_171)*(((double)-0x1.e672d713f2cc95ccf42f1e01c9e20606p-17) 
        + ((double)in_171)*(((double)-0x1.b42651fe93b8f43b394cf42ef9d130ap-13) 
        + ((double)in_171)*(((double)-0x1.27ee7256d04d047593b4c86dee78cc2ep-18) 
        + ((double)in_171)*(((double)0x1.60d9bf5511885d0b63b9da5ae347b61ep-20) 
        + ((double)in_171)*(((double)-0x1.653184b82f1f08992b77c5409f96a862p-22) 
        + ((double)in_171)*(((double)-0x1.4ec2a0b014f9cc6c936599732c265644p-24) 
        + ((double)in_171)*(((double)-0x1.743441fae56ad662d1b462bb22939014p-28) 
        + ((double)in_171)*(((double)-0x1.1f75195244a814ffbe22afc5681ca86ep-33) 
        + ((double)in_171)*((double)0x1.777b2c88af76e732ba70372d59ce65e2p-44)))))))))))))));
    double recons_51 = in_172 < 0.0 ? out_63 : ((-(out_63-1))+(-1));
    return recons_51;
}

double my_core_function_sin_42(double in_176)
{
// (periodic (* PI 4) (MirrorRight (- (* PI 6) (+ (+ PI PI) (+ x (* PI 4)))) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))
    int k_58 = (int) floor((((double)in_176)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_175 = ((double)in_176) - k_58*((double)12.566370614359172);
    double in_174 = in_175 < 0.0 ? in_175 : (0.0 - in_175);
    double out_64 = (((double)in_174)*(((double)0x1.fffffe2f8a002bcb311c70bda360a4ccp-1) 
        + ((double)in_174)*(((double)-0x1.a12d96f2b35bbe4767907e1014687834p-21) 
        + ((double)in_174)*(((double)-0x1.55576219c16e741401ecb22b0c9be2fap-3) 
        + ((double)in_174)*(((double)-0x1.4d4a9f0ca0cc6a795c2214ec72f3853p-17) 
        + ((double)in_174)*(((double)0x1.1093c69f5fde4e3fff3a4d7a46a8aeaep-7) 
        + ((double)in_174)*(((double)-0x1.e672d713f2cc95ccf42f1e01c9e20606p-17) 
        + ((double)in_174)*(((double)-0x1.b42651fe93b8f43b394cf42ef9d130ap-13) 
        + ((double)in_174)*(((double)-0x1.27ee7256d04d047593b4c86dee78cc2ep-18) 
        + ((double)in_174)*(((double)0x1.60d9bf5511885d0b63b9da5ae347b61ep-20) 
        + ((double)in_174)*(((double)-0x1.653184b82f1f08992b77c5409f96a862p-22) 
        + ((double)in_174)*(((double)-0x1.4ec2a0b014f9cc6c936599732c265644p-24) 
        + ((double)in_174)*(((double)-0x1.743441fae56ad662d1b462bb22939014p-28) 
        + ((double)in_174)*(((double)-0x1.1f75195244a814ffbe22afc5681ca86ep-33) 
        + ((double)in_174)*((double)0x1.777b2c88af76e732ba70372d59ce65e2p-44)))))))))))))));
    double recons_52 = in_175 < 0.0 ? out_64 : ((M_PI*6)-((M_PI+M_PI)+(out_64+(M_PI*4))));
    return recons_52;
}

double my_core_function_sin_43(double in_179)
{
// (periodic (* PI 4) (MirrorRight (- (- (+ PI PI)) (- x (+ PI PI))) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))
    int k_59 = (int) floor((((double)in_179)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_178 = ((double)in_179) - k_59*((double)12.566370614359172);
    double in_177 = in_178 < 0.0 ? in_178 : (0.0 - in_178);
    double out_65 = (((double)in_177)*(((double)0x1.fffffe2f8a002bcb311c70bda360a4ccp-1) 
        + ((double)in_177)*(((double)-0x1.a12d96f2b35bbe4767907e1014687834p-21) 
        + ((double)in_177)*(((double)-0x1.55576219c16e741401ecb22b0c9be2fap-3) 
        + ((double)in_177)*(((double)-0x1.4d4a9f0ca0cc6a795c2214ec72f3853p-17) 
        + ((double)in_177)*(((double)0x1.1093c69f5fde4e3fff3a4d7a46a8aeaep-7) 
        + ((double)in_177)*(((double)-0x1.e672d713f2cc95ccf42f1e01c9e20606p-17) 
        + ((double)in_177)*(((double)-0x1.b42651fe93b8f43b394cf42ef9d130ap-13) 
        + ((double)in_177)*(((double)-0x1.27ee7256d04d047593b4c86dee78cc2ep-18) 
        + ((double)in_177)*(((double)0x1.60d9bf5511885d0b63b9da5ae347b61ep-20) 
        + ((double)in_177)*(((double)-0x1.653184b82f1f08992b77c5409f96a862p-22) 
        + ((double)in_177)*(((double)-0x1.4ec2a0b014f9cc6c936599732c265644p-24) 
        + ((double)in_177)*(((double)-0x1.743441fae56ad662d1b462bb22939014p-28) 
        + ((double)in_177)*(((double)-0x1.1f75195244a814ffbe22afc5681ca86ep-33) 
        + ((double)in_177)*((double)0x1.777b2c88af76e732ba70372d59ce65e2p-44)))))))))))))));
    double recons_53 = in_178 < 0.0 ? out_65 : ((-(M_PI+M_PI))-(out_65-(M_PI+M_PI)));
    return recons_53;
}

double my_core_function_sin_44(double in_182)
{
// (periodic (* PI 4) (MirrorRight (* (* 2 x) (- (/ 1 2))) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))
    int k_60 = (int) floor((((double)in_182)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_181 = ((double)in_182) - k_60*((double)12.566370614359172);
    double in_180 = in_181 < 0.0 ? in_181 : (0.0 - in_181);
    double out_66 = (((double)in_180)*(((double)0x1.fffffe2f8a002bcb311c70bda360a4ccp-1) 
        + ((double)in_180)*(((double)-0x1.a12d96f2b35bbe4767907e1014687834p-21) 
        + ((double)in_180)*(((double)-0x1.55576219c16e741401ecb22b0c9be2fap-3) 
        + ((double)in_180)*(((double)-0x1.4d4a9f0ca0cc6a795c2214ec72f3853p-17) 
        + ((double)in_180)*(((double)0x1.1093c69f5fde4e3fff3a4d7a46a8aeaep-7) 
        + ((double)in_180)*(((double)-0x1.e672d713f2cc95ccf42f1e01c9e20606p-17) 
        + ((double)in_180)*(((double)-0x1.b42651fe93b8f43b394cf42ef9d130ap-13) 
        + ((double)in_180)*(((double)-0x1.27ee7256d04d047593b4c86dee78cc2ep-18) 
        + ((double)in_180)*(((double)0x1.60d9bf5511885d0b63b9da5ae347b61ep-20) 
        + ((double)in_180)*(((double)-0x1.653184b82f1f08992b77c5409f96a862p-22) 
        + ((double)in_180)*(((double)-0x1.4ec2a0b014f9cc6c936599732c265644p-24) 
        + ((double)in_180)*(((double)-0x1.743441fae56ad662d1b462bb22939014p-28) 
        + ((double)in_180)*(((double)-0x1.1f75195244a814ffbe22afc5681ca86ep-33) 
        + ((double)in_180)*((double)0x1.777b2c88af76e732ba70372d59ce65e2p-44)))))))))))))));
    double recons_54 = in_181 < 0.0 ? out_66 : ((2*out_66)*(-(1/2)));
    return recons_54;
}

double my_core_function_sin_45(double in_185)
{
// (periodic (* PI 4) (MirrorRight (- x) (Horner (MinimaxPolynomial (sin x) [(- (+ PI PI)) 0]))))
    int k_61 = (int) floor((((double)in_185)-((double)-6.283185307179586))*((double)0.07957747154594767));
    double in_184 = ((double)in_185) - k_61*((double)12.566370614359172);
    double in_183 = in_184 < 0.0 ? in_184 : (0.0 - in_184);
    double out_67 = (((double)in_183)*(((double)0x1.fffffe2f8a002bcb311c70bda360a4ccp-1) 
        + ((double)in_183)*(((double)-0x1.a12d96f2b35bbe4767907e1014687834p-21) 
        + ((double)in_183)*(((double)-0x1.55576219c16e741401ecb22b0c9be2fap-3) 
        + ((double)in_183)*(((double)-0x1.4d4a9f0ca0cc6a795c2214ec72f3853p-17) 
        + ((double)in_183)*(((double)0x1.1093c69f5fde4e3fff3a4d7a46a8aeaep-7) 
        + ((double)in_183)*(((double)-0x1.e672d713f2cc95ccf42f1e01c9e20606p-17) 
        + ((double)in_183)*(((double)-0x1.b42651fe93b8f43b394cf42ef9d130ap-13) 
        + ((double)in_183)*(((double)-0x1.27ee7256d04d047593b4c86dee78cc2ep-18) 
        + ((double)in_183)*(((double)0x1.60d9bf5511885d0b63b9da5ae347b61ep-20) 
        + ((double)in_183)*(((double)-0x1.653184b82f1f08992b77c5409f96a862p-22) 
        + ((double)in_183)*(((double)-0x1.4ec2a0b014f9cc6c936599732c265644p-24) 
        + ((double)in_183)*(((double)-0x1.743441fae56ad662d1b462bb22939014p-28) 
        + ((double)in_183)*(((double)-0x1.1f75195244a814ffbe22afc5681ca86ep-33) 
        + ((double)in_183)*((double)0x1.777b2c88af76e732ba70372d59ce65e2p-44)))))))))))))));
    double recons_55 = in_184 < 0.0 ? out_67 : (-out_67);
    return recons_55;
}

double my_core_function_sin_46(double in_188)
{
// (periodic (+ PI PI) (MirrorLeft (+ (- (- x 2)) (- 2)) (Horner (MinimaxPolynomial (sin x) [0 PI]))))
    int k_62 = (int) floor((((double)in_188)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_187 = ((double)in_188) - k_62*((double)6.283185307179586);
    double in_186 = in_187 < 0.0 ? (0.0 - in_187) : in_187;
    double out_68 = (((double)in_186)*(((double)0x1.00000000003cb0067f0b6b796e0cbe92p0) 
        + ((double)in_186)*(((double)-0x1.f1539b1f3a373d06687bd16d8984fe6cp-38) 
        + ((double)in_186)*(((double)-0x1.555555528a598cfe96aadd9753a86a38p-3) 
        + ((double)in_186)*(((double)-0x1.04782924118d1beb073006b4e67b9bccp-31) 
        + ((double)in_186)*(((double)0x1.11111498c02e48b35de474de478e1a8ap-7) 
        + ((double)in_186)*(((double)-0x1.fe05eedd7b9e1e063b04d8ad5249aca2p-29) 
        + ((double)in_186)*(((double)-0x1.a016eaa2be2170df3598e5288a938d34p-13) 
        + ((double)in_186)*(((double)-0x1.b3de4606534174c0a84776e9920c73p-28) 
        + ((double)in_186)*(((double)0x1.728c5043d2d7e69c4b039bc9c5463c44p-19) 
        + ((double)in_186)*(((double)-0x1.969990b39d0b49f83a08d0090f92cb12p-29) 
        + ((double)in_186)*(((double)-0x1.98c0b15a5d4d407845606168ce54cac2p-26) 
        + ((double)in_186)*(((double)-0x1.a73226a8e63d5f9f7c5d326d9422d7a8p-32) 
        + ((double)in_186)*(((double)0x1.0a103bbcaf5f953c518ff0b1b139ad58p-32) 
        + ((double)in_186)*((double)-0x1.8328374a2e9c269a98c1628fee33e2e4p-37)))))))))))))));
    double recons_56 = in_187 < 0.0 ? ((-(out_68-2))+(-2)) : out_68;
    return recons_56;
}

double my_core_function_sin_47(double in_191)
{
// (periodic (+ PI PI) (MirrorLeft (- (+ (+ PI PI) (- (* PI 4) x)) (* PI 6)) (Horner (MinimaxPolynomial (sin x) [0 PI]))))
    int k_63 = (int) floor((((double)in_191)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_190 = ((double)in_191) - k_63*((double)6.283185307179586);
    double in_189 = in_190 < 0.0 ? (0.0 - in_190) : in_190;
    double out_69 = (((double)in_189)*(((double)0x1.00000000003cb0067f0b6b796e0cbe92p0) 
        + ((double)in_189)*(((double)-0x1.f1539b1f3a373d06687bd16d8984fe6cp-38) 
        + ((double)in_189)*(((double)-0x1.555555528a598cfe96aadd9753a86a38p-3) 
        + ((double)in_189)*(((double)-0x1.04782924118d1beb073006b4e67b9bccp-31) 
        + ((double)in_189)*(((double)0x1.11111498c02e48b35de474de478e1a8ap-7) 
        + ((double)in_189)*(((double)-0x1.fe05eedd7b9e1e063b04d8ad5249aca2p-29) 
        + ((double)in_189)*(((double)-0x1.a016eaa2be2170df3598e5288a938d34p-13) 
        + ((double)in_189)*(((double)-0x1.b3de4606534174c0a84776e9920c73p-28) 
        + ((double)in_189)*(((double)0x1.728c5043d2d7e69c4b039bc9c5463c44p-19) 
        + ((double)in_189)*(((double)-0x1.969990b39d0b49f83a08d0090f92cb12p-29) 
        + ((double)in_189)*(((double)-0x1.98c0b15a5d4d407845606168ce54cac2p-26) 
        + ((double)in_189)*(((double)-0x1.a73226a8e63d5f9f7c5d326d9422d7a8p-32) 
        + ((double)in_189)*(((double)0x1.0a103bbcaf5f953c518ff0b1b139ad58p-32) 
        + ((double)in_189)*((double)-0x1.8328374a2e9c269a98c1628fee33e2e4p-37)))))))))))))));
    double recons_57 = in_190 < 0.0 ? (((M_PI+M_PI)+((M_PI*4)-out_69))-(M_PI*6)) : out_69;
    return recons_57;
}

double my_core_function_sin_48(double in_194)
{
// (periodic (+ PI PI) (MirrorLeft (- (* PI 4) (+ x (* PI 4))) (Horner (MinimaxPolynomial (sin x) [0 PI]))))
    int k_64 = (int) floor((((double)in_194)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_193 = ((double)in_194) - k_64*((double)6.283185307179586);
    double in_192 = in_193 < 0.0 ? (0.0 - in_193) : in_193;
    double out_70 = (((double)in_192)*(((double)0x1.00000000003cb0067f0b6b796e0cbe92p0) 
        + ((double)in_192)*(((double)-0x1.f1539b1f3a373d06687bd16d8984fe6cp-38) 
        + ((double)in_192)*(((double)-0x1.555555528a598cfe96aadd9753a86a38p-3) 
        + ((double)in_192)*(((double)-0x1.04782924118d1beb073006b4e67b9bccp-31) 
        + ((double)in_192)*(((double)0x1.11111498c02e48b35de474de478e1a8ap-7) 
        + ((double)in_192)*(((double)-0x1.fe05eedd7b9e1e063b04d8ad5249aca2p-29) 
        + ((double)in_192)*(((double)-0x1.a016eaa2be2170df3598e5288a938d34p-13) 
        + ((double)in_192)*(((double)-0x1.b3de4606534174c0a84776e9920c73p-28) 
        + ((double)in_192)*(((double)0x1.728c5043d2d7e69c4b039bc9c5463c44p-19) 
        + ((double)in_192)*(((double)-0x1.969990b39d0b49f83a08d0090f92cb12p-29) 
        + ((double)in_192)*(((double)-0x1.98c0b15a5d4d407845606168ce54cac2p-26) 
        + ((double)in_192)*(((double)-0x1.a73226a8e63d5f9f7c5d326d9422d7a8p-32) 
        + ((double)in_192)*(((double)0x1.0a103bbcaf5f953c518ff0b1b139ad58p-32) 
        + ((double)in_192)*((double)-0x1.8328374a2e9c269a98c1628fee33e2e4p-37)))))))))))))));
    double recons_58 = in_193 < 0.0 ? ((M_PI*4)-(out_70+(M_PI*4))) : out_70;
    return recons_58;
}

double my_core_function_sin_49(double in_197)
{
// (periodic (+ PI PI) (MirrorLeft (/ (* 2 x) (- 2)) (Horner (MinimaxPolynomial (sin x) [0 PI]))))
    int k_65 = (int) floor((((double)in_197)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_196 = ((double)in_197) - k_65*((double)6.283185307179586);
    double in_195 = in_196 < 0.0 ? (0.0 - in_196) : in_196;
    double out_71 = (((double)in_195)*(((double)0x1.00000000003cb0067f0b6b796e0cbe92p0) 
        + ((double)in_195)*(((double)-0x1.f1539b1f3a373d06687bd16d8984fe6cp-38) 
        + ((double)in_195)*(((double)-0x1.555555528a598cfe96aadd9753a86a38p-3) 
        + ((double)in_195)*(((double)-0x1.04782924118d1beb073006b4e67b9bccp-31) 
        + ((double)in_195)*(((double)0x1.11111498c02e48b35de474de478e1a8ap-7) 
        + ((double)in_195)*(((double)-0x1.fe05eedd7b9e1e063b04d8ad5249aca2p-29) 
        + ((double)in_195)*(((double)-0x1.a016eaa2be2170df3598e5288a938d34p-13) 
        + ((double)in_195)*(((double)-0x1.b3de4606534174c0a84776e9920c73p-28) 
        + ((double)in_195)*(((double)0x1.728c5043d2d7e69c4b039bc9c5463c44p-19) 
        + ((double)in_195)*(((double)-0x1.969990b39d0b49f83a08d0090f92cb12p-29) 
        + ((double)in_195)*(((double)-0x1.98c0b15a5d4d407845606168ce54cac2p-26) 
        + ((double)in_195)*(((double)-0x1.a73226a8e63d5f9f7c5d326d9422d7a8p-32) 
        + ((double)in_195)*(((double)0x1.0a103bbcaf5f953c518ff0b1b139ad58p-32) 
        + ((double)in_195)*((double)-0x1.8328374a2e9c269a98c1628fee33e2e4p-37)))))))))))))));
    double recons_59 = in_196 < 0.0 ? ((2*out_71)/(-2)) : out_71;
    return recons_59;
}

double my_core_function_sin_50(double in_200)
{
// (periodic (+ PI PI) (MirrorLeft (+ (- (- (- (+ PI PI)) (- (* PI 4) x))) (- (* PI 6))) (Horner (MinimaxPolynomial (sin x) [0 PI]))))
    int k_66 = (int) floor((((double)in_200)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_199 = ((double)in_200) - k_66*((double)6.283185307179586);
    double in_198 = in_199 < 0.0 ? (0.0 - in_199) : in_199;
    double out_72 = (((double)in_198)*(((double)0x1.00000000003cb0067f0b6b796e0cbe92p0) 
        + ((double)in_198)*(((double)-0x1.f1539b1f3a373d06687bd16d8984fe6cp-38) 
        + ((double)in_198)*(((double)-0x1.555555528a598cfe96aadd9753a86a38p-3) 
        + ((double)in_198)*(((double)-0x1.04782924118d1beb073006b4e67b9bccp-31) 
        + ((double)in_198)*(((double)0x1.11111498c02e48b35de474de478e1a8ap-7) 
        + ((double)in_198)*(((double)-0x1.fe05eedd7b9e1e063b04d8ad5249aca2p-29) 
        + ((double)in_198)*(((double)-0x1.a016eaa2be2170df3598e5288a938d34p-13) 
        + ((double)in_198)*(((double)-0x1.b3de4606534174c0a84776e9920c73p-28) 
        + ((double)in_198)*(((double)0x1.728c5043d2d7e69c4b039bc9c5463c44p-19) 
        + ((double)in_198)*(((double)-0x1.969990b39d0b49f83a08d0090f92cb12p-29) 
        + ((double)in_198)*(((double)-0x1.98c0b15a5d4d407845606168ce54cac2p-26) 
        + ((double)in_198)*(((double)-0x1.a73226a8e63d5f9f7c5d326d9422d7a8p-32) 
        + ((double)in_198)*(((double)0x1.0a103bbcaf5f953c518ff0b1b139ad58p-32) 
        + ((double)in_198)*((double)-0x1.8328374a2e9c269a98c1628fee33e2e4p-37)))))))))))))));
    double recons_60 = in_199 < 0.0 ? ((-((-(M_PI+M_PI))-((M_PI*4)-out_72)))+(-(M_PI*6))) : out_72;
    return recons_60;
}

double my_core_function_sin_51(double in_203)
{
// (periodic (+ PI PI) (MirrorLeft (+ (- (- x 1)) (- 1)) (Horner (MinimaxPolynomial (sin x) [0 PI]))))
    int k_67 = (int) floor((((double)in_203)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_202 = ((double)in_203) - k_67*((double)6.283185307179586);
    double in_201 = in_202 < 0.0 ? (0.0 - in_202) : in_202;
    double out_73 = (((double)in_201)*(((double)0x1.00000000003cb0067f0b6b796e0cbe92p0) 
        + ((double)in_201)*(((double)-0x1.f1539b1f3a373d06687bd16d8984fe6cp-38) 
        + ((double)in_201)*(((double)-0x1.555555528a598cfe96aadd9753a86a38p-3) 
        + ((double)in_201)*(((double)-0x1.04782924118d1beb073006b4e67b9bccp-31) 
        + ((double)in_201)*(((double)0x1.11111498c02e48b35de474de478e1a8ap-7) 
        + ((double)in_201)*(((double)-0x1.fe05eedd7b9e1e063b04d8ad5249aca2p-29) 
        + ((double)in_201)*(((double)-0x1.a016eaa2be2170df3598e5288a938d34p-13) 
        + ((double)in_201)*(((double)-0x1.b3de4606534174c0a84776e9920c73p-28) 
        + ((double)in_201)*(((double)0x1.728c5043d2d7e69c4b039bc9c5463c44p-19) 
        + ((double)in_201)*(((double)-0x1.969990b39d0b49f83a08d0090f92cb12p-29) 
        + ((double)in_201)*(((double)-0x1.98c0b15a5d4d407845606168ce54cac2p-26) 
        + ((double)in_201)*(((double)-0x1.a73226a8e63d5f9f7c5d326d9422d7a8p-32) 
        + ((double)in_201)*(((double)0x1.0a103bbcaf5f953c518ff0b1b139ad58p-32) 
        + ((double)in_201)*((double)-0x1.8328374a2e9c269a98c1628fee33e2e4p-37)))))))))))))));
    double recons_61 = in_202 < 0.0 ? ((-(out_73-1))+(-1)) : out_73;
    return recons_61;
}

double my_core_function_sin_52(double in_206)
{
// (periodic (+ PI PI) (MirrorLeft (- (* PI 6) (+ (+ PI PI) (+ x (* PI 4)))) (Horner (MinimaxPolynomial (sin x) [0 PI]))))
    int k_68 = (int) floor((((double)in_206)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_205 = ((double)in_206) - k_68*((double)6.283185307179586);
    double in_204 = in_205 < 0.0 ? (0.0 - in_205) : in_205;
    double out_74 = (((double)in_204)*(((double)0x1.00000000003cb0067f0b6b796e0cbe92p0) 
        + ((double)in_204)*(((double)-0x1.f1539b1f3a373d06687bd16d8984fe6cp-38) 
        + ((double)in_204)*(((double)-0x1.555555528a598cfe96aadd9753a86a38p-3) 
        + ((double)in_204)*(((double)-0x1.04782924118d1beb073006b4e67b9bccp-31) 
        + ((double)in_204)*(((double)0x1.11111498c02e48b35de474de478e1a8ap-7) 
        + ((double)in_204)*(((double)-0x1.fe05eedd7b9e1e063b04d8ad5249aca2p-29) 
        + ((double)in_204)*(((double)-0x1.a016eaa2be2170df3598e5288a938d34p-13) 
        + ((double)in_204)*(((double)-0x1.b3de4606534174c0a84776e9920c73p-28) 
        + ((double)in_204)*(((double)0x1.728c5043d2d7e69c4b039bc9c5463c44p-19) 
        + ((double)in_204)*(((double)-0x1.969990b39d0b49f83a08d0090f92cb12p-29) 
        + ((double)in_204)*(((double)-0x1.98c0b15a5d4d407845606168ce54cac2p-26) 
        + ((double)in_204)*(((double)-0x1.a73226a8e63d5f9f7c5d326d9422d7a8p-32) 
        + ((double)in_204)*(((double)0x1.0a103bbcaf5f953c518ff0b1b139ad58p-32) 
        + ((double)in_204)*((double)-0x1.8328374a2e9c269a98c1628fee33e2e4p-37)))))))))))))));
    double recons_62 = in_205 < 0.0 ? ((M_PI*6)-((M_PI+M_PI)+(out_74+(M_PI*4)))) : out_74;
    return recons_62;
}

double my_core_function_sin_53(double in_209)
{
// (periodic (+ PI PI) (MirrorLeft (- (- (+ PI PI)) (- x (+ PI PI))) (Horner (MinimaxPolynomial (sin x) [0 PI]))))
    int k_69 = (int) floor((((double)in_209)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_208 = ((double)in_209) - k_69*((double)6.283185307179586);
    double in_207 = in_208 < 0.0 ? (0.0 - in_208) : in_208;
    double out_75 = (((double)in_207)*(((double)0x1.00000000003cb0067f0b6b796e0cbe92p0) 
        + ((double)in_207)*(((double)-0x1.f1539b1f3a373d06687bd16d8984fe6cp-38) 
        + ((double)in_207)*(((double)-0x1.555555528a598cfe96aadd9753a86a38p-3) 
        + ((double)in_207)*(((double)-0x1.04782924118d1beb073006b4e67b9bccp-31) 
        + ((double)in_207)*(((double)0x1.11111498c02e48b35de474de478e1a8ap-7) 
        + ((double)in_207)*(((double)-0x1.fe05eedd7b9e1e063b04d8ad5249aca2p-29) 
        + ((double)in_207)*(((double)-0x1.a016eaa2be2170df3598e5288a938d34p-13) 
        + ((double)in_207)*(((double)-0x1.b3de4606534174c0a84776e9920c73p-28) 
        + ((double)in_207)*(((double)0x1.728c5043d2d7e69c4b039bc9c5463c44p-19) 
        + ((double)in_207)*(((double)-0x1.969990b39d0b49f83a08d0090f92cb12p-29) 
        + ((double)in_207)*(((double)-0x1.98c0b15a5d4d407845606168ce54cac2p-26) 
        + ((double)in_207)*(((double)-0x1.a73226a8e63d5f9f7c5d326d9422d7a8p-32) 
        + ((double)in_207)*(((double)0x1.0a103bbcaf5f953c518ff0b1b139ad58p-32) 
        + ((double)in_207)*((double)-0x1.8328374a2e9c269a98c1628fee33e2e4p-37)))))))))))))));
    double recons_63 = in_208 < 0.0 ? ((-(M_PI+M_PI))-(out_75-(M_PI+M_PI))) : out_75;
    return recons_63;
}

double my_core_function_sin_54(double in_212)
{
// (periodic (+ PI PI) (MirrorLeft (* (* 2 x) (- (/ 1 2))) (Horner (MinimaxPolynomial (sin x) [0 PI]))))
    int k_70 = (int) floor((((double)in_212)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_211 = ((double)in_212) - k_70*((double)6.283185307179586);
    double in_210 = in_211 < 0.0 ? (0.0 - in_211) : in_211;
    double out_76 = (((double)in_210)*(((double)0x1.00000000003cb0067f0b6b796e0cbe92p0) 
        + ((double)in_210)*(((double)-0x1.f1539b1f3a373d06687bd16d8984fe6cp-38) 
        + ((double)in_210)*(((double)-0x1.555555528a598cfe96aadd9753a86a38p-3) 
        + ((double)in_210)*(((double)-0x1.04782924118d1beb073006b4e67b9bccp-31) 
        + ((double)in_210)*(((double)0x1.11111498c02e48b35de474de478e1a8ap-7) 
        + ((double)in_210)*(((double)-0x1.fe05eedd7b9e1e063b04d8ad5249aca2p-29) 
        + ((double)in_210)*(((double)-0x1.a016eaa2be2170df3598e5288a938d34p-13) 
        + ((double)in_210)*(((double)-0x1.b3de4606534174c0a84776e9920c73p-28) 
        + ((double)in_210)*(((double)0x1.728c5043d2d7e69c4b039bc9c5463c44p-19) 
        + ((double)in_210)*(((double)-0x1.969990b39d0b49f83a08d0090f92cb12p-29) 
        + ((double)in_210)*(((double)-0x1.98c0b15a5d4d407845606168ce54cac2p-26) 
        + ((double)in_210)*(((double)-0x1.a73226a8e63d5f9f7c5d326d9422d7a8p-32) 
        + ((double)in_210)*(((double)0x1.0a103bbcaf5f953c518ff0b1b139ad58p-32) 
        + ((double)in_210)*((double)-0x1.8328374a2e9c269a98c1628fee33e2e4p-37)))))))))))))));
    double recons_64 = in_211 < 0.0 ? ((2*out_76)*(-(1/2))) : out_76;
    return recons_64;
}

double my_core_function_sin_55(double in_215)
{
// (periodic (+ PI PI) (MirrorLeft (- x) (Horner (MinimaxPolynomial (sin x) [0 PI]))))
    int k_71 = (int) floor((((double)in_215)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_214 = ((double)in_215) - k_71*((double)6.283185307179586);
    double in_213 = in_214 < 0.0 ? (0.0 - in_214) : in_214;
    double out_77 = (((double)in_213)*(((double)0x1.00000000003cb0067f0b6b796e0cbe92p0) 
        + ((double)in_213)*(((double)-0x1.f1539b1f3a373d06687bd16d8984fe6cp-38) 
        + ((double)in_213)*(((double)-0x1.555555528a598cfe96aadd9753a86a38p-3) 
        + ((double)in_213)*(((double)-0x1.04782924118d1beb073006b4e67b9bccp-31) 
        + ((double)in_213)*(((double)0x1.11111498c02e48b35de474de478e1a8ap-7) 
        + ((double)in_213)*(((double)-0x1.fe05eedd7b9e1e063b04d8ad5249aca2p-29) 
        + ((double)in_213)*(((double)-0x1.a016eaa2be2170df3598e5288a938d34p-13) 
        + ((double)in_213)*(((double)-0x1.b3de4606534174c0a84776e9920c73p-28) 
        + ((double)in_213)*(((double)0x1.728c5043d2d7e69c4b039bc9c5463c44p-19) 
        + ((double)in_213)*(((double)-0x1.969990b39d0b49f83a08d0090f92cb12p-29) 
        + ((double)in_213)*(((double)-0x1.98c0b15a5d4d407845606168ce54cac2p-26) 
        + ((double)in_213)*(((double)-0x1.a73226a8e63d5f9f7c5d326d9422d7a8p-32) 
        + ((double)in_213)*(((double)0x1.0a103bbcaf5f953c518ff0b1b139ad58p-32) 
        + ((double)in_213)*((double)-0x1.8328374a2e9c269a98c1628fee33e2e4p-37)))))))))))))));
    double recons_65 = in_214 < 0.0 ? (-out_77) : out_77;
    return recons_65;
}

double my_core_function_sin_56(double in_218)
{
// (periodic (+ PI PI) (MirrorRight (+ (- (- x 2)) (- 2)) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))
    int k_72 = (int) floor((((double)in_218)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_217 = ((double)in_218) - k_72*((double)6.283185307179586);
    double in_216 = in_217 < 0.0 ? in_217 : (0.0 - in_217);
    double out_78 = (((double)in_216)*(((double)0x1.00000000003cb0067f0b6b57b15ba676p0) 
        + ((double)in_216)*(((double)0x1.f1539b1f3a3700e4af203ba7fbf5c912p-38) 
        + ((double)in_216)*(((double)-0x1.555555528a598cfe96aae1ebf8325784p-3) 
        + ((double)in_216)*(((double)0x1.04782924118d26ef2e7dc7239cc3dc46p-31) 
        + ((double)in_216)*(((double)0x1.11111498c02e48b35e1b9d912bbc85c8p-7) 
        + ((double)in_216)*(((double)0x1.fe05eedd7b9e3e4667e39d7d1a32babep-29) 
        + ((double)in_216)*(((double)-0x1.a016eaa2be2170df08c562e0f084a754p-13) 
        + ((double)in_216)*(((double)0x1.b3de4606534188ef11f41bef731092aep-28) 
        + ((double)in_216)*(((double)0x1.728c5043d2d7e6a267e29b7ac0ea490cp-19) 
        + ((double)in_216)*(((double)0x1.969990b39d0b540aae96c76e9c11b7f2p-29) 
        + ((double)in_216)*(((double)-0x1.98c0b15a5d4d401f24fb1e551a791a5cp-26) 
        + ((double)in_216)*(((double)0x1.a73226a8e63d63956a70a69ee2444684p-32) 
        + ((double)in_216)*(((double)0x1.0a103bbcaf5f95a5061f84025821a9d6p-32) 
        + ((double)in_216)*((double)0x1.8328374a2e9c2733614929013e076826p-37)))))))))))))));
    double recons_66 = in_217 < 0.0 ? out_78 : ((-(out_78-2))+(-2));
    return recons_66;
}

double my_core_function_sin_57(double in_221)
{
// (periodic (+ PI PI) (MirrorRight (- (+ (+ PI PI) (- (* PI 4) x)) (* PI 6)) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))
    int k_73 = (int) floor((((double)in_221)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_220 = ((double)in_221) - k_73*((double)6.283185307179586);
    double in_219 = in_220 < 0.0 ? in_220 : (0.0 - in_220);
    double out_79 = (((double)in_219)*(((double)0x1.00000000003cb0067f0b6b57b15ba676p0) 
        + ((double)in_219)*(((double)0x1.f1539b1f3a3700e4af203ba7fbf5c912p-38) 
        + ((double)in_219)*(((double)-0x1.555555528a598cfe96aae1ebf8325784p-3) 
        + ((double)in_219)*(((double)0x1.04782924118d26ef2e7dc7239cc3dc46p-31) 
        + ((double)in_219)*(((double)0x1.11111498c02e48b35e1b9d912bbc85c8p-7) 
        + ((double)in_219)*(((double)0x1.fe05eedd7b9e3e4667e39d7d1a32babep-29) 
        + ((double)in_219)*(((double)-0x1.a016eaa2be2170df08c562e0f084a754p-13) 
        + ((double)in_219)*(((double)0x1.b3de4606534188ef11f41bef731092aep-28) 
        + ((double)in_219)*(((double)0x1.728c5043d2d7e6a267e29b7ac0ea490cp-19) 
        + ((double)in_219)*(((double)0x1.969990b39d0b540aae96c76e9c11b7f2p-29) 
        + ((double)in_219)*(((double)-0x1.98c0b15a5d4d401f24fb1e551a791a5cp-26) 
        + ((double)in_219)*(((double)0x1.a73226a8e63d63956a70a69ee2444684p-32) 
        + ((double)in_219)*(((double)0x1.0a103bbcaf5f95a5061f84025821a9d6p-32) 
        + ((double)in_219)*((double)0x1.8328374a2e9c2733614929013e076826p-37)))))))))))))));
    double recons_67 = in_220 < 0.0 ? out_79 : (((M_PI+M_PI)+((M_PI*4)-out_79))-(M_PI*6));
    return recons_67;
}

double my_core_function_sin_58(double in_224)
{
// (periodic (+ PI PI) (MirrorRight (- (* PI 4) (+ x (* PI 4))) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))
    int k_74 = (int) floor((((double)in_224)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_223 = ((double)in_224) - k_74*((double)6.283185307179586);
    double in_222 = in_223 < 0.0 ? in_223 : (0.0 - in_223);
    double out_80 = (((double)in_222)*(((double)0x1.00000000003cb0067f0b6b57b15ba676p0) 
        + ((double)in_222)*(((double)0x1.f1539b1f3a3700e4af203ba7fbf5c912p-38) 
        + ((double)in_222)*(((double)-0x1.555555528a598cfe96aae1ebf8325784p-3) 
        + ((double)in_222)*(((double)0x1.04782924118d26ef2e7dc7239cc3dc46p-31) 
        + ((double)in_222)*(((double)0x1.11111498c02e48b35e1b9d912bbc85c8p-7) 
        + ((double)in_222)*(((double)0x1.fe05eedd7b9e3e4667e39d7d1a32babep-29) 
        + ((double)in_222)*(((double)-0x1.a016eaa2be2170df08c562e0f084a754p-13) 
        + ((double)in_222)*(((double)0x1.b3de4606534188ef11f41bef731092aep-28) 
        + ((double)in_222)*(((double)0x1.728c5043d2d7e6a267e29b7ac0ea490cp-19) 
        + ((double)in_222)*(((double)0x1.969990b39d0b540aae96c76e9c11b7f2p-29) 
        + ((double)in_222)*(((double)-0x1.98c0b15a5d4d401f24fb1e551a791a5cp-26) 
        + ((double)in_222)*(((double)0x1.a73226a8e63d63956a70a69ee2444684p-32) 
        + ((double)in_222)*(((double)0x1.0a103bbcaf5f95a5061f84025821a9d6p-32) 
        + ((double)in_222)*((double)0x1.8328374a2e9c2733614929013e076826p-37)))))))))))))));
    double recons_68 = in_223 < 0.0 ? out_80 : ((M_PI*4)-(out_80+(M_PI*4)));
    return recons_68;
}

double my_core_function_sin_59(double in_227)
{
// (periodic (+ PI PI) (MirrorRight (/ (* 2 x) (- 2)) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))
    int k_75 = (int) floor((((double)in_227)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_226 = ((double)in_227) - k_75*((double)6.283185307179586);
    double in_225 = in_226 < 0.0 ? in_226 : (0.0 - in_226);
    double out_81 = (((double)in_225)*(((double)0x1.00000000003cb0067f0b6b57b15ba676p0) 
        + ((double)in_225)*(((double)0x1.f1539b1f3a3700e4af203ba7fbf5c912p-38) 
        + ((double)in_225)*(((double)-0x1.555555528a598cfe96aae1ebf8325784p-3) 
        + ((double)in_225)*(((double)0x1.04782924118d26ef2e7dc7239cc3dc46p-31) 
        + ((double)in_225)*(((double)0x1.11111498c02e48b35e1b9d912bbc85c8p-7) 
        + ((double)in_225)*(((double)0x1.fe05eedd7b9e3e4667e39d7d1a32babep-29) 
        + ((double)in_225)*(((double)-0x1.a016eaa2be2170df08c562e0f084a754p-13) 
        + ((double)in_225)*(((double)0x1.b3de4606534188ef11f41bef731092aep-28) 
        + ((double)in_225)*(((double)0x1.728c5043d2d7e6a267e29b7ac0ea490cp-19) 
        + ((double)in_225)*(((double)0x1.969990b39d0b540aae96c76e9c11b7f2p-29) 
        + ((double)in_225)*(((double)-0x1.98c0b15a5d4d401f24fb1e551a791a5cp-26) 
        + ((double)in_225)*(((double)0x1.a73226a8e63d63956a70a69ee2444684p-32) 
        + ((double)in_225)*(((double)0x1.0a103bbcaf5f95a5061f84025821a9d6p-32) 
        + ((double)in_225)*((double)0x1.8328374a2e9c2733614929013e076826p-37)))))))))))))));
    double recons_69 = in_226 < 0.0 ? out_81 : ((2*out_81)/(-2));
    return recons_69;
}

double my_core_function_sin_60(double in_230)
{
// (periodic (+ PI PI) (MirrorRight (+ (- (- (- (+ PI PI)) (- (* PI 4) x))) (- (* PI 6))) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))
    int k_76 = (int) floor((((double)in_230)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_229 = ((double)in_230) - k_76*((double)6.283185307179586);
    double in_228 = in_229 < 0.0 ? in_229 : (0.0 - in_229);
    double out_82 = (((double)in_228)*(((double)0x1.00000000003cb0067f0b6b57b15ba676p0) 
        + ((double)in_228)*(((double)0x1.f1539b1f3a3700e4af203ba7fbf5c912p-38) 
        + ((double)in_228)*(((double)-0x1.555555528a598cfe96aae1ebf8325784p-3) 
        + ((double)in_228)*(((double)0x1.04782924118d26ef2e7dc7239cc3dc46p-31) 
        + ((double)in_228)*(((double)0x1.11111498c02e48b35e1b9d912bbc85c8p-7) 
        + ((double)in_228)*(((double)0x1.fe05eedd7b9e3e4667e39d7d1a32babep-29) 
        + ((double)in_228)*(((double)-0x1.a016eaa2be2170df08c562e0f084a754p-13) 
        + ((double)in_228)*(((double)0x1.b3de4606534188ef11f41bef731092aep-28) 
        + ((double)in_228)*(((double)0x1.728c5043d2d7e6a267e29b7ac0ea490cp-19) 
        + ((double)in_228)*(((double)0x1.969990b39d0b540aae96c76e9c11b7f2p-29) 
        + ((double)in_228)*(((double)-0x1.98c0b15a5d4d401f24fb1e551a791a5cp-26) 
        + ((double)in_228)*(((double)0x1.a73226a8e63d63956a70a69ee2444684p-32) 
        + ((double)in_228)*(((double)0x1.0a103bbcaf5f95a5061f84025821a9d6p-32) 
        + ((double)in_228)*((double)0x1.8328374a2e9c2733614929013e076826p-37)))))))))))))));
    double recons_70 = in_229 < 0.0 ? out_82 : ((-((-(M_PI+M_PI))-((M_PI*4)-out_82)))+(-(M_PI*6)));
    return recons_70;
}

double my_core_function_sin_61(double in_233)
{
// (periodic (+ PI PI) (MirrorRight (+ (- (- x 1)) (- 1)) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))
    int k_77 = (int) floor((((double)in_233)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_232 = ((double)in_233) - k_77*((double)6.283185307179586);
    double in_231 = in_232 < 0.0 ? in_232 : (0.0 - in_232);
    double out_83 = (((double)in_231)*(((double)0x1.00000000003cb0067f0b6b57b15ba676p0) 
        + ((double)in_231)*(((double)0x1.f1539b1f3a3700e4af203ba7fbf5c912p-38) 
        + ((double)in_231)*(((double)-0x1.555555528a598cfe96aae1ebf8325784p-3) 
        + ((double)in_231)*(((double)0x1.04782924118d26ef2e7dc7239cc3dc46p-31) 
        + ((double)in_231)*(((double)0x1.11111498c02e48b35e1b9d912bbc85c8p-7) 
        + ((double)in_231)*(((double)0x1.fe05eedd7b9e3e4667e39d7d1a32babep-29) 
        + ((double)in_231)*(((double)-0x1.a016eaa2be2170df08c562e0f084a754p-13) 
        + ((double)in_231)*(((double)0x1.b3de4606534188ef11f41bef731092aep-28) 
        + ((double)in_231)*(((double)0x1.728c5043d2d7e6a267e29b7ac0ea490cp-19) 
        + ((double)in_231)*(((double)0x1.969990b39d0b540aae96c76e9c11b7f2p-29) 
        + ((double)in_231)*(((double)-0x1.98c0b15a5d4d401f24fb1e551a791a5cp-26) 
        + ((double)in_231)*(((double)0x1.a73226a8e63d63956a70a69ee2444684p-32) 
        + ((double)in_231)*(((double)0x1.0a103bbcaf5f95a5061f84025821a9d6p-32) 
        + ((double)in_231)*((double)0x1.8328374a2e9c2733614929013e076826p-37)))))))))))))));
    double recons_71 = in_232 < 0.0 ? out_83 : ((-(out_83-1))+(-1));
    return recons_71;
}

double my_core_function_sin_62(double in_236)
{
// (periodic (+ PI PI) (MirrorRight (- (* PI 6) (+ (+ PI PI) (+ x (* PI 4)))) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))
    int k_78 = (int) floor((((double)in_236)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_235 = ((double)in_236) - k_78*((double)6.283185307179586);
    double in_234 = in_235 < 0.0 ? in_235 : (0.0 - in_235);
    double out_84 = (((double)in_234)*(((double)0x1.00000000003cb0067f0b6b57b15ba676p0) 
        + ((double)in_234)*(((double)0x1.f1539b1f3a3700e4af203ba7fbf5c912p-38) 
        + ((double)in_234)*(((double)-0x1.555555528a598cfe96aae1ebf8325784p-3) 
        + ((double)in_234)*(((double)0x1.04782924118d26ef2e7dc7239cc3dc46p-31) 
        + ((double)in_234)*(((double)0x1.11111498c02e48b35e1b9d912bbc85c8p-7) 
        + ((double)in_234)*(((double)0x1.fe05eedd7b9e3e4667e39d7d1a32babep-29) 
        + ((double)in_234)*(((double)-0x1.a016eaa2be2170df08c562e0f084a754p-13) 
        + ((double)in_234)*(((double)0x1.b3de4606534188ef11f41bef731092aep-28) 
        + ((double)in_234)*(((double)0x1.728c5043d2d7e6a267e29b7ac0ea490cp-19) 
        + ((double)in_234)*(((double)0x1.969990b39d0b540aae96c76e9c11b7f2p-29) 
        + ((double)in_234)*(((double)-0x1.98c0b15a5d4d401f24fb1e551a791a5cp-26) 
        + ((double)in_234)*(((double)0x1.a73226a8e63d63956a70a69ee2444684p-32) 
        + ((double)in_234)*(((double)0x1.0a103bbcaf5f95a5061f84025821a9d6p-32) 
        + ((double)in_234)*((double)0x1.8328374a2e9c2733614929013e076826p-37)))))))))))))));
    double recons_72 = in_235 < 0.0 ? out_84 : ((M_PI*6)-((M_PI+M_PI)+(out_84+(M_PI*4))));
    return recons_72;
}

double my_core_function_sin_63(double in_239)
{
// (periodic (+ PI PI) (MirrorRight (- (- (+ PI PI)) (- x (+ PI PI))) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))
    int k_79 = (int) floor((((double)in_239)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_238 = ((double)in_239) - k_79*((double)6.283185307179586);
    double in_237 = in_238 < 0.0 ? in_238 : (0.0 - in_238);
    double out_85 = (((double)in_237)*(((double)0x1.00000000003cb0067f0b6b57b15ba676p0) 
        + ((double)in_237)*(((double)0x1.f1539b1f3a3700e4af203ba7fbf5c912p-38) 
        + ((double)in_237)*(((double)-0x1.555555528a598cfe96aae1ebf8325784p-3) 
        + ((double)in_237)*(((double)0x1.04782924118d26ef2e7dc7239cc3dc46p-31) 
        + ((double)in_237)*(((double)0x1.11111498c02e48b35e1b9d912bbc85c8p-7) 
        + ((double)in_237)*(((double)0x1.fe05eedd7b9e3e4667e39d7d1a32babep-29) 
        + ((double)in_237)*(((double)-0x1.a016eaa2be2170df08c562e0f084a754p-13) 
        + ((double)in_237)*(((double)0x1.b3de4606534188ef11f41bef731092aep-28) 
        + ((double)in_237)*(((double)0x1.728c5043d2d7e6a267e29b7ac0ea490cp-19) 
        + ((double)in_237)*(((double)0x1.969990b39d0b540aae96c76e9c11b7f2p-29) 
        + ((double)in_237)*(((double)-0x1.98c0b15a5d4d401f24fb1e551a791a5cp-26) 
        + ((double)in_237)*(((double)0x1.a73226a8e63d63956a70a69ee2444684p-32) 
        + ((double)in_237)*(((double)0x1.0a103bbcaf5f95a5061f84025821a9d6p-32) 
        + ((double)in_237)*((double)0x1.8328374a2e9c2733614929013e076826p-37)))))))))))))));
    double recons_73 = in_238 < 0.0 ? out_85 : ((-(M_PI+M_PI))-(out_85-(M_PI+M_PI)));
    return recons_73;
}

double my_core_function_sin_64(double in_242)
{
// (periodic (+ PI PI) (MirrorRight (* (* 2 x) (- (/ 1 2))) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))
    int k_80 = (int) floor((((double)in_242)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_241 = ((double)in_242) - k_80*((double)6.283185307179586);
    double in_240 = in_241 < 0.0 ? in_241 : (0.0 - in_241);
    double out_86 = (((double)in_240)*(((double)0x1.00000000003cb0067f0b6b57b15ba676p0) 
        + ((double)in_240)*(((double)0x1.f1539b1f3a3700e4af203ba7fbf5c912p-38) 
        + ((double)in_240)*(((double)-0x1.555555528a598cfe96aae1ebf8325784p-3) 
        + ((double)in_240)*(((double)0x1.04782924118d26ef2e7dc7239cc3dc46p-31) 
        + ((double)in_240)*(((double)0x1.11111498c02e48b35e1b9d912bbc85c8p-7) 
        + ((double)in_240)*(((double)0x1.fe05eedd7b9e3e4667e39d7d1a32babep-29) 
        + ((double)in_240)*(((double)-0x1.a016eaa2be2170df08c562e0f084a754p-13) 
        + ((double)in_240)*(((double)0x1.b3de4606534188ef11f41bef731092aep-28) 
        + ((double)in_240)*(((double)0x1.728c5043d2d7e6a267e29b7ac0ea490cp-19) 
        + ((double)in_240)*(((double)0x1.969990b39d0b540aae96c76e9c11b7f2p-29) 
        + ((double)in_240)*(((double)-0x1.98c0b15a5d4d401f24fb1e551a791a5cp-26) 
        + ((double)in_240)*(((double)0x1.a73226a8e63d63956a70a69ee2444684p-32) 
        + ((double)in_240)*(((double)0x1.0a103bbcaf5f95a5061f84025821a9d6p-32) 
        + ((double)in_240)*((double)0x1.8328374a2e9c2733614929013e076826p-37)))))))))))))));
    double recons_74 = in_241 < 0.0 ? out_86 : ((2*out_86)*(-(1/2)));
    return recons_74;
}

double my_core_function_sin_65(double in_245)
{
// (periodic (+ PI PI) (MirrorRight (- x) (Horner (MinimaxPolynomial (sin x) [(- PI) 0]))))
    int k_81 = (int) floor((((double)in_245)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_244 = ((double)in_245) - k_81*((double)6.283185307179586);
    double in_243 = in_244 < 0.0 ? in_244 : (0.0 - in_244);
    double out_87 = (((double)in_243)*(((double)0x1.00000000003cb0067f0b6b57b15ba676p0) 
        + ((double)in_243)*(((double)0x1.f1539b1f3a3700e4af203ba7fbf5c912p-38) 
        + ((double)in_243)*(((double)-0x1.555555528a598cfe96aae1ebf8325784p-3) 
        + ((double)in_243)*(((double)0x1.04782924118d26ef2e7dc7239cc3dc46p-31) 
        + ((double)in_243)*(((double)0x1.11111498c02e48b35e1b9d912bbc85c8p-7) 
        + ((double)in_243)*(((double)0x1.fe05eedd7b9e3e4667e39d7d1a32babep-29) 
        + ((double)in_243)*(((double)-0x1.a016eaa2be2170df08c562e0f084a754p-13) 
        + ((double)in_243)*(((double)0x1.b3de4606534188ef11f41bef731092aep-28) 
        + ((double)in_243)*(((double)0x1.728c5043d2d7e6a267e29b7ac0ea490cp-19) 
        + ((double)in_243)*(((double)0x1.969990b39d0b540aae96c76e9c11b7f2p-29) 
        + ((double)in_243)*(((double)-0x1.98c0b15a5d4d401f24fb1e551a791a5cp-26) 
        + ((double)in_243)*(((double)0x1.a73226a8e63d63956a70a69ee2444684p-32) 
        + ((double)in_243)*(((double)0x1.0a103bbcaf5f95a5061f84025821a9d6p-32) 
        + ((double)in_243)*((double)0x1.8328374a2e9c2733614929013e076826p-37)))))))))))))));
    double recons_75 = in_244 < 0.0 ? out_87 : (-out_87);
    return recons_75;
}
