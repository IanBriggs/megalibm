

.PHONY: build
build: bin/megalibm_identities bin/megalibm_template_identities bin/megalibm_generate


.PHONY: requirements
requirements: requirements/done

bin/megalibm_identities: requirements/done | bin
	$(RM) $@
	cd bin && ln -s ../src/megalibm_identities.py megalibm_identities

bin/megalibm_template_identities: requirements/done | bin
	$(RM) $@
	cd bin && ln -s ../src/megalibm_template_identities.py megalibm_template_identities

bin/megalibm_generate: requirements/done | bin
	$(RM) $@
	cd bin && ln -s ../src/megalibm_generate.py megalibm_generate

bin/nightly.sh: build
	$(RM) $@
	cd bin && ln -s ../src/nightly.sh nightly.sh

.PHONY: nightly
nightly: bin/nightly.sh
	rm requirements/done # force a rebuild for now
	make requirements
	$<

bin/mini_nightly.sh: build
	$(RM) $@
	cd bin && ln -s ../src/mini_nightly.sh mini_nightly.sh
	chmod +x $@

.PHONY: mini_nightly
mini_nightly: bin/mini_nightly.sh
	rm requirements/done requirements/snake_egg/done
	make requirements
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
