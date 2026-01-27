all:
	latexmk -pdf cdi3.tex ; latexmk -c

clean:
	latexmk -C

