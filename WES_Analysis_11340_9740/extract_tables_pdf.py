"""
Extract tables from a PDF and save each table as a TSV file.

Requirements:
- Python 3.x
- camelot-py (install with: uv add camelot-py)

Extraction Flavors:
- The script extracts tables using three modes:
    1. 'stream' flavor (Camelot's stream algorithm)
    2. 'lattice' flavor (Camelot's lattice algorithm)
    3. No flavor (Camelot's default settings)
- Results for each mode are saved in subfolders named 'stream', 'lattice', and 'NA' inside the output folder.

Encoding Note:
- TSV output uses UTF-8 encoding by default to preserve special characters (e.g., ×, −, non-breaking spaces).
- If you encounter encoding issues, you may need to update the encoding argument in the script (see the 'encoding' parameter in table.to_csv).

Usage:
    python extract_tables_pdf.py <input_pdf> <output_folder>

Example (using uv):
    uv run python WES_Analysis_11340_9740/extract_tables_pdf.py local/StutterPaper_NA.pdf references/extracted_tables

This script will extract all tables from the specified PDF and save them as TSV files in the output folder, organized by extraction flavor.
"""

import os
import sys
import camelot

def extract_tables(pdf_path, output_folder):
    # Check if PDF exists
    if not os.path.exists(pdf_path):
        print(f"PDF file '{pdf_path}' not found.")
        return

    # Define flavor options
    flavor_options = ["stream", "lattice", None]
    flavor_names = {"stream": "stream", "lattice": "lattice", None: "NA"}

    for flavor in flavor_options:
        subfolder = os.path.join(output_folder, flavor_names[flavor])
        os.makedirs(subfolder, exist_ok=True)
        print(f"\nExtracting tables with flavor: {flavor_names[flavor]}")
        if flavor:
            tables = camelot.read_pdf(pdf_path, pages='all', flavor=flavor)
        else:
            tables = camelot.read_pdf(pdf_path, pages='all')
        if not tables or tables.n == 0:
            print("No tables found!")
            continue
        print(f"Found {tables.n} table(s).")
        for i, table in enumerate(tables):
            out_tsv = os.path.join(subfolder, f"table_{i+1}.tsv")
            out_xlsx = os.path.join(subfolder, f"table_{i+1}.xlsx")
            df = table.df  # Convert to pandas DataFrame
            df.to_csv(out_tsv, sep='\t', encoding='utf-8', index=False)
            df.to_excel(out_xlsx, index=False)
            print(f"Saved table {i+1} to {out_tsv} and {out_xlsx}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python extract_pdf_tables.py <input_pdf> <output_folder>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    out_folder = sys.argv[2]
    extract_tables(pdf_file, out_folder)