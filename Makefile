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
	-@rm -rf *.aux *.blg *.out *.bbl *.log *.dvi

purge: clean
	-@rm -rf $(TARGETS)

view: $(TARGETS)
	open $(TARGETS)