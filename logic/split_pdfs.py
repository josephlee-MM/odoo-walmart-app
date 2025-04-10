from PyPDF2 import PdfReader, PdfWriter
import pandas as pd
import os

def split_and_rename_pdfs(pdf_path, sales_order_file, output_dir):
    reader = PdfReader(pdf_path)
    so_df = pd.read_excel(sales_order_file)
    po_numbers = so_df["PO#"].dropna().unique().tolist()
    for i, po in enumerate(po_numbers):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        with open(os.path.join(output_dir, f"{po}.pdf"), "wb") as f:
            writer.write(f)
