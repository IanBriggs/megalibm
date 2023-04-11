/******************************************************************************/
/*  ____   __   _  _  ____  __    ____                                        */
/* (    \ /  \ / )( \(  _ \(  )  (  __)                                       */
/*  ) D ((  O )) \/ ( ) _ (/ (_/\ ) _)                                        */
/* (____/ \__/ \____/(____/\____/(____)                                       */
/*           __    ___  ___  ____  ____  ____     _  _                        */
/*          / _\  / __)/ __)(  __)/ ___)/ ___)   / )( \                       */
/*    ____ /    \( (__( (__  ) _) \___ \\___ \ _ ) __ (                       */
/*   (____)\_/\_/ \___)\___)(____)(____/(____/(_)\_)(_/                       */
/*                                                                            */
/* Transmute doubles into integer types                                       */
/*                                                                            */
/******************************************************************************/
/*  _    _  ___  ______ _   _ _____ _   _ _____  _____                        */
/* | |  | |/ _ \ | ___ \ \ | |_   _| \ | |  __ \/  ___|_                      */
/* | |  | / /_\ \| |_/ /  \| | | | |  \| | |  \/\ `--.(_)                     */
/* | |/\| |  _  ||    /| . ` | | | | . ` | | __  `--. \                       */
/* \  /\  / | | || |\ \| |\  |_| |_| |\  | |_\ \/\__/ /_                      */
/*  \/  \/\_| |_/\_| \_\_| \_/\___/\_| \_/\____/\____/(_)                     */
/*                                                                            */
/* 1. Assumes IEEE754 binary double                                           */
/* 2. Does not care about endianess                                           */
/* 3. May have undefined behavior depending on language standard and compile  */
/*    time setting used                                                       */
/******************************************************************************/

#ifndef DOUBLE_ACCESS_H
#define DOUBLE_ACCESS_H

#include "asserts.h"

#include <float.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>

/******************************************************************************/
/*   ___  __   _  _  ____  __  __    ____    ____  __  _  _  ____             */
/*  / __)/  \ ( \/ )(  _ \(  )(  )  (  __)  (_  _)(  )( \/ )(  __)            */
/* ( (__(  O )/ \/ \ ) __/ )( / (_/\ ) _)     )(   )( / \/ \ ) _)             */
/*  \___)\__/ \_)(_/(__)  (__)\____/(____)   (__) (__)\_)(_/(____)            */
/*  ____  ____  ____  ____  __  __ _   ___  ____                              */
/* / ___)(  __)(_  _)(_  _)(  )(  ( \ / __)/ ___)                             */
/* \___ \ ) _)   )(    )(   )( /    /( (_ \\___ \                             */
/* (____/(____) (__)  (__) (__)\_)__) \___/(____/                             */
/*                                                                            */
/******************************************************************************/

/* Which approach should be used to convert double to bits                    */
/* 0: Type punning                                                            */
/* 1: Union abuse                                                             */
/* 2: BitField Union abuse                                                    */
/* 3. Memcpy                                                                  */
#ifndef TRANSMUTE_VERSION
#define TRANSMUTE_VERSION 3
#endif

/******************************************************************************/
/*  ____  _  _  ____  __    __  ___                                           */
/* (  _ \/ )( \(  _ \(  )  (  )/ __)                                          */
/*  ) __/) \/ ( ) _ (/ (_/\ )(( (__                                           */
/* (__)  \____/(____/\____/(__)\___)                                          */
/*   __  __ _  ____  ____  ____  ____  __    ___  ____                        */
/*  (  )(  ( \(_  _)(  __)(  _ \(  __)/ _\  / __)(  __)                       */
/*   )( /    /  )(   ) _)  )   / ) _)/    \( (__  ) _)                        */
/*  (__)\_)__) (__) (____)(__\_)(__) \_/\_/ \___)(____)                       */
/*                                                                            */
/******************************************************************************/

/**
 * Get the sign bit from a double.
 */
static uint8_t get_sign_double(double d);

/**
 * Get the unbiased exponent bits from a double.
 */
static uint16_t get_exponent_double(double d);

