#ifndef DOUBLE_ACCESS_H
#define DOUBLE_ACCESS_H

#include "asserts.h"

#include <stdint.h>
#include <string.h>
#include <limits.h>

// WARNINGS:
// * NO HEED IS GIVEN TO ENDIANESS!!!
// * UB may be present

//   ___  __   _  _  ____  __  __    ____    ____  __  _  _  ____
//  / __)/  \ ( \/ )(  _ \(  )(  )  (  __)  (_  _)(  )( \/ )(  __)
// ( (__(  O )/ \/ \ ) __/ )( / (_/\ ) _)     )(   )( / \/ \ ) _)
//  \___)\__/ \_)(_/(__)  (__)\____/(____)   (__) (__)\_)(_/(____)
//  ____  ____  ____  ____  __  __ _   ___  ____
// / ___)(  __)(_  _)(_  _)(  )(  ( \ / __)/ ___)
// \___ \ ) _)   )(    )(   )( /    /( (_ \\___ \
// (____/(____) (__)  (__) (__)\_)__) \___/(____/
//
// Compile time settings
//

// Which approach should be used to convert double to bits
// 0: Type punning
// 1: Union abuse
// 2: BitField Union abuse
// 3. Memcpy
#ifndef TRANSMUTE_VERSION
#define TRANSMUTE_VERSION 3
#endif

//  ____  _  _  ____  __    __  ___
// (  _ \/ )( \(  _ \(  )  (  )/ __)
//  ) __/) \/ ( ) _ (/ (_/\ )(( (__
// (__)  \____/(____/\____/(__)\___)
//   __  __ _  ____  ____  ____  ____  __    ___  ____
//  (  )(  ( \(_  _)(  __)(  _ \(  __)/ _\  / __)(  __)
//   )( /    /  )(   ) _)  )   / ) _)/    \( (__  ) _)
//  (__)\_)__) (__) (____)(__\_)(__) \_/\_/ \___)(____)
//
// Public interface
//

// Nicer functions:

// Get/set sign/exponent/mantissa
static uint8_t get_sign_double(double d);
static uint16_t get_exponent_double(double d);
static uint64_t get_mantissa_double(double d);

static double set_sign_double(double d, uint8_t s);
static double set_exponent_double(double d, uint16_t e);
static double set_mantissa_double(double d, uint64_t m);

// Do your own bit twiddling functions:

// Reinterpret whole double
static uint64_t double_to_uint64_t(double d);
static double uint64_t_to_double(uint64_t u);

//  _  _  __  ___    ____  _  _  __ _  ____
// / )( \(  )/ __)  / ___)/ )( \(  ( \(_  _)
// ) __ ( )(( (__   \___ \) \/ (/    /  )(
// \_)(_/(__)\___)  (____/\____/\_)__) (__)
//  ____  ____   __    ___  __   __ _  ____  ____
// (    \(  _ \ / _\  / __)/  \ (  ( \(  __)/ ___)
//  ) D ( )   //    \( (__(  O )/    / ) _) \___ \
// (____/(__\_)\_/\_/ \___)\__/ \_)__)(____)(____/
//
// Here be dragons
//

// These functions all reinterpret the bit pattern of a type as another.
// Even though they all perform the same actions, due to UB they may be broken.
// Some may be faster if the compiler decides not to shoot us for our dirty
// deeds.

// We are assuming the following bit format:
/*
 s = sign bit
 e = exponent bits
 m = mantissa bits

   byte 0
   /
 |-------|
 seee eeee  eeee mmmm  mmmm mmmm  mmmm mmmm  mmmm mmmm  mmmm mmmm  mmmm mmmm  mmmm mmmm
 ||            | |
 |bit 1        | bit 12
 bit 0         bit 11
*/

static_assert(CHAR_BIT == 8, "Expected 8 bits per byte");
static_assert(sizeof(double) == 8, "Expected an 8 byte double");

static const size_t BYTE_SIGN_OFFSET = 7;
static const size_t SHORT_EXP_OFFSET = 4;

static const uint8_t BYTE_SIGN_MASK = UINT8_C(0x80);
static const uint16_t SHORT_EXP_MASK = UINT16_C(0x7FF0);
static const uint64_t LONG_MANT_MASK = UINT64_C(0x000FFFFFFFFFFFFF);

static const uint8_t SIGN_MAX = UINT8_C(1);
static const uint16_t EXP_MAX = UINT16_C(2048);              // 2 ** 11
static const uint64_t MANT_MAX = UINT64_C(4503599627370495); // 2 ** 52

