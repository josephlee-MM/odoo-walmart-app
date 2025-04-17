from PyPDF2 import PdfReader, PdfWriter
import re
import os

def split_and_rename_pdfs(pdf_path, sales_order_file, output_dir):
    reader = PdfReader(pdf_path)

    for i, page in enumerate(reader.pages):
        text = page.extract_text()

        # Try to extract Ship To name
        name_match = re.search(r'Ship to\s*\n(.+)', text, re.IGNORECASE)
        if name_match:
            name = name_match.group(1).strip()
            filename = re.sub(r'[^a-zA-Z0-9]+', '_', name).strip("_")
        else:
            filename = f"Page_{i+1}"

        writer = PdfWriter()
        writer.add_page(page)

        output_path = os.path.join(output_dir, f"{filename}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)