/**
 * Get the mantissa bits from a double.
 */
static uint64_t get_mantissa_double(double d);

/**
 * Set the sign bit of a double.
 */
static double set_sign_double(double d, uint8_t s);

/**
 * Set the unbiased exponent bits of a double.
 */
static double set_exponent_double(double d, uint16_t e);

/**
 * Set the mantissa bits of a double.
 */
static double set_mantissa_double(double d, uint64_t m);

/**
 * Get all the bits from a double
 */
static uint64_t double_to_uint64_t(double d);

/**
 * Set all the bits of a double
 */
static double uint64_t_to_double(uint64_t u);

/******************************************************************************/
/*  _  _  __  ___    ____  _  _  __ _  ____                                   */
/* / )( \(  )/ __)  / ___)/ )( \(  ( \(_  _)                                  */
/* ) __ ( )(( (__   \___ \) \/ (/    /  )(                                    */
/* \_)(_/(__)\___)  (____/\____/\_)__) (__)                                   */
/*  ____  ____   __    ___  __   __ _  ____  ____                             */
/* (    \(  _ \ / _\  / __)/  \ (  ( \(  __)/ ___)                            */
/*  ) D ( )   //    \( (__(  O )/    / ) _) \___ \                            */
/* (____/(__\_)\_/\_/ \___)\__/ \_)__)(____)(____/                            */
/*                                                                            */
/* Here be dragons                                                            */
/*                                                                            */
/******************************************************************************/

/* These functions all reinterpret the bit pattern of a type as another.      */
/* Even though they all perform the same actions, due to UB they may be       */
/*   broken.                                                                  */
/* Some may be faster if the compiler decides not to shoot us for our dirty   */
/*   deeds.                                                                   */

/* We are assuming the following bit format:                                  */
/*  + the sign is bit 63                                                      */
/*  + the exponent is bits 62-52                                              */
/*  + the mantissa is bits 51-0                                               */

/* (hopefully) check that we are using 8 byte IEEE 754 doubles */
static_assert(CHAR_BIT == 8, "Expected IEEE 754 floating point");
static_assert(sizeof(double) == 8, "Expected IEEE 754 floating point");
static_assert(FLT_RADIX == 2, "Expected IEEE 754 floating point");
static_assert(DBL_MANT_DIG == 53, "Expected IEEE 754 floating point");
static_assert(DBL_MAX_EXP == 1024, "Expected IEEE 754 floating point");
static_assert(DBL_MIN_EXP == -1021, "Expected IEEE 754 floating point");

/* From high uint8_t how much to shift the sign to the LSB */
static const size_t DBL_UINT8_SIGN_SHIFT = 7;

/* From high uint16_t how much to shift the exponent to the LSB */
static const size_t DBL_UINT16_EXP_SHIFT = 4;

/* From high uint8_t mask used to select sign */
static const uint8_t DBL_UINT8_SIGN_MASK = UINT8_C(0x80);

/* From high uint16_t mask used to select exponent */
static const uint16_t DBL_UINT16_EXP_MASK = UINT16_C(0x7FF0);

/* From uint64_t mask used to select mantissa */
static const uint64_t DBL_UINT64_MANT_MASK = UINT64_C(0x000FFFFFFFFFFFFF);

/* Maximum values for sign, exponent, and mantissa */
static const uint8_t DBL_SIGN_MAX = DBL_UINT8_SIGN_MASK >> DBL_UINT8_SIGN_SHIFT;
static const uint16_t DBL_EXP_MAX = DBL_UINT16_EXP_MASK >> DBL_UINT16_EXP_SHIFT;
static const uint64_t DBL_MANT_MAX = DBL_UINT64_MANT_MASK;

/**
 * Extract the sign bit from the high uint8_t of a double.
 */
static inline uint8_t
dbl_high_uint8_extract_sign(uint8_t high_uint8)
{
    /* no need to mask before the shift */
    uint8_t sign = high_uint8 >> DBL_UINT8_SIGN_SHIFT;
    postcondition(sign <= DBL_SIGN_MAX);
    return sign;
}

