PROJECT = main

all: $(PROJECT).pdf

.PHONY: clean view purge

clean:
	-rm *.aux *.blg *.out *.bbl *.log *.dvi

purge: clean
	-rm $(PROJECT).pdf

$(PROJECT).pdf: $(PROJECT).tex bibliography.bib
	pdflatex $(PROJECT).tex
	bibtex $(PROJECT)
	pdflatex $(PROJECT).tex
	pdflatex $(PROJECT).tex

view:
	open $(PROJECT).pdf