

.PHONY: build
build: bin/script


bin/script: requirements/done | bin
	$(RM) $@
	cd bin && ln -s ../src/script.py script
	chmod +x $@

bin/nightly.sh: bin/script
	$(RM) $@
	cd bin && ln -s ../src/nightly.sh nightly.sh
	chmod +x $@

.PHONY: nightly
nightly: bin/nightly.sh
	$<

requirements/done: requirements/build.sh
	$<

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec ${RM} -r {} +

.PHONY: clean-requirements
clean-requirements: requirements/clean.sh
	$<

.PHONY: distclean
distclean: clean clean-requirements
	$(RM) -r bin
	$(RM) -r nightlies

bin:
	mkdir bin
