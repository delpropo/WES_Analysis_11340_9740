# Getting Started

## Prerequisites

- Access to the Great Lakes HPC cluster (University of Michigan)
- Conda/Mamba for environment management
- Snakemake ≥8.0.0

## Setup

### 1. Clone the analysis repository

```bash
git clone https://github.com/delpropo/WES_Analysis_11340_9740.git
cd WES_Analysis_11340_9740
```

### 2. Set up the processing pipeline

The post-variant-calling pipeline is maintained in a separate repository:

```bash
git clone https://github.com/Speech-Neurophysiology-Lab/post-calling-snakemake-workflow.git
```

See the [pipeline README](https://github.com/Speech-Neurophysiology-Lab/post-calling-snakemake-workflow/blob/main/README.md) for full installation and configuration instructions.

### 3. Configure the pipeline

Edit `config/config.yaml` in the pipeline repository to point to your BCF files and set processing options. See [config/README.md](https://github.com/Speech-Neurophysiology-Lab/post-calling-snakemake-workflow/blob/main/config/README.md) for parameter documentation.

### 4. Data locations

- **Raw sequencing data**: `/nfs/turbo/umms-sooeunc/9790-JD` and `/nfs/turbo/umms-sooeunc/13340-JD`
- **Analysis working directory**: `/nfs/turbo/umms-sooeunc/analysis/WES_varloc/`
- **Backup**: Dropbox (MSA-ChangLabUM/ImagingGenetics/DNA processing/seq_data_backup)
