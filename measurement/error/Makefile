

CC ?= gcc
CFLAGS ?= -Wall -Wextra -Wconversion -O3 -mtune=native -fno-builtin -DNDEBUG
CFLAGS += -Wno-unused-variable
CFLAGS += -Iinclude

ifeq (, $(shell which brew))
else
export C_INCLUDE_PATH := /opt/homebrew/include:${C_INCLUDE_PATH}
export LIBRARY_PATH := /opt/homebrew/lib:${LIBRARY_PATH}
endif

GEN_DIRS = $(wildcard generated/*)
BINS = $(foreach g,$(GEN_DIRS),${g}/error_main)
INTER = $(foreach g,$(GEN_DIRS),${g}/funcs.o)
OBJS = obj/table_generation.o obj/xmalloc.o

ERROR_DATA_0 = $(foreach g,$(GEN_DIRS),${g}/error_data_0.json)
ERROR_DATA_1 = $(foreach g,$(GEN_DIRS),${g}/error_data_1.json)
ERROR_DATA_2 = $(foreach g,$(GEN_DIRS),${g}/error_data_2.json)
ERROR_DATA_3 = $(foreach g,$(GEN_DIRS),${g}/error_data_3.json)
ERROR_DATAS = ${ERROR_DATA_0} ${ERROR_DATA_1} ${ERROR_DATA_2} ${ERROR_DATA_3}

.PHONY: all
all: build

.PHONY: build
build: ${BINS}

.PHONY: run
run: ${ERROR_DATAS}

.PHONY: intermediates
intermediates: ${OBJS} ${INTER}

generated/%/error_data_0.json: generated/%/error_main
	./$< 0 > $@

generated/%/error_data_1.json: generated/%/error_main
	./$< 1 > $@

generated/%/error_data_2.json: generated/%/error_main
	./$< 2 > $@

generated/%/error_data_3.json: generated/%/error_main
	./$< 3 > $@


generated/%/error_main: generated/%/error_main.c generated/%/funcs.o ${OBJS}
	${CC} ${CFLAGS} -Igenerated/$* $^ -lmpfr -lgmp -lm -o $@

generated/%/funcs.o: generated/%/funcs.c generated/%/funcs.h
	${CC} ${CFLAGS} -Igenerated/$* $< -c -o $@

obj/%.o: src/%.c include/%.h | obj
	$(CC) ${CFLAGS} $< -c -o $@

obj:
	mkdir obj


.PHONY: clean
clean:
	$(RM) -r bin
	$(RM) -r obj


.PHONY: distclean
distclean: clean
	$(RM) -r error_data
	$(RM) -r generated
