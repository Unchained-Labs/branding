# Unchained Labs brand system.
#
# tokens/tokens.css is the source of truth for colour. tools/mkmark.py is the
# source of truth for the mark's geometry. Everything else in this repo is
# generated and safe to delete.
#
# The rasterisers run in containers rather than expecting a local toolchain:
# this repo gets opened on whatever machine is to hand, and a brand repo should
# not require an install to read.

.DEFAULT_GOAL := help
PY ?= python3

.PHONY: help
help: ## show this help
	@grep -hE '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) \
	  | awk -F':.*?## ' '{printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

.PHONY: tokens
tokens: ## regenerate tokens.json + tailwind.css from tokens.css (fails on a contrast tier breach)
	$(PY) tools/build-tokens.py

.PHONY: contrast
contrast: ## print every documented colour pair and its measured ratio
	$(PY) tools/contrast.py

.PHONY: verify-docs
verify-docs: ## assert every ratio written in tokens.css and brand/*.md matches measurement
	$(PY) tools/verify-docs.py

.PHONY: wordmark
wordmark: ## re-derive the wordmark outlines from the vendored Space Grotesk
	cd tools && $(PY) mkwordmark.py > wordmark.json && echo "ok  tools/wordmark.json"

.PHONY: logo
logo: ## rebuild every SVG from geometry + wordmark
	cd tools && $(PY) mkmark.py

.PHONY: png
png: ## rasterise every SVG at every documented size
	docker run --rm -v "$(CURDIR)":/w -w /w debian:bookworm-slim sh tools/render-png.sh

.PHONY: palette-image
palette-image: ## rebuild the palette hero image
	docker run --rm -v "$(CURDIR)":/w -w /w debian:bookworm-slim sh tools/render-palette.sh

.PHONY: verify
verify: ## check the rendered PNGs are the sizes and inks they claim
	docker run --rm -v "$(CURDIR)":/w -w /w python:3-slim sh -c \
	  'pip install -q pillow && python tools/verify-png.py'

.PHONY: check
check: tokens verify-docs ## everything CI runs that needs no container
	@echo "ok  brand system consistent"

.PHONY: all
all: wordmark logo tokens png palette-image verify verify-docs ## full rebuild from source

.PHONY: site
site: ## vendor tokens + stylesheet + assets into docs/ for GitHub Pages
	@mkdir -p docs/assets/png
	@cp tokens/tokens.css site/brand.css docs/assets/
	@cp assets/logo/favicon.svg assets/logo/mark-accent.svg assets/logo/mark-dark.svg \
	    assets/logo/lockup-horizontal.svg assets/logo/lockup-stacked.svg docs/assets/
	@cp assets/palette/tokens.png docs/assets/
	@for s in 16 32 48 64 128; do cp assets/logo/png/mark-accent-$$s.png docs/assets/png/; done
	@echo "ok  docs/assets vendored from tokens/, site/ and assets/"
