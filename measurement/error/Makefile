

CC ?= gcc
CFLAGS ?= -Wall -Wextra -Wconversion -O3 -march=native -mtune=native -fno-builtin -DNDEBUG
CFLAGS += -Iinclude

BIN_SRCS = $(wildcard generated/main_*.c)
BINS = $(foreach s,$(BIN_SRCS),$(patsubst generated/main_%.c,bin/main_%,$s))
SRCS = $(filter-out $(BIN_SRCS),$(wildcard generated/*.c))
OBJS = $(foreach s,$(SRCS),$(patsubst generated/%.c,obj/%.o,$s))
OBJS += obj/table_generation.o
OBJS += obj/xmalloc.o

CFLAGS +=  -Igenerated


.PHONY: all
all: ${BINS}


bin/main_%: generated/main_%.c ${OBJS} | bin
	$(CC) ${CFLAGS} $< ${OBJS} -lmpfr -lgmp -lm -o $@

obj/%.o: generated/%.c generated/%.h | obj
	$(CC) ${CFLAGS} $< -c -o $@	

obj/%.o: src/%.c include/%.h | obj
	$(CC) ${CFLAGS} $< -c -o $@




bin:
	mkdir bin

obj:
	mkdir obj


.PHONY: clean
clean:
	$(RM) -r bin
	$(RM) -r obj


.PHONY: distclean
distclean: clean
	$(RM) -r data