/**
 * Extract the exponent bits from the high uint16_t of a double.
 */
static inline uint16_t
dbl_high_uint16_extract_exp(uint16_t high_uint16)
{
    uint16_t shifted_exponent = high_uint16 & DBL_UINT16_EXP_MASK;
    uint16_t exponent = shifted_exponent >> DBL_UINT16_EXP_SHIFT;
    postcondition(exponent <= DBL_EXP_MAX);
    return exponent;
}

/**
 * Extract the mantissa bits from the uint64_t of a double.
 */
static inline uint64_t
dbl_high_uint64_extract_mant(uint64_t high_uint64)
{
    uint64_t mantissa = high_uint64 & DBL_UINT64_MANT_MASK;
    /* no need to shift */
    postcondition(mantissa <= DBL_MANT_MAX);
    return mantissa;
}

/**
 * Combine existing high uint8_t of a double with sign bit
 */
static inline uint8_t
dbl_combine_high_uint8(uint8_t high_uint8, uint8_t s)
{
    precondition(s <= DBL_SIGN_MAX);
    /* TODO: why is the cast needed?
             s, DBL_UINT8_SIGN_SHIFT, and shifted_sign are all uint8_t */
    uint8_t shifted_sign = (uint8_t)(s << DBL_UINT8_SIGN_SHIFT);
    uint8_t masked_high_uint8 = high_uint8 & (~DBL_UINT8_SIGN_MASK);
    uint8_t new_high_uint8 = shifted_sign | masked_high_uint8;
    return new_high_uint8;
}

/**
 * Combine existing high uint16_t of a double with exponent bits
 */
static inline uint16_t
dbl_combine_high_uint16(uint16_t high_uint16, uint16_t e)
{
    precondition(e <= DBL_EXP_MAX);
    /* TODO: why is the cast needed?
             e, DBL_UINT16_EXP_SHIFT, and shifted_exponent are all uint8_t */
    uint16_t shifted_exponent = (uint16_t)(e << DBL_UINT16_EXP_SHIFT);
    uint16_t masked_high_uint16 = high_uint16 & (~DBL_UINT16_EXP_MASK);
    uint16_t new_high_uint16 = shifted_exponent | masked_high_uint16;
    return new_high_uint16;
}

/**
 * Combine existing uint64_t of a double with mantissa bits
 */
static inline uint64_t
dbl_combine_high_uint64(uint64_t high_uint64, uint64_t m)
{
    precondition(m <= DBL_MANT_MAX);
    /* no need to shift */
    uint64_t masked_high_uint64 = high_uint64 & (~DBL_UINT64_MANT_MASK);
    uint64_t new_high_uint64 = m | masked_high_uint64;
    return new_high_uint64;
}

/******************************************************************************/
/* Approach 0: Type punning                                                   */
/******************************************************************************/

static inline uint8_t
pun_get_sign_double(double d)
{
    uint8_t high_uint8 = *(((uint8_t *)&d) + 7);
    return dbl_high_uint8_extract_sign(high_uint8);
}

static inline uint16_t
pun_get_exponent_double(double d)
{
    uint16_t high_uint16 = *(((uint16_t *)&d) + 3);
    return dbl_high_uint16_extract_exp(high_uint16);
}

static inline uint64_t
pun_get_mantissa_double(double d)
{
    uint64_t high_uint64 = *((uint64_t *)&d);
    return dbl_high_uint64_extract_mant(high_uint64);
}

static inline double
pun_set_sign_double(double d, uint8_t s)
{
    uint8_t high_uint8 = *(((uint8_t *)&d) + 7);
    *(((uint8_t *)&d) + 7) = dbl_combine_high_uint8(high_uint8, s);
    return d;
}

static inline double
pun_set_exponent_double(double d, uint16_t e)
{
    uint16_t high_uint16 = *((uint16_t *)&d + 3);
    *(((uint16_t *)&d) + 3) = dbl_combine_high_uint16(high_uint16, e);
    return d;
}

static inline double
pun_set_mantissa_double(double d, uint64_t m)
{
    uint64_t high_uint64 = *(uint64_t *)&d;
    *((uint64_t *)&d) = dbl_combine_high_uint64(high_uint64, m);
    return d;
}

