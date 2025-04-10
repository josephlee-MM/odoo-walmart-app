import streamlit as st
import pandas as pd
import os
import tempfile

from logic.customer_import import generate_customer_import
from logic.sales_order_import import generate_sales_order_import
from logic.split_pdfs import split_and_rename_pdfs

st.set_page_config(page_title="Walmart → Odoo Import Tool", layout="centered")

st.title("🛒 Walmart → Odoo Import Tool")
st.markdown("Upload your **Walmart PO (.xlsx)** and **Packing Slips (.pdf)** to generate import-ready files for Odoo v18.")

# File uploads
po_file = st.file_uploader("📤 Upload Walmart PO Excel File", type=["xlsx"])
pdf_file = st.file_uploader("📤 Upload Packing Slip PDF", type=["pdf"])
output_folder = tempfile.mkdtemp()

# Run processing
if st.button("🚀 Run Automation"):

    if not po_file or not pdf_file:
        st.warning("⚠️ Please upload both a PO Excel and PDF file.")
    else:
        with st.spinner("Processing files..."):

            po_path = os.path.join(output_folder, "walmart_po.xlsx")
            pdf_path = os.path.join(output_folder, "packing_slips.pdf")

            with open(po_path, "wb") as f:
                f.write(po_file.read())
            with open(pdf_path, "wb") as f:
                f.write(pdf_file.read())

            # Output file paths
            customer_output = os.path.join(output_folder, "customers.xlsx")
            sales_order_output = os.path.join(output_folder, "sales_orders.xlsx")

            # Run your existing logic
            generate_customer_import(po_path, customer_output)
            generate_sales_order_import(po_path, sales_order_output)
            split_and_rename_pdfs(pdf_path, sales_order_output, output_folder)

            st.success("✅ Done! Download your files below:")

            with open(customer_output, "rb") as f:
                st.download_button("📥 Download Customers.xlsx", f, file_name="customers.xlsx")

            with open(sales_order_output, "rb") as f:
                st.download_button("📥 Download Sales Orders.xlsx", f, file_name="sales_orders.xlsx")

            # List all generated PDFs
            st.markdown("### 📎 Split Packing Slips:")
            for file in os.listdir(output_folder):
                if file.endswith(".pdf") and file != "packing_slips.pdf":
                    with open(os.path.join(output_folder, file), "rb") as f:
                        st.download_button(f"📄 {file}", f, file_name=file)
