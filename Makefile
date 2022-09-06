

.PHONY: build
build: bin/megalibm_identities


.PHONY: requirements
requirements: requirements/done

bin/script: requirements/done | bin
	$(RM) $@
	cd bin && ln -s ../src/megalibm_identities.py megalibm_identities
	chmod +x $@

bin/nightly.sh: bin/megalibm_identities
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
	$(MAKE) -C measurement clean

.PHONY: clean-requirements
clean-requirements: requirements/clean.sh
	$<

.PHONY: distclean
distclean: clean clean-requirements
	$(RM) -r bin
	$(RM) -r nightlies
	$(MAKE) -C measurement distclean

bin:
	mkdir bin
