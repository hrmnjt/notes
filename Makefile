# Makefile

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = src/documentation/source
BUILDDIR      = src/documentation/build
DOCSDIR       = docs

# Put it first so that "make" without argument is like "make help".
.PHONY: help Makefile
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


.PHONY: html
html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "Regenerated all docs"
	@rm -rf $(DOCSDIR)
	@mkdir -p $(DOCSDIR)
	@cp -r $(BUILDDIR)/html/. $(DOCSDIR)/
	@echo "" > $(DOCSDIR)/.nojekyll
	@echo "Replaced latest generated docs in /docs folder"


.PHONY: clean
clean:
	@rm -rf $(BUILDDIR)/*
	@echo "Cleaned build directory"
	@rm -rf $(DOCSDIR)
	@echo "Cleaned GH docs directory"


.PHONY: cleanhtml
cleanhtml: clean html
