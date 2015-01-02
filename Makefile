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


#this checks the spelling in the latex file. must have \usepackage{spelling} in the header
#for this to work
# the spelling package only works with luatex, so comment it out for regular pdflatex
spell:
	latexmk -C #clean out the directory of temp files
	lualatex market_eq.tex # generate file.spell.txt to spellcheck
	# send the text through the aspell spellchecker, getting a list of bad words
	cat market_eq.spell.txt | aspell list > market_eq.spell.bad

	# rerun, with the lsit of bad words created, so that they can be highlighted
	# the lualatexmk script is from the latest version of TexShop
	~/Library/TeXShop/Engines/lualatexmk.engine market_eq.tex
	latexmk -c # clean, but don't delete the final pdf
	open market_eq.pdf
