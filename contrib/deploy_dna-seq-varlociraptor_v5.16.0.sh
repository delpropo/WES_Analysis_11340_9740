# Author: Jim Delproposto
# Date: 2025-04-23

# check if conda is installed
if ! command -v conda &> /dev/null
then
    echo "conda could not be found"
    exit
fi

# exit if the conda environment already exists
if conda env list | grep -q varloc_env; then
    echo "Conda environment already exists."

fi

# check to see if the conda environment exists
if ! conda env list | grep -q varloc_env; then
    echo "Creating conda environment"
    conda create -n varloc_env
    conda activate varloc_env

fi

# install mamba, snakedeploy and snakemake
conda install -c conda-forge mamba
mamba install -c bioconda snakedeploy snakemake


# ask user if they want to install the workflow in the current directory
read -p "Do you want to install the workflow in the current directory? (y/n) " answer
if [[ $answer == "y" ]]; then
    echo "Installing workflow in current directory"
    # download the workflow
    snakedeploy deploy-workflow https://github.com/snakemake-workflows/dna-seq-varlociraptor . --tag v5.16.0
    # download bash script https://github.com/delpropo/Umich_HPC/blob/main/snakemake_on_the_cluster/scripts/nonslurm_dryrun.sh
    # wget https://raw.githubusercontent.com/delpropo/Umich_HPC/main/snakemake_on_the_cluster/scripts/nonslurm_dryrun.sh


else
    # ask user to create and move to the directory and rerun the script
    read -p "Please create a directory and move to it, then rerun the script. Press enter to continue"
    echo "Exiting script"


