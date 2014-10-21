TARGETS = main.pdf note.pdf

all: $(TARGETS)

%.pdf: %.tex
	pdflatex $*
	bibtex $*
	pdflatex $*
	pdflatex $*
	make clean

main.pdf: bibliography.bib

note: note.pdf bibliography.bib
	open note.pdf

.PHONY: clean view purge note

clean:
	-@rm -rf *.aux *.blg *.out *.bbl *.log *.dvi *.tdo *.fdb_latexmk *.fls *.toc

purge: clean
	-@rm -rf $(TARGETS)

view: $(TARGETS)
	open $(TARGETS)