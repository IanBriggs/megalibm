

CC ?= gcc
CFLAGS ?= -Wall -Wextra -Wconversion -O3 -mtune=native -fno-builtin -DNDEBUG
CFLAGS += -Wno-unused-variable
CFLAGS += -Iinclude

GEN_DIRS = $(wildcard generated/*)
BINS = $(foreach g,$(GEN_DIRS),${g}/main)
INTER = $(foreach g,$(GEN_DIRS),${g}/funcs.o)
OBJS = obj/table_generation.o obj/xmalloc.o

DATA_0 = $(foreach g,$(GEN_DIRS),${g}/data_0.json)
DATA_1 = $(foreach g,$(GEN_DIRS),${g}/data_1.json)
DATA_2 = $(foreach g,$(GEN_DIRS),${g}/data_2.json)
DATA_3 = $(foreach g,$(GEN_DIRS),${g}/data_3.json)
DATAS = ${DATA_0} ${DATA_1} ${DATA_2} ${DATA_3}

.PHONY: all
all: build

.PHONY: build
build: ${BINS}

.PHONY: run
run: ${DATAS}

.PHONY: intermediates
intermediates: ${OBJS} ${INTER}

generated/%/data_0.json: generated/%/main
	./$< 0 > $@

generated/%/data_1.json: generated/%/main
	./$< 1 > $@

generated/%/data_2.json: generated/%/main
	./$< 2 > $@

generated/%/data_3.json: generated/%/main
	./$< 3 > $@


generated/%/main: generated/%/main.c generated/%/funcs.o ${OBJS}
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
	$(RM) -r data
	$(RM) -r generated
