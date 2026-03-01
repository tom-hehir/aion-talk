PRES_DIR      := presentation
MAIN          := presentation
BUILD_DIR     := build
RESOURCES_DIR := resources
PDF           := $(BUILD_DIR)/$(MAIN).pdf

MAIN_PAPER_DIR := $(RESOURCES_DIR)/aion-1-paper

# Set DEBUG=1 to skip post-build cleanup of lualatex artefacts in $(PRES_DIR)/
DEBUG ?= 0

.PHONY: all clean mrproper tidy-pres fetch release

all: $(PDF)

# ── fetch ─────────────────────────────────────────────────────────────────────
fetch:
	uv run scripts/fetch-resources.py

# ── build ─────────────────────────────────────────────────────────────────────
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(PDF): $(PRES_DIR)/$(MAIN).tex | $(BUILD_DIR)
	@test -d $(MAIN_PAPER_DIR)/source || \
	    (echo "ERROR: run 'make fetch' first." && exit 1)
	latexmk -interaction=nonstopmode -halt-on-error $(PRES_DIR)/$(MAIN).tex
	@if [ "$(DEBUG)" != "1" ]; then \
	    rm -f $(PRES_DIR)/$(MAIN).fdb_latexmk \
	          $(PRES_DIR)/$(MAIN).fls \
	          $(PRES_DIR)/$(MAIN).log; \
	fi

# ── clean ─────────────────────────────────────────────────────────────────────
clean:
	latexmk -c $(PRES_DIR)/$(MAIN).tex

mrproper:
	rm -rf $(BUILD_DIR)

tidy-pres:
	rm -f $(PRES_DIR)/$(MAIN).fdb_latexmk \
	      $(PRES_DIR)/$(MAIN).fls \
	      $(PRES_DIR)/$(MAIN).log

# ── release ───────────────────────────────────────────────────────────────────
# Copy built PDF to repo root, then: git add -f presentation.pdf && git commit && git tag <occasion>
release: $(PDF)
	cp $(PDF) $(MAIN).pdf
