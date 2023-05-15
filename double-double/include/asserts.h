/******************************************************************************/
/*   __   ____  ____  ____  ____  ____  ____     _  _                         */
/*  / _\ / ___)/ ___)(  __)(  _ \(_  _)/ ___)   / )( \                        */
/* /    \\___ \\___ \ ) _)  )   /  )(  \___ \ _ ) __ (                        */
/* \_/\_/(____/(____/(____)(__\_) (__) (____/(_)\_)(_/                        */
/*                                                                            */
/* Adds a static assert and multiple aliases for assert.                      */
/*                                                                            */
/******************************************************************************/

#ifndef ASSERTS_H
#define ASSERTS_H

#include <assert.h>

/* For now just add aliases, maybe later add more assertion variations */
#define precondition(pred) assert(pred)
#define postcondition(pred) assert(pred)

/* Add static_assert if we don't already have it */
#ifndef static_assert
/* from http://www.pixelbeat.org/programming/gcc/static_assert.html */
#define ASSERT_CONCAT_(a, b) a##b
#define ASSERT_CONCAT(a, b) ASSERT_CONCAT_(a, b)
/* These can't be used after statements in c89. */
#ifdef __COUNTER__
#define static_assert(e, m)                                       \
  enum                                                            \
  {                                                               \
    ASSERT_CONCAT(static_assert_, __COUNTER__) = 1 / (int)(!!(e)) \
  }
#else
/* This can't be used twice on the same line so ensure if using in headers
 * that the headers are not included twice (by wrapping in #ifndef...#endif)
 * Note it doesn't cause an issue when used on same line of separate modules
 * compiled with gcc -combine -fwhole-program.  */
#define static_assert(e, m)                                  \
  enum                                                       \
  {                                                          \
    ASSERT_CONCAT(assert_line_, __LINE__) = 1 / (int)(!!(e)) \
  }
#endif /* #ifdef __COUNTER__ */
#endif /* #ifndef static_assert */

#endif /* #ifndef ASSERTS_H */