static inline uint64_t
pun_double_to_uint64_t(double d)
{
    return *((uint64_t *)&d);
}

static inline double
pun_uint64_t_to_double(uint64_t u)
{
    return *((double *)&u);
}

/******************************************************************************/
/* Approach 1: Union abuse                                                    */
/******************************************************************************/

typedef union
{
    double d;
    uint64_t u;
    struct
    {
        uint16_t a;
        uint16_t b;
        uint16_t c;
        uint16_t d;
    } uint16s;
    struct
    {
        uint8_t a;
        uint8_t b;
        uint8_t c;
        uint8_t d;
        uint8_t e;
        uint8_t f;
        uint8_t g;
        uint8_t h;
    } uint8s;
} dbl_union_caster;

static inline uint8_t
union_get_sign_double(double d)
{
    dbl_union_caster b;
    b.d = d;
    uint8_t high_uint8 = b.uint8s.h;
    return dbl_high_uint8_extract_sign(high_uint8);
}

static inline uint16_t
union_get_exponent_double(double d)
{
    dbl_union_caster b;
    b.d = d;
    uint16_t high_uint16 = b.uint16s.d;
    return dbl_high_uint16_extract_exp(high_uint16);
}

static inline uint64_t
union_get_mantissa_double(double d)
{
    dbl_union_caster b;
    b.d = d;
    uint64_t high_uint64 = b.u;
    return dbl_high_uint64_extract_mant(high_uint64);
}

static inline double
union_set_sign_double(double d, uint8_t s)
{
    dbl_union_caster b;
    b.d = d;
    uint8_t high_uint8 = b.uint8s.h;
    b.uint8s.h = dbl_combine_high_uint8(high_uint8, s);
    return b.d;
}

static inline double
union_set_exponent_double(double d, uint16_t e)
{
    dbl_union_caster b;
    b.d = d;
    uint16_t high_uint16 = b.uint16s.d;
    b.uint16s.d = dbl_combine_high_uint16(high_uint16, e);
    return b.d;
}

static inline double
union_set_mantissa_double(double d, uint64_t m)
{
    dbl_union_caster b;
    b.d = d;
    uint64_t high_uint64 = b.u;
    b.u = dbl_combine_high_uint64(high_uint64, m);
    return b.d;
}

static inline uint64_t
union_double_to_uint64_t(double d)
{
    dbl_union_caster b;
    b.d = d;
    return b.u;
}

static inline double
union_uint64_t_to_double(uint64_t u)
{
    dbl_union_caster b;
    b.u = u;
    return b.d;
}

/******************************************************************************/
/* Approach 2: BitField Union abuse                                           */
/******************************************************************************/

typedef union
{
    double d;
    uint64_t u;
    struct
    {
        uint64_t mantissa : 52;
        uint16_t exponent : 11;
        uint8_t sign : 1;
    } parts;
} dbl_bitfield_caster;

static inline uint8_t
bitfield_get_sign_double(double d)
{
    dbl_bitfield_caster b;
    b.d = d;
    return b.parts.sign;
}

static inline uint16_t
bitfield_get_exponent_double(double d)
{
    dbl_bitfield_caster b;
    b.d = d;
    return b.parts.exponent;
}

static inline uint64_t
bitfield_get_mantissa_double(double d)
{
    dbl_bitfield_caster b;
    b.d = d;
    return b.parts.mantissa;
}

static inline double
bitfield_set_sign_double(double d, uint8_t s)
{
    precondition(s <= DBL_SIGN_MAX);
    dbl_bitfield_caster b;
    b.d = d;
    b.parts.sign = s;
    return b.d;
}

static inline double
bitfield_set_exponent_double(double d, uint16_t e)
{
    precondition(e <= DBL_EXP_MAX);
    dbl_bitfield_caster b;
    b.d = d;
    b.parts.exponent = e;
    return b.d;
}

static inline double
bitfield_set_mantissa_double(double d, uint64_t m)
{
    precondition(m <= DBL_MANT_MAX);
    dbl_bitfield_caster b;
    b.d = d;
    b.parts.mantissa = m;
    return b.d;
}

