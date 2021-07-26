

CC ?= gcc
CFLAGS ?= -Wall -Wextra -Wconversion -O3 -march=native -mtune=native
CFLAGS += -Iinclude

ORACLE_O = obj/oracle_functions.o
ORACLE_I = include

TABLE_O = obj/table_generation.o
TABLE_I = include

OBJ = ${ORACLE_O} ${TABLE_O}
INC = -I${ORACLE_I} -I${TABLE_I}


BINS = $(foreach s,$(wildcard src/*_error.c),$(patsubst src/%_error.c,bin/%_error,$s))


.PHONY: all
all: ${BINS}


bin/%_error: src/%_error.c ${OBJ} | bin
	$(CC) ${CFLAGS} ${INC} $< ${OBJ} -lmpfr -lm -o $@

${ORACLE_O}: src/oracle_functions.c include/oracle_functions.h | obj
	$(CC) ${CFLAGS} $< -c -o $@

${TABLE_O}: src/table_generation.c include/table_generation.h | obj
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

