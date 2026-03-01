PRES_DIR      := presentation
MAIN          := presentation
BUILD_DIR     := presentation/build
RESOURCES_DIR := resources
PDF           := $(BUILD_DIR)/$(MAIN).pdf

MAIN_PAPER_DIR := $(RESOURCES_DIR)/aion-1-paper

.PHONY: all clean mrproper fetch release

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

# ── clean ─────────────────────────────────────────────────────────────────────
clean:
	latexmk -c $(PRES_DIR)/$(MAIN).tex

mrproper:
	rm -rf $(BUILD_DIR)

# ── release ───────────────────────────────────────────────────────────────────
# Copy built PDF to repo root, then: git add -f presentation.pdf && git commit && git tag <occasion>
release: $(PDF)
	cp $(PDF) $(MAIN).pdf
