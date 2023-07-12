#include "funcs.h"
#include "table_generation.h"
#include <assert.h>
#include <math.h>

double libm_core_function_cos(double x)
{
    return cos(x);
}

int mpfr_core_function_cos(mpfr_t out, double dx)
{
  static int init_called = 0;
  static mpfr_t x;
  if (!init_called) {
    mpfr_init2(x, ORACLE_PREC);
    init_called = 1;
  }
  mpfr_set_d(x, dx, MPFR_RNDN);
  mpfr_cos(out, x, MPFR_RNDN);
  return 0;
}

double my_core_function_cos_0(double in_3)
{
// (periodic (+ PI PI) (Horner (MinimaxPolynomial (cos x) [0.0 (+ PI PI)])))
    int k_0 = (int) floor((((double)in_3)-((double)0.0))*((double)0.15915494309189535));
    double in_2 = ((double)in_3) - k_0*((double)6.283185307179586);
    double out_2 = (((double)0x1.000000007cd0a022402c759ff01e52e6p0) 
        +((double)in_2)*(((double)-0x1.3c8b880ea00726fe0c339b5a4b275afp-27) 
        + ((double)in_2)*(((double)-0x1.fffff7abe190ad31e274ed20f3bc91e6p-2) 
        + ((double)in_2)*(((double)-0x1.62a5bd3b9ae07454694b87a026a645fep-21) 
        + ((double)in_2)*(((double)0x1.555933c245a5b5a375e48d7831f829fcp-5) 
        + ((double)in_2)*(((double)-0x1.a18e9eb47118e6f0bb9a864cf0fb3984p-19) 
        + ((double)in_2)*(((double)-0x1.6b3020595eb6ce7150fdbc6c3c3b341p-10) 
        + ((double)in_2)*(((double)-0x1.5efed91de575f5d650fb7e2831e35e02p-19) 
        + ((double)in_2)*(((double)0x1.b7d3514bf081d2900d64fed58ada547ep-16) 
        + ((double)in_2)*(((double)-0x1.28b6f65e98932f92fb6bd7a029296952p-21) 
        + ((double)in_2)*(((double)-0x1.fdbcad2405e69420c520b6b79faf8466p-24) 
        + ((double)in_2)*(((double)-0x1.137252db6bb2cbd18745d30a752592cep-25) 
        + ((double)in_2)*(((double)0x1.ca885d7b63706d0f9ef9396cca0a40d6p-28) 
        + ((double)in_2)*(((double)-0x1.d636eb72a7889e9f517978b226f10006p-32) 
        + ((double)in_2)*((double)0x1.561ca214dd0d0a59b193c385e34acbfep-37)))))))))))))));
    return out_2;
}