static inline uint64_t
bitfield_double_to_uint64_t(double d)
{
    dbl_bitfield_caster b;
    b.d = d;
    return b.u;
}

static inline double
bitfield_uint64_t_to_double(uint64_t u)
{
    dbl_bitfield_caster b;
    b.u = u;
    return b.d;
}

/******************************************************************************/
/* Approach 3: Memcpy                                                         */
/******************************************************************************/

static inline uint8_t
memcpy_get_sign_double(double d)
{
    uint8_t buff_uint8[8];
    memcpy((void *)&buff_uint8, (void *)&d, sizeof(double));
    return dbl_high_uint8_extract_sign(buff_uint8[7]);
}

static inline uint16_t
memcpy_get_exponent_double(double d)
{
    uint16_t buff_uint16[4];
    memcpy((void *)&buff_uint16, (void *)&d, sizeof(double));
    return dbl_high_uint16_extract_exp(buff_uint16[3]);
}

static inline uint64_t
memcpy_get_mantissa_double(double d)
{
    uint64_t high_uint64;
    memcpy((void *)&high_uint64, (void *)&d, sizeof(uint64_t));
    return dbl_high_uint64_extract_mant(high_uint64);
}

static inline double
memcpy_set_sign_double(double d, uint8_t s)
{
    uint8_t buff_uint8[8];
    memcpy((void *)&buff_uint8, (void *)&d, sizeof(double));
    uint8_t new_high_uint8 = dbl_combine_high_uint8(buff_uint8[7], s);
    buff_uint8[7] = new_high_uint8;
    memcpy((void *)&d, (void *)&buff_uint8, sizeof(double));
    return d;
}

static inline double
memcpy_set_exponent_double(double d, uint16_t e)
{
    uint16_t buff_uint16[4];
    memcpy((void *)&buff_uint16, (void *)&d, sizeof(double));
    uint16_t new_high_uint16 = dbl_combine_high_uint16(buff_uint16[3], e);
    buff_uint16[3] = new_high_uint16;
    memcpy((void *)&d, (void *)&buff_uint16, sizeof(double));
    return d;
}

static inline double
memcpy_set_mantissa_double(double d, uint64_t m)
{
    uint64_t high_uint64;
    memcpy((void *)&high_uint64, (void *)&d, sizeof(uint64_t));
    uint64_t new_high_uint64 = dbl_combine_high_uint64(high_uint64, m);
    memcpy((void *)&d, (void *)&new_high_uint64, sizeof(uint64_t));
    return d;
}

static inline uint64_t
memcpy_double_to_uint64_t(double d)
{
    uint64_t u;
    memcpy((void *)&u, (void *)&d, sizeof(uint64_t));
    return u;
}

static inline double
memcpy_uint64_t_to_double(uint64_t u)
{
    double d;
    memcpy((void *)&d, (void *)&u, sizeof(double));
    return d;
}

/******************************************************************************/
/* Switcher: This allows us to select among implementations                   */
/******************************************************************************/

static inline uint8_t
get_sign_double(double d)
{
#ifndef TRANSMUTE_VERSION
#error "TRANSMUTE_VERSION must be set"
#elif TRANSMUTE_VERSION == 0
    return pun_get_sign_double(d);
#elif TRANSMUTE_VERSION == 1
    return union_get_sign_double(d);
#elif TRANSMUTE_VERSION == 2
    return bitfield_get_sign_double(d);
#elif TRANSMUTE_VERSION == 3
    return memcpy_get_sign_double(d);
#else
#error "Invalid TRANSMUTE_VERSION selection"
#endif
}

static inline uint16_t
get_exponent_double(double d)
{
#ifndef TRANSMUTE_VERSION
#error "TRANSMUTE_VERSION must be set"
#elif TRANSMUTE_VERSION == 0
    return pun_get_exponent_double(d);
#elif TRANSMUTE_VERSION == 1
    return union_get_exponent_double(d);
#elif TRANSMUTE_VERSION == 2
    return bitfield_get_exponent_double(d);
#elif TRANSMUTE_VERSION == 3
    return memcpy_get_exponent_double(d);
#else
#error "Invalid TRANSMUTE_VERSION selection"
#endif
}

