#ifndef LIBWALLY_CORE_TX_IO_H
#define LIBWALLY_CORE_TX_IO_H 1

#include <include/wally_map.h>
#include "ccan/ccan/crypto/sha256/sha256.h"

/* Suggested initial size of a signing cache to avoid re-allocations */
#define TXIO_CACHE_INITIAL_SIZE 16

/* A cursor for pushing/pulling tx bytes for hashing */
typedef struct cursor_io
{
    struct sha256_ctx ctx;
    struct wally_map *cache;
    unsigned char *cursor;
    size_t max;
} cursor_io;

#endif /* LIBWALLY_CORE_TX_IO_H */