double my_core_function_cos_1(double in_5)
{
// (periodic (+ PI PI) (Horner (MinimaxPolynomial (cos x) [(/ (* PI (- 2)) 2) (/ (+ PI PI) 2)])))
    int k_1 = (int) floor((((double)in_5)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_4 = ((double)in_5) - k_1*((double)6.283185307179586);
    double out_3 = (((double)0x1.ffffffff065ebfbb57b3f89f52193b38p-1) 
        +((double)in_4)*(((double)0x1.d5f10b611eb527230be1e291be403064p-61) 
        + ((double)in_4)*(((double)-0x1.ffffffe69a5fc21ad211fb4bd8f4d17cp-2) 
        + ((double)in_4)*(((double)-0x1.e64d7e6ed5af01227018ab1d5678869p-59) 
        + ((double)in_4)*(((double)0x1.555553a329324157397d4bce93553238p-5) 
        + ((double)in_4)*(((double)0x1.14f0e853f01496b855ef915d2b3f684ap-58) 
        + ((double)in_4)*(((double)-0x1.6c16953694183aa7e4f9121de417020ap-10) 
        + ((double)in_4)*(((double)-0x1.05d59798ea00015fb8836eec35cb9bp-59) 
        + ((double)in_4)*(((double)0x1.a015945b65231275fcc46722634a08bap-16) 
        + ((double)in_4)*(((double)0x1.d48f1f978d236bc2f4f103cf21bc67ecp-62) 
        + ((double)in_4)*(((double)-0x1.27a73528b785a1a0e98646392ad53f3ep-22) 
        + ((double)in_4)*(((double)-0x1.8960f0a8c956f0048ff8c9a25c543af6p-65) 
        + ((double)in_4)*(((double)0x1.1b2d8d6fcb16697007007b886434c154p-29) 
        + ((double)in_4)*(((double)0x1.f22fdc2e09ca2802e71aed369ac57086p-70) 
        + ((double)in_4)*((double)-0x1.561ca214dd0d0a59b193c386100f143cp-37)))))))))))))));
    return out_3;
}

double my_core_function_cos_2(double in_8)
{
// (periodic (+ PI PI) (MirrorLeft (- x) (Horner (MinimaxPolynomial (cos x) [PI (+ PI PI)]))))
    int k_2 = (int) floor((((double)in_8)-((double)0.0))*((double)0.15915494309189535));
    double in_7 = ((double)in_8) - k_2*((double)6.283185307179586);
    double in_6 = in_7 < 3.141592653589793 ? (3.141592653589793 - in_7) : in_7;
    double out_4 = (((double)0x1.fd29cedb7c8928ceb74ba68de27b0c2ep-1) 
        +((double)in_6)*(((double)0x1.2f725a5e9eba6fbc677be2518ad79944p-6) 
        + ((double)in_6)*(((double)-0x1.0eb296ec25dc1f294ab560d2b717e802p-1) 
        + ((double)in_6)*(((double)0x1.c0103e33d9cc50e1d23414f0d871844cp-6) 
        + ((double)in_6)*(((double)0x1.8584e096e7aba6cdb54d124d80ddcdep-6) 
        + ((double)in_6)*(((double)0x1.16ab3f72308125d4b04723dd784ffa06p-7) 
        + ((double)in_6)*(((double)-0x1.216ecf8ad64dd3ebe61e5fa702f3e03ap-8) 
        + ((double)in_6)*(((double)0x1.ad9af95d804aed792226f9b86534cbb4p-11) 
        + ((double)in_6)*(((double)-0x1.2ea2f8bb853347bc19e68ea45760f6fp-13) 
        + ((double)in_6)*(((double)0x1.ba613e37448e4727069dbdeca4f4e798p-16) 
        + ((double)in_6)*(((double)-0x1.bb208b13f0d20f4a73e7867ca7b1c88p-19) 
        + ((double)in_6)*(((double)0x1.02e9143f24b11f77f5fdd3195531ab1cp-22) 
        + ((double)in_6)*(((double)-0x1.437093a6362b86bf6b1967d76ead4f88p-27) 
        + ((double)in_6)*(((double)0x1.51e689d7e49961272cbda37cf451742ep-33) 
        + ((double)in_6)*((double)-0x1.1b68d90dea4c71fe2240c22fd541c6eap-68)))))))))))))));
    double recons_0 = in_7 < 3.141592653589793 ? (-out_4) : out_4;
    return recons_0;
}

double my_core_function_cos_3(double in_11)
{
// (periodic (+ PI PI) (MirrorRight (- x) (Horner (MinimaxPolynomial (cos x) [0.0 PI]))))
    int k_3 = (int) floor((((double)in_11)-((double)0.0))*((double)0.15915494309189535));
    double in_10 = ((double)in_11) - k_3*((double)6.283185307179586);
    double in_9 = in_10 < 3.141592653589793 ? in_10 : (6.283185307179586 - in_10);
    double out_5 = (((double)0x1.00000000000b0e138153e7fd50f2a69ap0) 
        +((double)in_9)*(((double)-0x1.8b65bce38b6cf528619151bf6dfa30a2p-38) 
        + ((double)in_9)*(((double)-0x1.fffffffdb5663560dfc6c06828f7a318p-2) 
        + ((double)in_9)*(((double)-0x1.5764631cd535d6cdd8043ad093247626p-30) 
        + ((double)in_9)*(((double)0x1.5555589f205f14e344fea97c7981eb06p-5) 
        + ((double)in_9)*(((double)-0x1.3676fa2d21e3aa9567c38f3bcaeb4532p-26) 
        + ((double)in_9)*(((double)-0x1.6c146c24e39552b7ff342f0b3346c8cap-10) 
        + ((double)in_9)*(((double)-0x1.89606f8f54c67e2851dd0f27c9ac20fap-25) 
        + ((double)in_9)*(((double)0x1.a0d0ad28acd7cfb93962ff19bbe2b4aep-16) 
        + ((double)in_9)*(((double)-0x1.e5a0e0b7678f96b49fd8d6b6f59d08eep-26) 
        + ((double)in_9)*(((double)-0x1.196dfb008c61cb280e95aa335bfc41c6p-22) 
        + ((double)in_9)*(((double)-0x1.386a1fcf991c31ea523c63793b593fecp-28) 
        + ((double)in_9)*(((double)0x1.af40c4d9ace2bf38acc1337e7aebbe6p-29) 
        + ((double)in_9)*(((double)-0x1.51e689d1ce7943e7401c49c67f9814eep-33) 
        + ((double)in_9)*((double)0x1.1b68d90dea4c5a798d2c3262d92b911p-68)))))))))))))));
    double recons_1 = in_10 < 3.141592653589793 ? out_5 : (-out_5);
    return recons_1;
}

double my_core_function_cos_4(double in_14)
{
// (periodic (+ PI PI) (MirrorLeft (- (* x (- 2)) (- (* x (- 2)) x)) (Horner (MinimaxPolynomial (cos x) [0 (/ (+ PI PI) 2)]))))
    int k_4 = (int) floor((((double)in_14)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_13 = ((double)in_14) - k_4*((double)6.283185307179586);
    double in_12 = in_13 < 0.0 ? (0.0 - in_13) : in_13;
    double out_6 = (((double)0x1.00000000000b0e138153e7fd50f2a69ap0) 
        +((double)in_12)*(((double)-0x1.8b65bce38b6cf528619151bf6dfa30a2p-38) 
        + ((double)in_12)*(((double)-0x1.fffffffdb5663560dfc6c06828f7a318p-2) 
        + ((double)in_12)*(((double)-0x1.5764631cd535d6cdd8043ad093247626p-30) 
        + ((double)in_12)*(((double)0x1.5555589f205f14e344fea97c7981eb06p-5) 
        + ((double)in_12)*(((double)-0x1.3676fa2d21e3aa9567c38f3bcaeb4532p-26) 
        + ((double)in_12)*(((double)-0x1.6c146c24e39552b7ff342f0b3346c8cap-10) 
        + ((double)in_12)*(((double)-0x1.89606f8f54c67e2851dd0f27c9ac20fap-25) 
        + ((double)in_12)*(((double)0x1.a0d0ad28acd7cfb93962ff19bbe2b4aep-16) 
        + ((double)in_12)*(((double)-0x1.e5a0e0b7678f96b49fd8d6b6f59d08eep-26) 
        + ((double)in_12)*(((double)-0x1.196dfb008c61cb280e95aa335bfc41c6p-22) 
        + ((double)in_12)*(((double)-0x1.386a1fcf991c31ea523c63793b593fecp-28) 
        + ((double)in_12)*(((double)0x1.af40c4d9ace2bf38acc1337e7aebbe6p-29) 
        + ((double)in_12)*(((double)-0x1.51e689d1ce7943e7401c49c67f9814eep-33) 
        + ((double)in_12)*((double)0x1.1b68d90dea4c5a798d2c3262d92b911p-68)))))))))))))));
    double recons_2 = in_13 < 0.0 ? ((out_6*(-2))-((out_6*(-2))-out_6)) : out_6;
    return recons_2;
}

double my_core_function_cos_5(double in_17)
{
// (periodic (+ PI PI) (MirrorLeft (- (+ (* x 2) (* x 2)) (- x (* x (- 2)))) (Horner (MinimaxPolynomial (cos x) [0 (/ (+ PI PI) 2)]))))
    int k_5 = (int) floor((((double)in_17)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_16 = ((double)in_17) - k_5*((double)6.283185307179586);
    double in_15 = in_16 < 0.0 ? (0.0 - in_16) : in_16;
    double out_7 = (((double)0x1.00000000000b0e138153e7fd50f2a69ap0) 
        +((double)in_15)*(((double)-0x1.8b65bce38b6cf528619151bf6dfa30a2p-38) 
        + ((double)in_15)*(((double)-0x1.fffffffdb5663560dfc6c06828f7a318p-2) 
        + ((double)in_15)*(((double)-0x1.5764631cd535d6cdd8043ad093247626p-30) 
        + ((double)in_15)*(((double)0x1.5555589f205f14e344fea97c7981eb06p-5) 
        + ((double)in_15)*(((double)-0x1.3676fa2d21e3aa9567c38f3bcaeb4532p-26) 
        + ((double)in_15)*(((double)-0x1.6c146c24e39552b7ff342f0b3346c8cap-10) 
        + ((double)in_15)*(((double)-0x1.89606f8f54c67e2851dd0f27c9ac20fap-25) 
        + ((double)in_15)*(((double)0x1.a0d0ad28acd7cfb93962ff19bbe2b4aep-16) 
        + ((double)in_15)*(((double)-0x1.e5a0e0b7678f96b49fd8d6b6f59d08eep-26) 
        + ((double)in_15)*(((double)-0x1.196dfb008c61cb280e95aa335bfc41c6p-22) 
        + ((double)in_15)*(((double)-0x1.386a1fcf991c31ea523c63793b593fecp-28) 
        + ((double)in_15)*(((double)0x1.af40c4d9ace2bf38acc1337e7aebbe6p-29) 
        + ((double)in_15)*(((double)-0x1.51e689d1ce7943e7401c49c67f9814eep-33) 
        + ((double)in_15)*((double)0x1.1b68d90dea4c5a798d2c3262d92b911p-68)))))))))))))));
    double recons_3 = in_16 < 0.0 ? (((out_7*2)+(out_7*2))-(out_7-(out_7*(-2)))) : out_7;
    return recons_3;
}

double my_core_function_cos_6(double in_20)
{
// (periodic (+ PI PI) (MirrorLeft (- (* x 2) x) (Horner (MinimaxPolynomial (cos x) [0 (/ (+ PI PI) 2)]))))
    int k_6 = (int) floor((((double)in_20)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_19 = ((double)in_20) - k_6*((double)6.283185307179586);
    double in_18 = in_19 < 0.0 ? (0.0 - in_19) : in_19;
    double out_8 = (((double)0x1.00000000000b0e138153e7fd50f2a69ap0) 
        +((double)in_18)*(((double)-0x1.8b65bce38b6cf528619151bf6dfa30a2p-38) 
        + ((double)in_18)*(((double)-0x1.fffffffdb5663560dfc6c06828f7a318p-2) 
        + ((double)in_18)*(((double)-0x1.5764631cd535d6cdd8043ad093247626p-30) 
        + ((double)in_18)*(((double)0x1.5555589f205f14e344fea97c7981eb06p-5) 
        + ((double)in_18)*(((double)-0x1.3676fa2d21e3aa9567c38f3bcaeb4532p-26) 
        + ((double)in_18)*(((double)-0x1.6c146c24e39552b7ff342f0b3346c8cap-10) 
        + ((double)in_18)*(((double)-0x1.89606f8f54c67e2851dd0f27c9ac20fap-25) 
        + ((double)in_18)*(((double)0x1.a0d0ad28acd7cfb93962ff19bbe2b4aep-16) 
        + ((double)in_18)*(((double)-0x1.e5a0e0b7678f96b49fd8d6b6f59d08eep-26) 
        + ((double)in_18)*(((double)-0x1.196dfb008c61cb280e95aa335bfc41c6p-22) 
        + ((double)in_18)*(((double)-0x1.386a1fcf991c31ea523c63793b593fecp-28) 
        + ((double)in_18)*(((double)0x1.af40c4d9ace2bf38acc1337e7aebbe6p-29) 
        + ((double)in_18)*(((double)-0x1.51e689d1ce7943e7401c49c67f9814eep-33) 
        + ((double)in_18)*((double)0x1.1b68d90dea4c5a798d2c3262d92b911p-68)))))))))))))));
    double recons_4 = in_19 < 0.0 ? ((out_8*2)-out_8) : out_8;
    return recons_4;
}

double my_core_function_cos_7(double in_23)
{
// (periodic (+ PI PI) (MirrorLeft (/ (* x 2) 2) (Horner (MinimaxPolynomial (cos x) [0 (/ (+ PI PI) 2)]))))
    int k_7 = (int) floor((((double)in_23)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_22 = ((double)in_23) - k_7*((double)6.283185307179586);
    double in_21 = in_22 < 0.0 ? (0.0 - in_22) : in_22;
    double out_9 = (((double)0x1.00000000000b0e138153e7fd50f2a69ap0) 
        +((double)in_21)*(((double)-0x1.8b65bce38b6cf528619151bf6dfa30a2p-38) 
        + ((double)in_21)*(((double)-0x1.fffffffdb5663560dfc6c06828f7a318p-2) 
        + ((double)in_21)*(((double)-0x1.5764631cd535d6cdd8043ad093247626p-30) 
        + ((double)in_21)*(((double)0x1.5555589f205f14e344fea97c7981eb06p-5) 
        + ((double)in_21)*(((double)-0x1.3676fa2d21e3aa9567c38f3bcaeb4532p-26) 
        + ((double)in_21)*(((double)-0x1.6c146c24e39552b7ff342f0b3346c8cap-10) 
        + ((double)in_21)*(((double)-0x1.89606f8f54c67e2851dd0f27c9ac20fap-25) 
        + ((double)in_21)*(((double)0x1.a0d0ad28acd7cfb93962ff19bbe2b4aep-16) 
        + ((double)in_21)*(((double)-0x1.e5a0e0b7678f96b49fd8d6b6f59d08eep-26) 
        + ((double)in_21)*(((double)-0x1.196dfb008c61cb280e95aa335bfc41c6p-22) 
        + ((double)in_21)*(((double)-0x1.386a1fcf991c31ea523c63793b593fecp-28) 
        + ((double)in_21)*(((double)0x1.af40c4d9ace2bf38acc1337e7aebbe6p-29) 
        + ((double)in_21)*(((double)-0x1.51e689d1ce7943e7401c49c67f9814eep-33) 
        + ((double)in_21)*((double)0x1.1b68d90dea4c5a798d2c3262d92b911p-68)))))))))))))));
    double recons_5 = in_22 < 0.0 ? ((out_9*2)/2) : out_9;
    return recons_5;
}

double my_core_function_cos_8(double in_26)
{
// (periodic (+ PI PI) (MirrorLeft (- (- x (* x (- 2))) (* x 2)) (Horner (MinimaxPolynomial (cos x) [0 (/ (+ PI PI) 2)]))))
    int k_8 = (int) floor((((double)in_26)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_25 = ((double)in_26) - k_8*((double)6.283185307179586);
    double in_24 = in_25 < 0.0 ? (0.0 - in_25) : in_25;
    double out_10 = (((double)0x1.00000000000b0e138153e7fd50f2a69ap0) 
        +((double)in_24)*(((double)-0x1.8b65bce38b6cf528619151bf6dfa30a2p-38) 
        + ((double)in_24)*(((double)-0x1.fffffffdb5663560dfc6c06828f7a318p-2) 
        + ((double)in_24)*(((double)-0x1.5764631cd535d6cdd8043ad093247626p-30) 
        + ((double)in_24)*(((double)0x1.5555589f205f14e344fea97c7981eb06p-5) 
        + ((double)in_24)*(((double)-0x1.3676fa2d21e3aa9567c38f3bcaeb4532p-26) 
        + ((double)in_24)*(((double)-0x1.6c146c24e39552b7ff342f0b3346c8cap-10) 
        + ((double)in_24)*(((double)-0x1.89606f8f54c67e2851dd0f27c9ac20fap-25) 
        + ((double)in_24)*(((double)0x1.a0d0ad28acd7cfb93962ff19bbe2b4aep-16) 
        + ((double)in_24)*(((double)-0x1.e5a0e0b7678f96b49fd8d6b6f59d08eep-26) 
        + ((double)in_24)*(((double)-0x1.196dfb008c61cb280e95aa335bfc41c6p-22) 
        + ((double)in_24)*(((double)-0x1.386a1fcf991c31ea523c63793b593fecp-28) 
        + ((double)in_24)*(((double)0x1.af40c4d9ace2bf38acc1337e7aebbe6p-29) 
        + ((double)in_24)*(((double)-0x1.51e689d1ce7943e7401c49c67f9814eep-33) 
        + ((double)in_24)*((double)0x1.1b68d90dea4c5a798d2c3262d92b911p-68)))))))))))))));
    double recons_6 = in_25 < 0.0 ? ((out_10-(out_10*(-2)))-(out_10*2)) : out_10;
    return recons_6;
}

double my_core_function_cos_9(double in_29)
{
// (periodic (+ PI PI) (MirrorLeft (* x (pow x 0)) (Horner (MinimaxPolynomial (cos x) [0 (/ (+ PI PI) 2)]))))
    int k_9 = (int) floor((((double)in_29)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_28 = ((double)in_29) - k_9*((double)6.283185307179586);
    double in_27 = in_28 < 0.0 ? (0.0 - in_28) : in_28;
    double out_11 = (((double)0x1.00000000000b0e138153e7fd50f2a69ap0) 
        +((double)in_27)*(((double)-0x1.8b65bce38b6cf528619151bf6dfa30a2p-38) 
        + ((double)in_27)*(((double)-0x1.fffffffdb5663560dfc6c06828f7a318p-2) 
        + ((double)in_27)*(((double)-0x1.5764631cd535d6cdd8043ad093247626p-30) 
        + ((double)in_27)*(((double)0x1.5555589f205f14e344fea97c7981eb06p-5) 
        + ((double)in_27)*(((double)-0x1.3676fa2d21e3aa9567c38f3bcaeb4532p-26) 
        + ((double)in_27)*(((double)-0x1.6c146c24e39552b7ff342f0b3346c8cap-10) 
        + ((double)in_27)*(((double)-0x1.89606f8f54c67e2851dd0f27c9ac20fap-25) 
        + ((double)in_27)*(((double)0x1.a0d0ad28acd7cfb93962ff19bbe2b4aep-16) 
        + ((double)in_27)*(((double)-0x1.e5a0e0b7678f96b49fd8d6b6f59d08eep-26) 
        + ((double)in_27)*(((double)-0x1.196dfb008c61cb280e95aa335bfc41c6p-22) 
        + ((double)in_27)*(((double)-0x1.386a1fcf991c31ea523c63793b593fecp-28) 
        + ((double)in_27)*(((double)0x1.af40c4d9ace2bf38acc1337e7aebbe6p-29) 
        + ((double)in_27)*(((double)-0x1.51e689d1ce7943e7401c49c67f9814eep-33) 
        + ((double)in_27)*((double)0x1.1b68d90dea4c5a798d2c3262d92b911p-68)))))))))))))));
    double recons_7 = in_28 < 0.0 ? (out_11*pow(out_11, 0)) : out_11;
    return recons_7;
}

double my_core_function_cos_10(double in_32)
{
// (periodic (+ PI PI) (MirrorLeft (+ (+ (* x 2) (* x 2)) (- (* x (- 2)) x)) (Horner (MinimaxPolynomial (cos x) [0 (/ (+ PI PI) 2)]))))
    int k_10 = (int) floor((((double)in_32)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_31 = ((double)in_32) - k_10*((double)6.283185307179586);
    double in_30 = in_31 < 0.0 ? (0.0 - in_31) : in_31;
    double out_12 = (((double)0x1.00000000000b0e138153e7fd50f2a69ap0) 
        +((double)in_30)*(((double)-0x1.8b65bce38b6cf528619151bf6dfa30a2p-38) 
        + ((double)in_30)*(((double)-0x1.fffffffdb5663560dfc6c06828f7a318p-2) 
        + ((double)in_30)*(((double)-0x1.5764631cd535d6cdd8043ad093247626p-30) 
        + ((double)in_30)*(((double)0x1.5555589f205f14e344fea97c7981eb06p-5) 
        + ((double)in_30)*(((double)-0x1.3676fa2d21e3aa9567c38f3bcaeb4532p-26) 
        + ((double)in_30)*(((double)-0x1.6c146c24e39552b7ff342f0b3346c8cap-10) 
        + ((double)in_30)*(((double)-0x1.89606f8f54c67e2851dd0f27c9ac20fap-25) 
        + ((double)in_30)*(((double)0x1.a0d0ad28acd7cfb93962ff19bbe2b4aep-16) 
        + ((double)in_30)*(((double)-0x1.e5a0e0b7678f96b49fd8d6b6f59d08eep-26) 
        + ((double)in_30)*(((double)-0x1.196dfb008c61cb280e95aa335bfc41c6p-22) 
        + ((double)in_30)*(((double)-0x1.386a1fcf991c31ea523c63793b593fecp-28) 
        + ((double)in_30)*(((double)0x1.af40c4d9ace2bf38acc1337e7aebbe6p-29) 
        + ((double)in_30)*(((double)-0x1.51e689d1ce7943e7401c49c67f9814eep-33) 
        + ((double)in_30)*((double)0x1.1b68d90dea4c5a798d2c3262d92b911p-68)))))))))))))));
    double recons_8 = in_31 < 0.0 ? (((out_12*2)+(out_12*2))+((out_12*(-2))-out_12)) : out_12;
    return recons_8;
}

double my_core_function_cos_11(double in_35)
{
// (periodic (+ PI PI) (MirrorRight (- (* x (- 2)) (- (* x (- 2)) x)) (Horner (MinimaxPolynomial (cos x) [(/ (* PI (- 2)) 2) 0]))))
    int k_11 = (int) floor((((double)in_35)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_34 = ((double)in_35) - k_11*((double)6.283185307179586);
    double in_33 = in_34 < 0.0 ? in_34 : (0.0 - in_34);
    double out_13 = (((double)0x1.00000000000b0e138153e7fd50f2a69ap0) 
        +((double)in_33)*(((double)0x1.8b65bcc59cbfba6f8ffcd3efdf662c54p-38) 
        + ((double)in_33)*(((double)-0x1.fffffffdb56635861701bba08113cfc2p-2) 
        + ((double)in_33)*(((double)0x1.57646307e4887202aee54e059a094af4p-30) 
        + ((double)in_33)*(((double)0x1.5555589f205edcbfec88d8dfcfa28264p-5) 
        + ((double)in_33)*(((double)0x1.3676fa1752a11de948671ca654d9aba2p-26) 
        + ((double)in_33)*(((double)-0x1.6c146c24e3bedb02571c120e1b22c682p-10) 
        + ((double)in_33)*(((double)0x1.89606f75a52e3307af0d39163fff4118p-25) 
        + ((double)in_33)*(((double)0x1.a0d0ad28a21ce51009d34e3c84e2626ap-16) 
        + ((double)in_33)*(((double)0x1.e5a0e09eb136bf39f595a0e0569606f4p-26) 
        + ((double)in_33)*(((double)-0x1.196dfb0129a2577a9229b41cf8d9b2cep-22) 
        + ((double)in_33)*(((double)0x1.386a1fc4fbf9bf256b23a2cc0cb3f384p-28) 
        + ((double)in_33)*(((double)0x1.af40c4d5f5b98e886b87f3e1ef81937ap-29) 
        + ((double)in_33)*(((double)0x1.51e689cbb85926a7537bb095ea8746dep-33) 
        + ((double)in_33)*((double)-0x1.1b68d90dea4c5980f86460aee7db085p-68)))))))))))))));
    double recons_9 = in_34 < 0.0 ? out_13 : ((out_13*(-2))-((out_13*(-2))-out_13));
    return recons_9;
}

double my_core_function_cos_12(double in_38)
{
// (periodic (+ PI PI) (MirrorRight (- (+ (* x 2) (* x 2)) (- x (* x (- 2)))) (Horner (MinimaxPolynomial (cos x) [(/ (* PI (- 2)) 2) 0]))))
    int k_12 = (int) floor((((double)in_38)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_37 = ((double)in_38) - k_12*((double)6.283185307179586);
    double in_36 = in_37 < 0.0 ? in_37 : (0.0 - in_37);
    double out_14 = (((double)0x1.00000000000b0e138153e7fd50f2a69ap0) 
        +((double)in_36)*(((double)0x1.8b65bcc59cbfba6f8ffcd3efdf662c54p-38) 
        + ((double)in_36)*(((double)-0x1.fffffffdb56635861701bba08113cfc2p-2) 
        + ((double)in_36)*(((double)0x1.57646307e4887202aee54e059a094af4p-30) 
        + ((double)in_36)*(((double)0x1.5555589f205edcbfec88d8dfcfa28264p-5) 
        + ((double)in_36)*(((double)0x1.3676fa1752a11de948671ca654d9aba2p-26) 
        + ((double)in_36)*(((double)-0x1.6c146c24e3bedb02571c120e1b22c682p-10) 
        + ((double)in_36)*(((double)0x1.89606f75a52e3307af0d39163fff4118p-25) 
        + ((double)in_36)*(((double)0x1.a0d0ad28a21ce51009d34e3c84e2626ap-16) 
        + ((double)in_36)*(((double)0x1.e5a0e09eb136bf39f595a0e0569606f4p-26) 
        + ((double)in_36)*(((double)-0x1.196dfb0129a2577a9229b41cf8d9b2cep-22) 
        + ((double)in_36)*(((double)0x1.386a1fc4fbf9bf256b23a2cc0cb3f384p-28) 
        + ((double)in_36)*(((double)0x1.af40c4d5f5b98e886b87f3e1ef81937ap-29) 
        + ((double)in_36)*(((double)0x1.51e689cbb85926a7537bb095ea8746dep-33) 
        + ((double)in_36)*((double)-0x1.1b68d90dea4c5980f86460aee7db085p-68)))))))))))))));
    double recons_10 = in_37 < 0.0 ? out_14 : (((out_14*2)+(out_14*2))-(out_14-(out_14*(-2))));
    return recons_10;
}

double my_core_function_cos_13(double in_41)
{
// (periodic (+ PI PI) (MirrorRight (- (* x 2) x) (Horner (MinimaxPolynomial (cos x) [(/ (* PI (- 2)) 2) 0]))))
    int k_13 = (int) floor((((double)in_41)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_40 = ((double)in_41) - k_13*((double)6.283185307179586);
    double in_39 = in_40 < 0.0 ? in_40 : (0.0 - in_40);
    double out_15 = (((double)0x1.00000000000b0e138153e7fd50f2a69ap0) 
        +((double)in_39)*(((double)0x1.8b65bcc59cbfba6f8ffcd3efdf662c54p-38) 
        + ((double)in_39)*(((double)-0x1.fffffffdb56635861701bba08113cfc2p-2) 
        + ((double)in_39)*(((double)0x1.57646307e4887202aee54e059a094af4p-30) 
        + ((double)in_39)*(((double)0x1.5555589f205edcbfec88d8dfcfa28264p-5) 
        + ((double)in_39)*(((double)0x1.3676fa1752a11de948671ca654d9aba2p-26) 
        + ((double)in_39)*(((double)-0x1.6c146c24e3bedb02571c120e1b22c682p-10) 
        + ((double)in_39)*(((double)0x1.89606f75a52e3307af0d39163fff4118p-25) 
        + ((double)in_39)*(((double)0x1.a0d0ad28a21ce51009d34e3c84e2626ap-16) 
        + ((double)in_39)*(((double)0x1.e5a0e09eb136bf39f595a0e0569606f4p-26) 
        + ((double)in_39)*(((double)-0x1.196dfb0129a2577a9229b41cf8d9b2cep-22) 
        + ((double)in_39)*(((double)0x1.386a1fc4fbf9bf256b23a2cc0cb3f384p-28) 
        + ((double)in_39)*(((double)0x1.af40c4d5f5b98e886b87f3e1ef81937ap-29) 
        + ((double)in_39)*(((double)0x1.51e689cbb85926a7537bb095ea8746dep-33) 
        + ((double)in_39)*((double)-0x1.1b68d90dea4c5980f86460aee7db085p-68)))))))))))))));
    double recons_11 = in_40 < 0.0 ? out_15 : ((out_15*2)-out_15);
    return recons_11;
}

double my_core_function_cos_14(double in_44)
{
// (periodic (+ PI PI) (MirrorRight (/ (* x 2) 2) (Horner (MinimaxPolynomial (cos x) [(/ (* PI (- 2)) 2) 0]))))
    int k_14 = (int) floor((((double)in_44)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_43 = ((double)in_44) - k_14*((double)6.283185307179586);
    double in_42 = in_43 < 0.0 ? in_43 : (0.0 - in_43);
    double out_16 = (((double)0x1.00000000000b0e138153e7fd50f2a69ap0) 
        +((double)in_42)*(((double)0x1.8b65bcc59cbfba6f8ffcd3efdf662c54p-38) 
        + ((double)in_42)*(((double)-0x1.fffffffdb56635861701bba08113cfc2p-2) 
        + ((double)in_42)*(((double)0x1.57646307e4887202aee54e059a094af4p-30) 
        + ((double)in_42)*(((double)0x1.5555589f205edcbfec88d8dfcfa28264p-5) 
        + ((double)in_42)*(((double)0x1.3676fa1752a11de948671ca654d9aba2p-26) 
        + ((double)in_42)*(((double)-0x1.6c146c24e3bedb02571c120e1b22c682p-10) 
        + ((double)in_42)*(((double)0x1.89606f75a52e3307af0d39163fff4118p-25) 
        + ((double)in_42)*(((double)0x1.a0d0ad28a21ce51009d34e3c84e2626ap-16) 
        + ((double)in_42)*(((double)0x1.e5a0e09eb136bf39f595a0e0569606f4p-26) 
        + ((double)in_42)*(((double)-0x1.196dfb0129a2577a9229b41cf8d9b2cep-22) 
        + ((double)in_42)*(((double)0x1.386a1fc4fbf9bf256b23a2cc0cb3f384p-28) 
        + ((double)in_42)*(((double)0x1.af40c4d5f5b98e886b87f3e1ef81937ap-29) 
        + ((double)in_42)*(((double)0x1.51e689cbb85926a7537bb095ea8746dep-33) 
        + ((double)in_42)*((double)-0x1.1b68d90dea4c5980f86460aee7db085p-68)))))))))))))));
    double recons_12 = in_43 < 0.0 ? out_16 : ((out_16*2)/2);
    return recons_12;
}

double my_core_function_cos_15(double in_47)
{
// (periodic (+ PI PI) (MirrorRight (- (- x (* x (- 2))) (* x 2)) (Horner (MinimaxPolynomial (cos x) [(/ (* PI (- 2)) 2) 0]))))
    int k_15 = (int) floor((((double)in_47)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_46 = ((double)in_47) - k_15*((double)6.283185307179586);
    double in_45 = in_46 < 0.0 ? in_46 : (0.0 - in_46);
    double out_17 = (((double)0x1.00000000000b0e138153e7fd50f2a69ap0) 
        +((double)in_45)*(((double)0x1.8b65bcc59cbfba6f8ffcd3efdf662c54p-38) 
        + ((double)in_45)*(((double)-0x1.fffffffdb56635861701bba08113cfc2p-2) 
        + ((double)in_45)*(((double)0x1.57646307e4887202aee54e059a094af4p-30) 
        + ((double)in_45)*(((double)0x1.5555589f205edcbfec88d8dfcfa28264p-5) 
        + ((double)in_45)*(((double)0x1.3676fa1752a11de948671ca654d9aba2p-26) 
        + ((double)in_45)*(((double)-0x1.6c146c24e3bedb02571c120e1b22c682p-10) 
        + ((double)in_45)*(((double)0x1.89606f75a52e3307af0d39163fff4118p-25) 
        + ((double)in_45)*(((double)0x1.a0d0ad28a21ce51009d34e3c84e2626ap-16) 
        + ((double)in_45)*(((double)0x1.e5a0e09eb136bf39f595a0e0569606f4p-26) 
        + ((double)in_45)*(((double)-0x1.196dfb0129a2577a9229b41cf8d9b2cep-22) 
        + ((double)in_45)*(((double)0x1.386a1fc4fbf9bf256b23a2cc0cb3f384p-28) 
        + ((double)in_45)*(((double)0x1.af40c4d5f5b98e886b87f3e1ef81937ap-29) 
        + ((double)in_45)*(((double)0x1.51e689cbb85926a7537bb095ea8746dep-33) 
        + ((double)in_45)*((double)-0x1.1b68d90dea4c5980f86460aee7db085p-68)))))))))))))));
    double recons_13 = in_46 < 0.0 ? out_17 : ((out_17-(out_17*(-2)))-(out_17*2));
    return recons_13;
}

double my_core_function_cos_16(double in_50)
{
// (periodic (+ PI PI) (MirrorRight (* x (pow x 0)) (Horner (MinimaxPolynomial (cos x) [(/ (* PI (- 2)) 2) 0]))))
    int k_16 = (int) floor((((double)in_50)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_49 = ((double)in_50) - k_16*((double)6.283185307179586);
    double in_48 = in_49 < 0.0 ? in_49 : (0.0 - in_49);
    double out_18 = (((double)0x1.00000000000b0e138153e7fd50f2a69ap0) 
        +((double)in_48)*(((double)0x1.8b65bcc59cbfba6f8ffcd3efdf662c54p-38) 
        + ((double)in_48)*(((double)-0x1.fffffffdb56635861701bba08113cfc2p-2) 
        + ((double)in_48)*(((double)0x1.57646307e4887202aee54e059a094af4p-30) 
        + ((double)in_48)*(((double)0x1.5555589f205edcbfec88d8dfcfa28264p-5) 
        + ((double)in_48)*(((double)0x1.3676fa1752a11de948671ca654d9aba2p-26) 
        + ((double)in_48)*(((double)-0x1.6c146c24e3bedb02571c120e1b22c682p-10) 
        + ((double)in_48)*(((double)0x1.89606f75a52e3307af0d39163fff4118p-25) 
        + ((double)in_48)*(((double)0x1.a0d0ad28a21ce51009d34e3c84e2626ap-16) 
        + ((double)in_48)*(((double)0x1.e5a0e09eb136bf39f595a0e0569606f4p-26) 
        + ((double)in_48)*(((double)-0x1.196dfb0129a2577a9229b41cf8d9b2cep-22) 
        + ((double)in_48)*(((double)0x1.386a1fc4fbf9bf256b23a2cc0cb3f384p-28) 
        + ((double)in_48)*(((double)0x1.af40c4d5f5b98e886b87f3e1ef81937ap-29) 
        + ((double)in_48)*(((double)0x1.51e689cbb85926a7537bb095ea8746dep-33) 
        + ((double)in_48)*((double)-0x1.1b68d90dea4c5980f86460aee7db085p-68)))))))))))))));
    double recons_14 = in_49 < 0.0 ? out_18 : (out_18*pow(out_18, 0));
    return recons_14;
}

double my_core_function_cos_17(double in_53)
{
// (periodic (+ PI PI) (MirrorRight (+ (+ (* x 2) (* x 2)) (- (* x (- 2)) x)) (Horner (MinimaxPolynomial (cos x) [(/ (* PI (- 2)) 2) 0]))))
    int k_17 = (int) floor((((double)in_53)-((double)-3.141592653589793))*((double)0.15915494309189535));
    double in_52 = ((double)in_53) - k_17*((double)6.283185307179586);
    double in_51 = in_52 < 0.0 ? in_52 : (0.0 - in_52);
    double out_19 = (((double)0x1.00000000000b0e138153e7fd50f2a69ap0) 
        +((double)in_51)*(((double)0x1.8b65bcc59cbfba6f8ffcd3efdf662c54p-38) 
        + ((double)in_51)*(((double)-0x1.fffffffdb56635861701bba08113cfc2p-2) 
        + ((double)in_51)*(((double)0x1.57646307e4887202aee54e059a094af4p-30) 
        + ((double)in_51)*(((double)0x1.5555589f205edcbfec88d8dfcfa28264p-5) 
        + ((double)in_51)*(((double)0x1.3676fa1752a11de948671ca654d9aba2p-26) 
        + ((double)in_51)*(((double)-0x1.6c146c24e3bedb02571c120e1b22c682p-10) 
        + ((double)in_51)*(((double)0x1.89606f75a52e3307af0d39163fff4118p-25) 
        + ((double)in_51)*(((double)0x1.a0d0ad28a21ce51009d34e3c84e2626ap-16) 
        + ((double)in_51)*(((double)0x1.e5a0e09eb136bf39f595a0e0569606f4p-26) 
        + ((double)in_51)*(((double)-0x1.196dfb0129a2577a9229b41cf8d9b2cep-22) 
        + ((double)in_51)*(((double)0x1.386a1fc4fbf9bf256b23a2cc0cb3f384p-28) 
        + ((double)in_51)*(((double)0x1.af40c4d5f5b98e886b87f3e1ef81937ap-29) 
        + ((double)in_51)*(((double)0x1.51e689cbb85926a7537bb095ea8746dep-33) 
        + ((double)in_51)*((double)-0x1.1b68d90dea4c5980f86460aee7db085p-68)))))))))))))));
    double recons_15 = in_52 < 0.0 ? out_19 : (((out_19*2)+(out_19*2))+((out_19*(-2))-out_19));
    return recons_15;
}
