.PHONY: test watch

WEBPACK = ./node_modules/.bin/webpack
WEBPACK_ARGS = --colors --progress
ELM_PACKAGE = ./node_modules/.bin/elm-package

test:
	coverage run manage.py test --keepdb

production_assets: node_modules
	$(WEBPACK) $(WEBPACK_ARGS)

watch: node_modules elm-stuff
	$(WEBPACK) $(WEBPACK_ARGS) --watch

node_modules: package.json
	@npm install

elm-stuff: node_modules elm-package.json
	$(ELM_PACKAGE) install -y
