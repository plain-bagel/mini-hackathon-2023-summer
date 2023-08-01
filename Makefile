# Makefile
.PHONY: install clean format

#py-files := $(filter-out exploration.py, $(shell git ls-files '*.py'))
py-files := .

## Install for production
install:
	@echo ">> Installing dependencies"
	python -m pip install --upgrade pip setuptools wheel
	python -m pip install -e .


## Install for development
install-dev:
	@echo ">> Installing dependencies"
	python -m pip install -e ".[dev]"


## Clean up
clean:
	@echo ">> Cleaning up"
	@rm -rf build dist .pytest_cache .mypy_cache .ruff_cache __pycache__ .coverage htmlcov
	@rm -rf *.egg-info **/*.egg-info **/__pycache__ **/*.pyc


## Format code (black + ruff)
format:
	@black $(py-files)
	@ruff --fix $(py-files)


## Lint code (black + ruff + mypy)
static-checks:
	@black --diff --check $(py-files)
	@ruff $(py-files)
	@mypy --install-types --non-interactive $(py-files)
.PHONY: lint


## Anchor dependencies with pip-tools
anchor:
	python -m pip install --upgrade pip
	python -m pip install pip-tools
	pip-compile --resolver=backtracking --output-file=requirements.txt pyproject.toml
	pip-compile --resolver=backtracking --output-file=requirements-dev.txt pyproject.toml

## Build using Hatch/Hatchling
build:
	@hatch -v build


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available commands:$$(tput sgr0)"
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
