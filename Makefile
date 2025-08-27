install:
	pip install -r requirements.txt

run-help:
	python3 src/python_foundation/cli.py --help

dryrun:
	python3 src/python_foundation/cli.py --root ./sample --pattern "{stem_slug}_{num:03}{ext}" --dry-run

apply:
	python3 src/python_foundation/cli.py --root ./sample --pattern "{stem_slug}_{num:03}{ext}" --apply

test:
	pytest -v
