/*
 * Heavily modified source from the VDT math library
 * Modifications were made to allow the file to be compiled on its own.
 */

#include <math.h>
#include <stdint.h>

const double ONEOPIO4 = 4./M_PI;

// double precision constants

const double DP1sc = 7.85398125648498535156E-1;
const double DP2sc = 3.77489470793079817668E-8;
const double DP3sc = 2.69515142907905952645E-15;

const double C1sin = 1.58962301576546568060E-10;
const double C2sin =-2.50507477628578072866E-8;
const double C3sin = 2.75573136213857245213E-6;
const double C4sin =-1.98412698295895385996E-4;
const double C5sin = 8.33333333332211858878E-3;
const double C6sin =-1.66666666666666307295E-1;

const double C1cos =-1.13585365213876817300E-11;
const double C2cos = 2.08757008419747316778E-9;
const double C3cos =-2.75573141792967388112E-7;
const double C4cos = 2.48015872888517045348E-5;
const double C5cos =-1.38888888888730564116E-3;
const double C6cos = 4.16666666666665929218E-2;

const double DP1 = 7.853981554508209228515625E-1;
const double DP2 = 7.94662735614792836714E-9;
const double DP3 = 3.06161699786838294307E-17;

//------------------------------------------------------------------------------

inline double get_sin_px(const double x){
	double px=C1sin;
	px *= x;
	px += C2sin;
	px *= x;
	px += C3sin;
	px *= x;
	px += C4sin;
	px *= x;
	px += C5sin;
	px *= x;
	px += C6sin;
	return px;
}

//------------------------------------------------------------------------------

inline double get_cos_px(const double x){
	double px=C1cos;
	px *= x;
	px += C2cos;
	px *= x;
	px += C3cos;
	px *= x;
	px += C4cos;
	px *= x;
	px += C5cos;
	px *= x;
	px += C6cos;
	return px;
}

//------------------------------------------------------------------------------
/// Reduce to 0 to 45
inline double reduce2quadrant(double x, int32_t* quad) {

    x = fabs(x);
    *quad = (int) (ONEOPIO4 * x); // always positive, so (int) == std::floor
    *quad = (*quad+1) & (~1);
    const double y = (double) (*quad);
    // Extended precision modular arithmetic
    return ((x - y * DP1) - y * DP2) - y * DP3;
  }

//------------------------------------------------------------------------------
/// Sincos only for -45deg < x < 45deg
inline void fast_sincos_m45_45( const double z, double * s, double *c ) {

    double zz = z * z;
    *s = z  +  z * zz * get_sin_px(zz);
    *c = 1.0 - zz * .5 + zz * zz * get_cos_px(zz);
  }

/// Double precision sincos
inline void fast_sincos( const double xx, double * s, double *c ) {
    // I have to use doubles to make it vectorise...

    int j;
    double x = reduce2quadrant(xx,&j);
    const double signS = (j&4);

    j-=2;

    const double signC = (j&4);
    const double poly = j&2;

    fast_sincos_m45_45(x,s,c);

    //swap
    if( poly==0 ) {
      const double tmp = *c;
      *c=*s;
      *s=tmp;
    }

    if(signC == 0.)
      *c = -(*c);
    if(signS != 0.)
      *s = -(*s);
    if (xx < 0.)
      *s = -(*s);

  }

/// Double precision cosine: just call sincos.
inline double vdt_cos(double x){double s,c;fast_sincos(x,&s,&c);return c;}