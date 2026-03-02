PRES_DIR      := presentation
MAIN          := presentation
BUILD_DIR     := presentation/build
RESOURCES_DIR := resources
PDF           := $(BUILD_DIR)/$(MAIN).pdf

PAPERS_DIR        := $(RESOURCES_DIR)/papers
MAIN_PAPER_DIR    := $(PAPERS_DIR)/aion-1-paper
PAPER_SRC_DIR     := $(MAIN_PAPER_DIR)/source
TITLEPAGE_STANDALONE := $(PRES_DIR)/titlepage-standalone.tex
TITLEPAGE_PDF     := $(RESOURCES_DIR)/titlepage.pdf

.PHONY: all clean mrproper fetch bibliography release tables

all: $(PDF)

# ── fetch ─────────────────────────────────────────────────────────────────────
fetch:
	uv run scripts/fetch-resources.py

# ── bibliography (regenerate .bib from notes/*.yaml) ─────────────────────────
bibliography:
	uv run scripts/update-bibliography.py

# ── tables (render paper tables to cached PDFs) ───────────────────────────────
tables:
	uv run scripts/render-tables.py

# ── titlepage (rendered from paper source, pdfcropped) ────────────────────────
$(TITLEPAGE_PDF): $(TITLEPAGE_STANDALONE)
	@test -d $(PAPER_SRC_DIR) || \
	    (echo "ERROR: run 'make fetch' first." && exit 1)
	cp $(TITLEPAGE_STANDALONE) $(PAPER_SRC_DIR)/titlepage-standalone.tex
	cd $(PAPER_SRC_DIR) && pdflatex -interaction=nonstopmode titlepage-standalone.tex
	pdfcrop $(PAPER_SRC_DIR)/titlepage-standalone.pdf $(TITLEPAGE_PDF)

# ── build ─────────────────────────────────────────────────────────────────────
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(PDF): $(PRES_DIR)/$(MAIN).tex $(TITLEPAGE_PDF) | $(BUILD_DIR)
	@test -d $(MAIN_PAPER_DIR)/source || \
	    (echo "ERROR: run 'make fetch' first." && exit 1)
	cd $(PRES_DIR) && latexmk -interaction=nonstopmode -halt-on-error $(MAIN).tex

# ── clean ─────────────────────────────────────────────────────────────────────
clean:
	cd $(PRES_DIR) && latexmk -c $(MAIN).tex

mrproper:
	rm -rf $(BUILD_DIR)

# ── release ───────────────────────────────────────────────────────────────────
# Copy built PDF to repo root, then: git add -f presentation.pdf && git commit && git tag <occasion>
release: $(PDF)
	cp $(PDF) $(MAIN).pdf
