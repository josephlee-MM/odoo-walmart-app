from PyPDF2 import PdfReader, PdfWriter
import pandas as pd
import os

def split_and_rename_pdfs(pdf_path, sales_order_file, output_dir):
    # Load the PDF
    reader = PdfReader(pdf_path)
    
    # Load the Excel with PO#s
    so_df = pd.read_excel(sales_order_file)

    # Get unique PO numbers in order
    po_numbers = so_df["PO#"].dropna().unique().tolist()

    # Loop through pages and PO#s
    for i, po in enumerate(po_numbers):
        if i >= len(reader.pages):
            print(f"Warning: Not enough PDF pages for PO {po}")
            break

        writer = PdfWriter()
        writer.add_page(reader.pages[i])

        # Write PDF to output folder
        output_path = os.path.join(output_dir, f"{po}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)
