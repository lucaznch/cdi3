# Each script scripts/<name>.py generates the figure fig/<name>.pdf
PYTHON ?= python3

FIGS := $(patsubst scripts/%.py,fig/%.pdf,$(wildcard scripts/*.py))

all:
	latexmk -pdf cdi3.tex ; latexmk -c

figs: $(FIGS)

fig/%.pdf: scripts/%.py
	$(PYTHON) $<

clean:
	latexmk -C

.PHONY: all figs clean
