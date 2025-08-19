import pandas as pd
import os
import sys
import urllib.request
from pyliftover import LiftOver

# Path to input Excel file and output Excel file
input_excel = 'references/stuttering_paper_GWAS/stuttering_paper_combined_only.xlsx'
input_excel_2024 = 'references/2024_stuttering_associated/2024_stuttering_associated.xlsx'
out_dir = 'references/stuttering_paper_GWAS'
os.makedirs(out_dir, exist_ok=True)
output_excel = os.path.join(out_dir, 'stuttering_paper_combined_only_reformatted.xlsx')
output_tsv = os.path.join(out_dir, 'stuttering_paper_combined_reformatted_for_search.tsv')
combined_output_xlsx = os.path.join(out_dir, 'paper_and_2024_combined_reformatted_for_search.xlsx')

# Path to chain file for liftover
chain_file = os.path.join(out_dir, 'hg19ToHg38.over.chain.gz')
chain_url = 'https://hgdownload.cse.ucsc.edu/goldenpath/hg19/liftOver/hg19ToHg38.over.chain.gz'

# Download chain file if it doesn't exist
if not os.path.exists(chain_file):
    print(f"Chain file not found. Downloading from UCSC...")
    print(f"URL: {chain_url}")
    try:
        urllib.request.urlretrieve(chain_url, chain_file)
        print(f"Downloaded chain file to: {chain_file}")
    except Exception as e:
        print(f"Error downloading chain file: {e}")
        sys.exit(1)
else:
    print(f"Using existing chain file: {chain_file}")

print(f"Using chain file: {chain_file}")

# Read the Excel file
print(f"Reading input Excel file: {input_excel}")
try:
    df = pd.read_excel(input_excel)
    print(f"Loaded {len(df)} rows from {input_excel}")
except Exception as e:
    print(f"Error reading {input_excel}: {e}")
    sys.exit(1)

# Initialize pyliftover
print("Initializing pyliftover...")
lo = LiftOver(chain_file)

# Perform liftover for each row
def liftover_row(row):
    chrom = str(row['Chr'])
    pos = int(str(row['pos_b37']).replace(',', ''))
    print(f"Liftover: chr{chrom}:{pos}", end=' -> ')
    result = lo.convert_coordinate(f'chr{chrom}', pos - 1)  # pyliftover is 0-based
    if result:
        new_chrom = result[0][0].replace('chr', '')
        new_pos = int(result[0][1]) + 1  # Convert back to 1-based
        print(f"chr{new_chrom}:{new_pos}")
        return pd.Series([new_chrom, new_pos])
    else:
        print("No mapping found")
        return pd.Series([None, None])

# Apply liftover to DataFrame
print("Applying liftover to all rows...")
df[['Chr_b38', 'pos_b38']] = df.apply(liftover_row, axis=1)

# Add formatted coordinate columns
print("Adding formatted coordinate columns...")
df['hg19'] = 'chr' + df['Chr'].astype(str) + ':' + df['pos_b37'].astype(str).str.replace(',', '')
df['hg38'] = df.apply(lambda row: f"chr{row['Chr_b38']}:{row['pos_b38']}" if pd.notna(row['Chr_b38']) and pd.notna(row['pos_b38']) else None, axis=1)

# Clean up rsID column if present
def clean_rsid(val):
    if not isinstance(val, str):
        return None
    if not val.startswith('rs'):
        return None
    # Keep only 'rs' followed by digits
    import re
    m = re.match(r'(rs\d+)', val)
    if m:
        return m.group(1)
    return None

if 'rsID' in df.columns:
    print("Cleaning rsID column...")
    # Keep original rsID column as rsID_paper
    df['rsID_paper'] = df['rsID']
    df['rsID'] = df['rsID'].apply(clean_rsid)

# Rename 'Functional gene...' column to 'Symbol', remove NA and whitespace
func_gene_col = None
for col in df.columns:
    if str(col).startswith('Functional gene'):
        func_gene_col = col
        break
if func_gene_col:
    print(f"Renaming column '{func_gene_col}' to 'Symbol' and cleaning values...")
    df = df.rename(columns={func_gene_col: 'Symbol'})
    # Remove rows where Symbol is NA or empty after stripping whitespace
    df['Symbol'] = df['Symbol'].astype(str).str.strip()
    before = len(df)
    df = df[df['Symbol'].notna() & (df['Symbol'] != '') & (df['Symbol'].str.lower() != 'na')]
    after = len(df)
    print(f"Removed {before - after} rows with NA or empty Symbol values.")

# Save to Excel
print(f"Saving reformatted file to {output_excel}")
try:
    df.to_excel(output_excel, index=False)
    print(f"Reformatted file saved as {output_excel}")
except Exception as e:
    print(f"Error saving {output_excel}: {e}")

# Save to TSV
print(f"Saving reformatted file to {output_tsv}")
try:
    # Keep only the new/reformatted columns for TSV
    columns_to_save = ['Chr_b38', 'pos_b38', 'hg19', 'hg38', 'Symbol']
    if 'rsID' in df.columns:
        columns_to_save.extend(['rsID', 'rsID_paper'])

    # Only include columns that actually exist in the dataframe
    existing_columns = [col for col in columns_to_save if col in df.columns]
    df_tsv = df[existing_columns]

    # Add index column
    df_tsv.reset_index(drop=True, inplace=True)
    df_tsv.insert(0, 'index', df_tsv.index + 1)

    df_tsv.to_csv(output_tsv, sep='\t', index=False)
    print(f"Reformatted file saved as {output_tsv} with columns: {['index'] + existing_columns}")
except Exception as e:
    print(f"Error saving {output_tsv}: {e}")

# Read the 2024 Excel file and append to df
print(f"Reading additional Excel file: {input_excel_2024}")
try:
    df_2024 = pd.read_excel(input_excel_2024)
    print(f"Loaded {len(df_2024)} rows from {input_excel_2024}")
    df = pd.concat([df, df_2024], ignore_index=True)
    print(f"Combined DataFrame now has {len(df)} rows")
except Exception as e:
    print(f"Error reading {input_excel_2024}: {e}")
    sys.exit(1)

# Save the combined DataFrame to Excel
print(f"Saving combined DataFrame to {combined_output_xlsx}")
try:
    df.to_excel(combined_output_xlsx, index=False)
    print(f"Combined DataFrame saved as {combined_output_xlsx}")
except Exception as e:
    print(f"Error saving {combined_output_xlsx}: {e}")
