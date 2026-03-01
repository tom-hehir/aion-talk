PRES_DIR  := presentation
MAIN      := presentation
BUILD_DIR := build
PDF       := $(BUILD_DIR)/$(MAIN).pdf

.PHONY: all clean mrproper release

all: $(PDF)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(PDF): $(PRES_DIR)/$(MAIN).tex | $(BUILD_DIR)
	cd $(PRES_DIR) && latexmk -lualatex -output-directory=../$(BUILD_DIR) \
	    -interaction=nonstopmode -halt-on-error $(MAIN).tex

clean:
	cd $(PRES_DIR) && latexmk -c -output-directory=../$(BUILD_DIR) $(MAIN).tex

mrproper:
	rm -rf $(BUILD_DIR)

# Copy built PDF to repo root, then: git add -f presentation.pdf && git commit && git tag <occasion>
release: $(PDF)
	cp $(PDF) $(MAIN).pdf
