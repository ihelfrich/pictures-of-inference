# =============================================
# Pictures of Inference - build system
# =============================================
#
# Common targets:
#   make pdf        Build the full book PDF
#   make figures    Regenerate all figures
#   make ch01       Build chapter 1 standalone
#   make clean      Remove build artifacts
#   make distclean  Remove build artifacts AND figures
#   make watch      Rebuild on file changes (requires entr)
#   make check      Style check the prose

PROSE_DIR  := prose
FIGS_DIR   := pictures/figures
BUILD_DIR  := build/pdf
PYTHON     ?= python3
PDFLATEX   ?= pdflatex -interaction=nonstopmode -halt-on-error

.PHONY: pdf figures clean distclean help check ch% watch

help:
	@echo "Pictures of Inference - build targets"
	@echo "  make pdf       Build the full book PDF"
	@echo "  make figures   Regenerate all figures"
	@echo "  make chXX      Build chapter XX standalone"
	@echo "  make clean     Remove .aux, .log, etc."
	@echo "  make distclean Also remove generated figures"
	@echo "  make check     Check prose for banned phrases"

# ---------- Figures ----------

figures:
	@echo "Regenerating all figures..."
	@cd $(FIGS_DIR) && $(PYTHON) generate_all.py

fig_%:
	@echo "Regenerating chapter $* figures..."
	@cd $(FIGS_DIR) && $(PYTHON) generate_all.py --ch $*

# ---------- Full PDF ----------
# Build inside prose/ so \include can write aux files there,
# then copy the final pdf to build/pdf/.

pdf: figures
	@echo "Building full book..."
	@mkdir -p $(BUILD_DIR)
	@cd $(PROSE_DIR) && $(PDFLATEX) main.tex > /dev/null
	@cd $(PROSE_DIR) && $(PDFLATEX) main.tex > /dev/null
	@cp $(PROSE_DIR)/main.pdf $(BUILD_DIR)/main.pdf
	@echo "  -> $(BUILD_DIR)/main.pdf"

# ---------- Chapter-only build ----------

ch%:
	@echo "Building chapter $* standalone..."
	@$(PYTHON) tools/build_chapter.py $*

# ---------- Style check ----------

check:
	@$(PYTHON) tools/style_check.py

# ---------- Cleanup ----------

clean:
	@echo "Cleaning build artifacts..."
	@find $(PROSE_DIR) -name "*.aux" -delete
	@find $(PROSE_DIR) -name "*.log" -delete
	@find $(PROSE_DIR) -name "*.out" -delete
	@find $(PROSE_DIR) -name "*.toc" -delete
	@find $(PROSE_DIR) -name "*.lof" -delete
	@find $(PROSE_DIR) -name "*.lot" -delete
	@rm -f $(PROSE_DIR)/main.pdf

distclean: clean
	@echo "Removing generated figures and build/..."
	@rm -rf $(FIGS_DIR)/output/
	@rm -rf build/

# ---------- Watch mode ----------

watch:
	@echo "Watching for changes... (Ctrl-C to stop)"
	@find $(PROSE_DIR) $(FIGS_DIR) -type f \( -name "*.tex" -o -name "*.py" \) | \
		entr -c make pdf
