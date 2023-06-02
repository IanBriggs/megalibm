#ifndef XMALLOC_H
#define XMALLOC_H

#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

static void *
xmalloc(size_t len)
{
    assert(len > 0);

    void *retval = malloc(len);

    if (retval == NULL)
    {
        fprintf(stderr, "Unable to malloc memory\n");
        exit(EXIT_FAILURE);
    }

    return retval;
}

static void *
xrealloc(void *ptr, size_t new_size)
{
    assert(ptr != NULL);

    void *retval = realloc(ptr, new_size);

    if (retval == NULL)
    {
        fprintf(stderr, "Unable to realloc memory\n");
        exit(EXIT_FAILURE);
    }

    return retval;
}

static void xfree(void *ptr)
{
    assert(ptr != NULL);

    free(ptr);
}

#endif
