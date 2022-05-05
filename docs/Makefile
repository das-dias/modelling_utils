BUILDDIR=build
FILENAME=main
METADATA=meta
TEMPLATE=myIEEEtrantemplate
# Commands to create the pdf document using pandoc

#--epub-cover-image=<cover-image> : Set the cover image for epub output.

all: paper

pdf:
	mkdir $(BUILDDIR) -p
	pandoc $(FILENAME).$(EXTENSION) $(METADATA).yaml \
	--filter pandoc-citeproc \
	--from=markdown+tex_math_single_backslash+tex_math_dollars+raw_tex \
	--to=latex \
	--output=$(BUILDDIR)/$(FILENAME).pdf \
	--pdf-engine=xelatex
html:
	mkdir $(BUILDDIR) -p
	pandoc $(FILENAME).$(EXTENSION) $(METADATA).yaml \
	--filter pandoc-citeproc \
	--from=markdown+tex_math_single_backslash+tex_math_dollars \
    --to=html5 \
    --output=$(BUILDDIR)/$(FILENAME).html \
    --mathjax \
    --self-contained

epub: # for E-book generation
	mkdir $(BUILDDIR) -p
    pandoc $(FILENAME).$(EXTENSION) $(METADATA).yaml \
	--filter pandoc-citeproc \
	--from=markdown+tex_math_single_backslash+tex_math_dollars \
    --to=epub \
    --output=$(BUILDDIR)/$(FILENAME).epub \
    --toc

paper:
	pandoc -s \
	--citeproc \
	--natbib \
	$(METADATA).yaml \
	--template=$(TEMPLATE).tex \
	-N \
	-f markdown \
	-t latex+raw_tex \
	-o $(FILENAME).tex $(FILENAME).md
	pdflatex $(FILENAME).tex &> /dev/null
	bibtex $(FILENAME) &> /dev/null
	pdflatex $(FILENAME).tex &> /dev/null
	pdflatex $(FILENAME).tex &> /dev/null

clean:
	rm $(FILENAME).aux $(FILENAME).tex $(FILENAME).log $(FILENAME).bbl $(FILENAME).blg $(FILENAME).out

.PHONY: all clean paper