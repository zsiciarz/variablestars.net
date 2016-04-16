.PHONY: test watch elm-test

WEBPACK = ./node_modules/.bin/webpack
WEBPACK_ARGS = --colors --progress
ELM_PACKAGE = elm-package
ELM_TEST_DIR = assets/js/tests

test:
	py.test --cov

production_assets: node_modules
	$(WEBPACK) $(WEBPACK_ARGS)

watch: elm-stuff
	$(WEBPACK) $(WEBPACK_ARGS) --watch

node_modules: package.json
	@npm install

elm-stuff: node_modules elm-package.json
	$(ELM_PACKAGE) install -y

$(ELM_TEST_DIR)/elm-stuff: $(ELM_TEST_DIR)/elm-package.json
	cd $(ELM_TEST_DIR) && $(ELM_PACKAGE) install -y

elm-test: $(ELM_TEST_DIR)/elm-stuff
	cd $(ELM_TEST_DIR) && elm-test TestRunner.elm
