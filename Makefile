#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = WES_Analysis_11340_9740
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Update for use with conda or uv as decision is made.  Ruff linter.  Update so it can be run with slurm

## Install Python dependencies
.PHONY: requirements
requirements:
	bash -c "source ~/.bashrc && module load uv && uv sync --extra dev"




## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## Lint using ruff (use `make format` to do formatting)
.PHONY: lint
lint:
	ruff format --check
	ruff check

## Format source code with ruff
.PHONY: format
format:
	ruff check --fix
	ruff format



## Run tests
.PHONY: test
test:
	python -m pytest tests


## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	bash -c "source ~/.bashrc && module load uv && uv venv --python $(PYTHON_VERSION)"
	@echo ">>> New uv virtual environment created. Activate with:"
	@echo ">>> Windows: .\\\\.venv\\\\Scripts\\\\activate"
	@echo ">>> Unix/macOS: source ./.venv/bin/activate"




#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


## Make dataset
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) WES_Analysis_11340_9740/dataset.py

## Combine gene references
.PHONY: combine_genes
combine_genes: requirements
	$(PYTHON_INTERPRETER) WES_Analysis_11340_9740/combine_gene_references.py

## Start Jupyter notebook with SLURM (1 CPU, 7GB memory)
.PHONY: notebook
notebook:
	srun --cpus-per-task=1 --mem=7G --time=1:00:00 --pty bash -c "module load uv &&  source .venv/bin/activate && jupyter lab notebooks/20250805.ipynb --no-browser --ip=0.0.0.0 --port=8888"

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