static inline uint8_t
top_byte_extract_sign(uint8_t top_byte)
{
    // no need to mask before the shift
    uint8_t sign = top_byte >> BYTE_SIGN_OFFSET;
    postcondition(sign <= SIGN_MAX);
    return sign;
}

static inline uint16_t
top_short_extract_exp(uint16_t top_short)
{
    uint16_t shifted_exponent = top_short & SHORT_EXP_MASK;
    uint16_t exponent = shifted_exponent >> SHORT_EXP_OFFSET;
    postcondition(exponent <= EXP_MAX);
    return exponent;
}

static inline uint64_t
top_long_extract_mant(uint64_t top_long)
{
    uint64_t mantissa = top_long & LONG_MANT_MASK;
    // no need for a shift
    postcondition(mantissa <= MANT_MAX);
    return mantissa;
}

static inline uint8_t
combine_top_byte(uint8_t top_byte, uint8_t s)
{
    precondition(s <= SIGN_MAX);
    uint8_t shifted_sign = (uint8_t) (s << BYTE_SIGN_OFFSET); // why is the cast needed????
    uint8_t masked_top_byte = top_byte & (~BYTE_SIGN_MASK);
    uint8_t new_top_byte = shifted_sign | masked_top_byte;
    return new_top_byte;
}

static inline uint16_t
combine_top_short(uint16_t top_short, uint16_t e)
{
    precondition(e <= EXP_MAX);
    uint16_t shifted_exponent = (uint16_t) (e << SHORT_EXP_OFFSET); // why is the cast needed????
    uint16_t masked_top_short = top_short & (~SHORT_EXP_MASK);
    uint16_t new_top_short = shifted_exponent | masked_top_short;
    return new_top_short;
}

static inline uint64_t
combine_top_long(uint64_t top_long, uint64_t m)
{
    precondition(m <= MANT_MAX);
    uint64_t masked_top_long = top_long & (~LONG_MANT_MASK);
    uint64_t new_top_long = m | masked_top_long;
    return new_top_long;
}

// Type punning.
// This is the oldest way, but definitely invokes undefined behavior

static inline uint8_t
pun_get_sign_double(double d)
{
    uint8_t top_byte = *(uint8_t *)&d;
    return top_byte_extract_sign(top_byte);
}

static inline uint16_t
pun_get_exponent_double(double d)
{
    uint16_t top_short = *(uint16_t *)&d;
    return top_short_extract_exp(top_short);
}

static inline uint64_t
pun_get_mantissa_double(double d)
{
    uint64_t top_long = *(uint64_t *)&d;
    return top_long_extract_mant(top_long);
}

static inline double
pun_set_sign_double(double d, uint8_t s)
{
    uint8_t top_byte = *(uint8_t *)&d;
    *(uint8_t *)&d = combine_top_byte(top_byte, s);
    return d;
}

static inline double
pun_set_exponent_double(double d, uint16_t e)
{
    uint16_t top_short = *(uint16_t *)&d;
    *(uint16_t *)&d = combine_top_short(top_short, e);
    return d;
}

static inline double
pun_set_mantissa_double(double d, uint64_t m)
{
    uint64_t top_long = *(uint64_t *)&d;
    *(uint64_t *)&d = combine_top_long(top_long, m);
    return d;
}

static inline uint64_t
pun_double_to_uint64_t(double d)
{
    return *(uint64_t *)&d;
}

static inline double
pun_uint64_t_to_double(uint64_t u)
{
    return *(double *)&u;
}

// Unions.
// Most people seem to think this is defined, but it is not.

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
    } shorts;
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
    } bytes;
} union_caster;

static inline uint8_t
union_get_sign_double(double d)
{
    union_caster b;
    b.d = d;
    uint8_t top_byte = b.bytes.a;
    return top_byte_extract_sign(top_byte);
}

static inline uint16_t
union_get_exponent_double(double d)
{
    union_caster b;
    b.d = d;
    uint16_t top_short = b.shorts.a;
    return top_short_extract_exp(top_short);
}

static inline uint64_t
union_get_mantissa_double(double d)
{
    union_caster b;
    b.d = d;
    uint64_t top_long = b.u;
    return top_long_extract_mant(top_long);
}

static inline double
union_set_sign_double(double d, uint8_t s)
{
    union_caster b;
    b.d = d;
    uint8_t top_byte = b.bytes.a;
    b.bytes.a = combine_top_byte(top_byte, s);
    return b.d;
}

static inline double
union_set_exponent_double(double d, uint16_t e)
{
    union_caster b;
    b.d = d;
    uint16_t top_short = b.shorts.a;
    b.shorts.a = combine_top_short(top_short, e);
    return b.d;
}

