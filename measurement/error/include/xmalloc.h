#ifndef XMALLOC_H
#define XMALLOC_H

#include <stddef.h>

void *xmalloc(size_t len);

void *xrealloc(void *ptr, size_t new_size);

void xfree(void *ptr);

#endif