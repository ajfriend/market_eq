TARGETS = market_eq.pdf

all: $(TARGETS)

%.pdf: %.tex
	pdflatex $*
	bibtex $*
	pdflatex $*
	pdflatex $*
	make clean

market_eq.pdf: bibliography.bib

scratch: scratch.pdf bibliography.bib
	open scratch.pdf

.PHONY: clean view purge scratch

clean:
	-@rm -rf *.aux *.blg *.out *.bbl *.log *.dvi *.tdo *.fdb_latexmk *.fls *.toc

purge: clean
	-@rm -rf $(TARGETS)

view: $(TARGETS)
	open $(TARGETS)