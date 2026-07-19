PYTHON ?= python3
REPORT ?= report.yaml

.PHONY: check render report test clean

check:
	$(PYTHON) scripts/render_report.py --check $(REPORT)

render:
	$(PYTHON) scripts/render_report.py $(REPORT)

report: render
	latexmk -silent -jobname=weekly-report main.tex

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

clean:
	latexmk -c -jobname=weekly-report main.tex
