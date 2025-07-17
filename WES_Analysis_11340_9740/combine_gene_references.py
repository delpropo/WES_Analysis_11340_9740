#!/usr/bin/env python3

import pandas as pd
from datetime import datetime
from pathlib import Path

# Get current date for the output filename
current_date = datetime.now().strftime('%Y%m%d')

# Define paths
base_dir = Path('/nfs/turbo/umms-sooeunc/analysis/WES_Analysis_11340_9740')
ref_dir = base_dir / 'references'
genes_dir = ref_dir / 'genes'
output_file = ref_dir / f'{current_date}_combined_info.tsv'

# Dictionary mapping files to their disease/pathway association
file_association = {
    'Parkinsons_genes.tsv': 'parkinsons',
    '20250529_GeneCards-Parkinsons.csv': 'parkinsons',
    'Autism_genes.tsv': 'autism',
    '20250529_GeneCards-Autism.csv': 'autism',
    'ADHD_genes.tsv': 'ADHD',
    '20250529_GeneCards-ADHD.csv': 'ADHD',
    'Stuttering_genes.tsv': 'stuttering',
    '20250529_GeneCards-stuttering.csv': 'stuttering',
    'Tic_Disorders_genes.tsv': 'tic',
    '20250529_GeneCards-Tic.csv': 'tic',
    'Intracellular_Trafficking_genes.tsv': 'intracellular_trafficking',
    'Basal_Ganglia_genes.tsv': 'basal_ganglia',
}

def read_and_process_file(file_path, association):
    """Read a file and process it to ensure it has the required columns."""
    # Determine file type and read accordingly
    if file_path.suffix == '.csv':
        df = pd.read_csv(file_path)
    else:  # .tsv
        df = pd.read_csv(file_path, sep='\t')

    # Check for Gene Symbol column
    if 'Gene Symbol' not in df.columns:
        raise ValueError(f"File {file_path.name} does not contain a 'Gene Symbol' column")

    # Add Disease_or_Pathway_Association if it doesn't exist
    if 'Disease_or_Pathway_Association' not in df.columns:
        df['Disease_or_Pathway_Association'] = association

    return df

def main():
    # List to store all dataframes
    dfs = []

    # Process each file
    for file_name, association in file_association.items():
        file_path = genes_dir / file_name
        if file_path.exists():
            try:
                df = read_and_process_file(file_path, association)
                dfs.append(df)
                print(f"Successfully processed {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {str(e)}")
        else:
            print(f"File not found: {file_name}")

    if not dfs:
        print("No files were successfully processed")
        return

    # Combine all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)

    # Remove duplicate rows
    combined_df = combined_df.drop_duplicates()

    print(f"\nInitial combined data shape: {combined_df.shape}")
    print(f"Columns in combined data: {list(combined_df.columns)}")

    # Determine the number of unique Gene Symbols
    unique_genes = combined_df['Gene Symbol'].nunique()
    print(f"Number of unique Gene Symbols: {unique_genes}")
    print("This should be the final number of rows after pivoting.")

    # Check if we have the required columns for pivoting
    required_cols = ['Gene Symbol', 'Description', 'Category']
    missing_cols = [col for col in required_cols if col not in combined_df.columns]
    if missing_cols:
        print(f"WARNING: Missing required columns for pivoting: {missing_cols}")
        print("Available columns:", list(combined_df.columns))

    # Create a composite key for validation
    combined_df['composite_key'] = combined_df['Gene Symbol'].astype(str) + '|' + \
                                  combined_df.get('Description', '').astype(str) + '|' + \
                                  combined_df.get('Category', '').astype(str)

    # Check for duplicate composite keys within the same disease/pathway
    duplicate_keys = combined_df.groupby(['composite_key', 'Disease_or_Pathway_Association']).size()
    duplicate_keys = duplicate_keys[duplicate_keys > 1]

    if len(duplicate_keys) > 0:
        print(f"\nWARNING: Found {len(duplicate_keys)} duplicate composite keys within same disease/pathway:")
        print(duplicate_keys.head(10))
        print("Removing duplicates by keeping first occurrence...")
        combined_df = combined_df.drop_duplicates(subset=['composite_key', 'Disease_or_Pathway_Association'], keep='first')

    # Pivot on Gene Symbol, creating columns for each disease/pathway
    print("\nPivoting data with Gene Symbol as index...")

    # Create presence/absence indicators
    presence_pivot = pd.crosstab(
        combined_df['Gene Symbol'],
        combined_df['Disease_or_Pathway_Association']
    ).astype(bool)

    print(f"Presence pivot shape: {presence_pivot.shape}")
    print(f"Disease/pathway columns: {list(presence_pivot.columns)}")

    # Rename columns to indicate gene presence
    presence_pivot.columns = [f"{col}_gene" for col in presence_pivot.columns]

    # Get other columns (like Description, Category) for each gene
    # Group by Gene Symbol and take the first non-null value for each column
    other_columns = [col for col in combined_df.columns
                    if col not in ['Gene Symbol', 'Disease_or_Pathway_Association', 'composite_key']]

    gene_info = combined_df.groupby('Gene Symbol')[other_columns].first()

    print(f"Gene info shape: {gene_info.shape}")
    print(f"Additional columns: {list(gene_info.columns)}")

    # Combine presence indicators with gene info
    final_df = pd.concat([gene_info, presence_pivot], axis=1)

    # Validation: Check if final number of rows matches unique Gene Symbols
    final_row_count = len(final_df)

    if final_row_count != unique_genes:
        print(f"\nERROR: Final row count ({final_row_count}) does not match unique Gene Symbols ({unique_genes})")

        # Find which symbols occurred multiple times
        gene_counts = combined_df['Gene Symbol'].value_counts()
        multi_occurrence_genes = gene_counts[gene_counts > 1]

        print("Gene Symbols that occurred multiple times:")
        for gene, count in multi_occurrence_genes.items():
            print(f"  {gene}: {count} occurrences")
            # Show the conflicting rows
            conflicting_rows = combined_df[combined_df['Gene Symbol'] == gene]
            print("    Conflicting data:")
            for _, row in conflicting_rows.iterrows():
                print(f"      Disease: {row['Disease_or_Pathway_Association']}, " +
                      f"Description: {row.get('Description', 'N/A')}, " +
                      f"Category: {row.get('Category', 'N/A')}")

        print("\nThis indicates that the same Gene Symbol has different Description/Category values.")
        print("You may need to decide how to handle these conflicts.")
        return

    print(f"\nSUCCESS: Final row count ({final_row_count}) matches unique Gene Symbols ({unique_genes})")    # Sort by index (Gene Symbol)
    final_df.sort_index(inplace=True)

    # Save to file
    final_df.to_csv(output_file, sep='\t')
    print(f"\nSuccessfully created combined file: {output_file}")
    print(f"Total number of unique genes: {len(final_df)}")

if __name__ == "__main__":
    main()
