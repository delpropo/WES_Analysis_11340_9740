# WES Analysis Documentation

Project-specific methodology documentation for the 11340/9740 stuttering WES analysis.

## Contents

| Document | Description |
|----------|-------------|
| [filtering.md](filtering.md) | Filtering criteria: FDR thresholds, allele frequency cutoffs, functional impact, gene list restriction, QC coverage |
| [individual_analysis.md](individual_analysis.md) | Individual-level analysis: gene group stratification, variant class analysis, chromosome-wise counting, heatmaps |
| [qc.md](qc.md) | Quality control validation: gene selection verification, coding status, variant class distribution, count consistency |
| [archive/timeline.md](archive/timeline.md) | Original project timeline (archived) |

## Related

- **Processing Pipeline**: [post-calling-snakemake-workflow](https://github.com/Speech-Neurophysiology-Lab/post-calling-snakemake-workflow) — The Snakemake pipeline used for BCF processing, aggregation, and GOI analysis
- **Gene References**: [references/](../references/) — Curated gene lists for stuttering, ADHD, tic disorders, ASD, and related conditions
- **Project README**: [README.md](../README.md) — Full project overview and workflow description
