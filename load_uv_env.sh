module purge
if [[ ! -z "$CONDA_DEFAULT_ENV" ]]; then
    while [[ "$CONDA_DEFAULT_ENV" != "base" && ! -z "$CONDA_DEFAULT_ENV" ]]; do
        conda deactivate
    done
fi
module load uv
source .venv/bin/activate