static inline uint64_t
get_mantissa_double(double d)
{
#ifndef TRANSMUTE_VERSION
#error "TRANSMUTE_VERSION must be set"
#elif TRANSMUTE_VERSION == 0
    return pun_get_mantissa_double(d);
#elif TRANSMUTE_VERSION == 1
    return union_get_mantissa_double(d);
#elif TRANSMUTE_VERSION == 2
    return bitfield_get_mantissa_double(d);
#elif TRANSMUTE_VERSION == 3
    return memcpy_get_mantissa_double(d);
#else
#error "Invalid TRANSMUTE_VERSION selection"
#endif
}

static inline double
set_sign_double(double d, uint8_t s)
{
#ifndef TRANSMUTE_VERSION
#error "TRANSMUTE_VERSION must be set"
#elif TRANSMUTE_VERSION == 0
    return pun_set_sign_double(d, s);
#elif TRANSMUTE_VERSION == 1
    return union_set_sign_double(d, s);
#elif TRANSMUTE_VERSION == 2
    return bitfield_set_sign_double(d, s);
#elif TRANSMUTE_VERSION == 3
    return memcpy_set_sign_double(d, s);
#else
#error "Invalid TRANSMUTE_VERSION selection"
#endif
}

static inline double
set_exponent_double(double d, uint16_t e)
{
#ifndef TRANSMUTE_VERSION
#error "TRANSMUTE_VERSION must be set"
#elif TRANSMUTE_VERSION == 0
    return pun_set_exponent_double(d, e);
#elif TRANSMUTE_VERSION == 1
    return union_set_exponent_double(d, e);
#elif TRANSMUTE_VERSION == 2
    return bitfield_set_exponent_double(d, e);
#elif TRANSMUTE_VERSION == 3
    return memcpy_set_exponent_double(d, e);
#else
#error "Invalid TRANSMUTE_VERSION selection"
#endif
}

static inline double
set_mantissa_double(double d, uint64_t m)
{
#ifndef TRANSMUTE_VERSION
#error "TRANSMUTE_VERSION must be set"
#elif TRANSMUTE_VERSION == 0
    return pun_set_mantissa_double(d, m);
#elif TRANSMUTE_VERSION == 1
    return union_set_mantissa_double(d, m);
#elif TRANSMUTE_VERSION == 2
    return bitfield_set_mantissa_double(d, m);
#elif TRANSMUTE_VERSION == 3
    return memcpy_set_mantissa_double(d, m);
#else
#error "Invalid TRANSMUTE_VERSION selection"
#endif
}

static inline uint64_t
double_to_uint64_t(double d)
{
#ifndef TRANSMUTE_VERSION
#error "TRANSMUTE_VERSION must be set"
#elif TRANSMUTE_VERSION == 0
    return pun_double_to_uint64_t(d);
#elif TRANSMUTE_VERSION == 1
    return union_double_to_uint64_t(d);
#elif TRANSMUTE_VERSION == 2
    return bitfield_double_to_uint64_t(d);
#elif TRANSMUTE_VERSION == 3
    return memcpy_double_to_uint64_t(d);
#else
#error "Invalid TRANSMUTE_VERSION selection"
#endif
}

static inline double
uint64_t_to_double(uint64_t u)
{
#ifndef TRANSMUTE_VERSION
#error "TRANSMUTE_VERSION must be set"
#elif TRANSMUTE_VERSION == 0
    return pun_uint64_t_to_double(u);
#elif TRANSMUTE_VERSION == 1
    return union_uint64_t_to_double(u);
#elif TRANSMUTE_VERSION == 2
    return bitfield_uint64_t_to_double(u);
#elif TRANSMUTE_VERSION == 3
    return memcpy_uint64_t_to_double(u);
#else
#error "Invalid TRANSMUTE_VERSION selection"
#endif
}

#endif /* #ifndef DOUBLE_ACCESS_H */