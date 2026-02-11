# Original Expected Outcomes & Potential Pitfalls (Archived)

> **Note:** These sections were written during project planning (April 2025) and are preserved for historical reference. See the main [README.md](../../README.md) for current project status.

## Expected Outcomes (Original)

- A well-documented dataset of identified variants, suitable for future research, regardless of whether variants directly linkable to stuttering are found.
- **Minimum Deliverable**: Well-documented WES dataset even if no significant variants are found.
    - Fastq files, associated documents from the core, md5 checksum files, tables with sample id and metadata.
- **Best Case:** Identification of one or more variants strongly associated with stuttering, enabling correlation studies with existing MRI data.

## Potential Pitfalls (Original)

- **Sequencing Quality:** There is a possibility of low quality sequencing data or failures in one or more samples. Analysis will be performed on the data that is available.
- **Pipeline Issues:** Variant identification pipelines are always improving. The current pipeline may miss variants or not have enough annotation. Pipeline risk was reduced by running it on the initial 12 samples before processing all 71.
- **Storage:** The size of the data may be larger than expected, and storage space should be monitored. A large number of intermediary files can be created during WES analysis. Additional storage may be needed on the Great Lakes cluster.