static inline double
union_set_mantissa_double(double d, uint64_t m)
{
    union_caster b;
    b.d = d;
    uint64_t top_long = b.u;
    b.u = combine_top_long(top_long, m);
    return b.d;
}

static inline uint64_t
union_double_to_uint64_t(double d)
{
    union_caster b;
    b.d = d;
    return b.u;
}

static inline double
union_uint64_t_to_double(uint64_t u)
{
    union_caster b;
    b.u = u;
    return b.d;
}

// BitField
// This is similar to the union approach, without the need for shifts and masks.

typedef union
{
    double d;
    uint64_t u;
    struct
    {
        uint8_t sign : 1;
        uint16_t exponent : 11;
        uint64_t mantissa : 52;
    } parts;
} bitfield_caster;

static inline uint8_t
bitfield_get_sign_double(double d)
{
    bitfield_caster b;
    b.d = d;
    return b.parts.sign;
}

static inline uint16_t
bitfield_get_exponent_double(double d)
{
    bitfield_caster b;
    b.d = d;
    return b.parts.exponent;
}

static inline uint64_t
bitfield_get_mantissa_double(double d)
{
    bitfield_caster b;
    b.d = d;
    return b.parts.mantissa;
}

static inline double
bitfield_set_sign_double(double d, uint8_t s)
{
    precondition(s <= SIGN_MAX);
    bitfield_caster b;
    b.d = d;
    b.parts.sign = s;
    return b.d;
}

static inline double
bitfield_set_exponent_double(double d, uint16_t e)
{
    precondition(e <= EXP_MAX);
    bitfield_caster b;
    b.d = d;
    b.parts.exponent = e;
    return b.d;
}

static inline double
bitfield_set_mantissa_double(double d, uint64_t m)
{
    precondition(m <= MANT_MAX);
    bitfield_caster b;
    b.d = d;
    b.parts.mantissa = m;
    return b.d;
}

static inline uint64_t
bitfield_double_to_uint64_t(double d)
{
    bitfield_caster b;
    b.d = d;
    return b.u;
}

static inline double
bitfield_uint64_t_to_double(uint64_t u)
{
    bitfield_caster b;
    b.u = u;
    return b.d;
}

// Mempcy
// As far as I know this is the only method that does not invoke undefined
// behavior.

static inline uint8_t
memcpy_get_sign_double(double d)
{
    uint8_t top_byte;
    memcpy(&top_byte, (void *)&d, sizeof(uint8_t));
    return top_byte_extract_sign(top_byte);
}

static inline uint16_t
memcpy_get_exponent_double(double d)
{
    uint16_t top_short;
    memcpy(&top_short, (void *)&d, sizeof(uint16_t));
    return top_short_extract_exp(top_short);
}

static inline uint64_t
memcpy_get_mantissa_double(double d)
{
    uint64_t top_long;
    memcpy(&top_long, (void *)&d, sizeof(uint64_t));
    return top_long_extract_mant(top_long);
}

static inline double
memcpy_set_sign_double(double d, uint8_t s)
{
    uint8_t top_byte;
    memcpy(&top_byte, (void *)&d, sizeof(uint8_t));
    uint8_t new_top_byte = combine_top_byte(top_byte, s);
    memcpy(&d, (void *)&new_top_byte, sizeof(uint8_t));
    return d;
}

static inline double
memcpy_set_exponent_double(double d, uint16_t e)
{
    uint16_t top_short;
    memcpy(&top_short, (void *)&d, sizeof(uint16_t));
    uint16_t new_top_short = combine_top_short(top_short, e);
    memcpy(&d, (void *)&new_top_short, sizeof(uint16_t));
    return d;
}

static inline double
memcpy_set_mantissa_double(double d, uint64_t m)
{
    uint64_t top_long;
    memcpy(&top_long, (void *)&d, sizeof(uint64_t));
    uint64_t new_top_long = combine_top_long(top_long, m);
    memcpy(&d, (void *)&new_top_long, sizeof(uint64_t));
    return d;
}

static inline uint64_t
memcpy_double_to_uint64_t(double d)
{
    uint64_t u;
    memcpy(&u, (void *)&d, sizeof(uint64_t));
    return u;
}

static inline double
memcpy_uint64_t_to_double(uint64_t u)
{
    double d;
    memcpy(&d, (void *)&u, sizeof(double));
    return d;
}

// Switcher
// This allows us to select among implementations

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

#endif // #ifndef DOUBLE_ACCESS_H