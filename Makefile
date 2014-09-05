TARGETS = main.pdf

all: $(TARGETS)

%.pdf: %.tex
	pdflatex $*
	bibtex $*
	pdflatex $*
	pdflatex $*
	make clean

main.pdf: bibliography.bib

.PHONY: clean view purge

clean:
	-rm *.aux *.blg *.out *.bbl *.log *.dvi

purge: clean
	-rm $(TARGETS)

view:
	open $(TARGETS)