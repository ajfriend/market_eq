TARGETS = market_eq.pdf

all: $(TARGETS)

%.pdf: %.tex
	pdflatex $*
	bibtex $*
	pdflatex $*
	pdflatex $*
	make clean

market_eq.pdf: bibliography.bib

market_eq_long.pdf: bibliography.bib

.PHONY: clean view purge

clean:
	-@rm -rf *.aux *.blg *.out *.bbl *.log *.dvi *.tdo *.fdb_latexmk *.fls *.toc

purge: clean
	-@rm -rf $(TARGETS)

view: $(TARGETS)
	open $(TARGETS)