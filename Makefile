PRES_DIR      := presentation
MAIN          := presentation
BUILD_DIR     := build
RESOURCES_DIR := resources
PDF           := $(BUILD_DIR)/$(MAIN).pdf

MAIN_PAPER_ID  := 2510.17960
MAIN_PAPER_DIR := $(RESOURCES_DIR)/aion-1-paper

.PHONY: all clean mrproper fetch release

all: $(PDF)

# ── fetch ─────────────────────────────────────────────────────────────────────
fetch: $(MAIN_PAPER_DIR)/source

$(MAIN_PAPER_DIR)/source:
	./scripts/fetch-paper.sh $(MAIN_PAPER_ID) $(MAIN_PAPER_DIR)

# ── build ─────────────────────────────────────────────────────────────────────
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(PDF): $(PRES_DIR)/$(MAIN).tex | $(BUILD_DIR)
	@test -d $(MAIN_PAPER_DIR)/source || \
	    (echo "ERROR: $(MAIN_PAPER_DIR)/source not found — run 'make fetch' first." && exit 1)
	cd $(PRES_DIR) && latexmk -lualatex -output-directory=../$(BUILD_DIR) \
	    -interaction=nonstopmode -halt-on-error $(MAIN).tex

# ── clean ─────────────────────────────────────────────────────────────────────
clean:
	cd $(PRES_DIR) && latexmk -c -output-directory=../$(BUILD_DIR) $(MAIN).tex

mrproper:
	rm -rf $(BUILD_DIR)

# ── release ───────────────────────────────────────────────────────────────────
# Copy built PDF to repo root, then: git add -f presentation.pdf && git commit && git tag <occasion>
release: $(PDF)
	cp $(PDF) $(MAIN).pdf
