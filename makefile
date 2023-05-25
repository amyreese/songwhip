install:
	python -m pip install -Ue .[dev]

.venv:
	python -m venv .venv
	source .venv/bin/activate && make install
	echo 'run `source .venv/bin/activate` to activate virtualenv'

venv: .venv

test:
	python -m unittest -v songwhip
	python -m mypy -p songwhip --non-interactive --install-types

lint:
	python -m flake8 songwhip
	python -m ufmt check songwhip

format:
	python -m ufmt format songwhip

release: lint test clean
	flit publish

clean:
	rm -rf .mypy_cache build dist html *.egg-info

distclean: clean
	rm -rf .venv
