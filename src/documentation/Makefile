
# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
.PHONY: help Makefile
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


.PHONY: html
html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "Regenerated all docs"
	@rm -rf ../../docs
	@mkdir -p ../../docs
	@cp -r $(BUILDDIR)/html/. ../../docs/
	@echo "" > ../../docs/.nojekyll
	@echo "Replaced latest generated docs in /docs folder"

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
# %: Makefile
# 	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


.PHONY: clean
clean:
	@rm -rf $(BUILDDIR)/*
	@echo "Cleaned build directory"
	@rm -rf ../../docs
	@echo "Cleaned GH docs directory"


.PHONY: cleanhtml
cleanhtml: clean html
