

CC ?= gcc
CFLAGS ?= -Wall -Wextra -Wconversion -O3 -mtune=native -fno-builtin -DNDEBUG
CFLAGS += -Wno-unused-variable
CFLAGS += -Iinclude

GEN_DIRS = $(wildcard generated/*)
BINS = $(foreach g,$(GEN_DIRS),${g}/timing_main)
INTER = $(foreach g,$(GEN_DIRS),${g}/funcs.o)
OBJS = obj/table_generation.o obj/xmalloc.o

TIMING_DATA_0 = $(foreach g,$(GEN_DIRS),${g}/timing_data_0.json)
TIMING_DATA_1 = $(foreach g,$(GEN_DIRS),${g}/timing_data_1.json)
TIMING_DATA_2 = $(foreach g,$(GEN_DIRS),${g}/timing_data_2.json)
TIMING_DATA_3 = $(foreach g,$(GEN_DIRS),${g}/timing_data_3.json)
TIMING_DATAS = ${TIMING_DATA_0} ${TIMING_DATA_1} ${TIMING_DATA_2} ${TIMING_DATA_3}

.PHONY: all
all: build

.PHONY: build
build: ${BINS}

.PHONY: run
run: ${TIMING_DATAS}

.PHONY: intermediates
intermediates: ${OBJS} ${INTER}

generated/%/timing_data_0.json: generated/%/timing_main
	./$< 0 > $@

generated/%/timing_data_1.json: generated/%/timing_main
	./$< 1 > $@

generated/%/timing_data_2.json: generated/%/timing_main
	./$< 2 > $@

generated/%/timing_data_3.json: generated/%/timing_main
	./$< 3 > $@


generated/%/timing_main: generated/%/timing_main.c generated/%/funcs.o ${OBJS}
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
