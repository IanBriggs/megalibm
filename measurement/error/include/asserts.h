#ifndef ASSERTS_H
#define ASSERTS_H

#include <assert.h>

// If debug is off then we have nothing to do
#ifdef DNDEBUG
#define ASSERT_LEVEL 0

// When debug is on set a default
#elif !defined(ASSERT_LEVEL)
#define ASSERT_LEVEL 1
#endif

#if ASSERT_LEVEL == 0
#define precondition(pred)
#define postcondition(pred)
#elif ASSERT_LEVEL == 1
#define precondition(pred) assert(pred)
#define postcondition(pred) assert(pred)
#endif

// Get a static assert

#ifndef static_assert
/* from http://www.pixelbeat.org/programming/gcc/static_assert.html */
#define ASSERT_CONCAT_(a, b) a##b
#define ASSERT_CONCAT(a, b) ASSERT_CONCAT_(a, b)
/* These can't be used after statements in c89. */
#ifdef __COUNTER__
#define static_assert(e,m)						\
  enum { ASSERT_CONCAT(static_assert_, __COUNTER__) = 1/(int)(!!(e)) }
#else
/* This can't be used twice on the same line so ensure if using in headers
 * that the headers are not included twice (by wrapping in #ifndef...#endif)
 * Note it doesn't cause an issue when used on same line of separate modules
 * compiled with gcc -combine -fwhole-program.  */
#define static_assert(e,m)						\
  enum { ASSERT_CONCAT(assert_line_, __LINE__) = 1/(int)(!!(e)) }
#endif
#endif

#endif // #ifndef ASSERTS_H