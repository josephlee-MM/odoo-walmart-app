import streamlit as st
import os
import pandas as pd
from logic.customer_import import generate_customer_import
from logic.sales_order_import import generate_sales_order_import
from logic.split_pdfs import split_and_rename_pdfs

# Session state to persist output dir and file status
if 'files_ready' not in st.session_state:
    st.session_state['files_ready'] = False
if 'output_dir' not in st.session_state:
    st.session_state['output_dir'] = None

st.title("Walmart PO → Odoo Import Files")

# File uploaders
po_path = st.file_uploader("Upload Walmart PO Excel file", type=["xlsx"])
pdf_path = st.file_uploader("Upload Combined Packing Slips PDF", type=["pdf"])

# Set output path
output_dir = st.session_state['output_dir'] if st.session_state['output_dir'] else "dist/output"
os.makedirs(output_dir, exist_ok=True)

customer_output = os.path.join(output_dir, "customers.xlsx")
sales_order_output = os.path.join(output_dir, "sales_orders.xlsx")

if st.button("Run Automation"):
    if po_path and pdf_path:
        st.session_state['files_ready'] = True
        st.session_state['output_dir'] = output_dir

        # ✅ FIX: Load PO file into a DataFrame
        po_data = pd.read_excel(po_path)

        # Process all files
        generate_sales_order_import(po_data, sales_order_output)
        generate_customer_import(po_data, customer_output)
        split_and_rename_pdfs(pdf_path, output_dir, po_data)

        st.success("✅ Files generated successfully.")
    else:
        st.warning("Please upload both the PO Excel file and the PDF packing slip.")

# Show download buttons
if st.session_state['files_ready']:
    st.subheader("📥 Download Files")

    if os.path.exists(sales_order_output):
        with open(sales_order_output, "rb") as f:
            st.download_button("Download Sales Orders Excel", f, file_name="sales_orders.xlsx")

    if os.path.exists(customer_output):
        with open(customer_output, "rb") as f:
            st.download_button("Download Customer Import Excel", f, file_name="customers.xlsx")

    # Show all generated PDFs
    st.subheader("📦 Packing Slips")
    for fname in os.listdir(output_dir):
        if fname.lower().endswith(".pdf"):
            with open(os.path.join(output_dir, fname), "rb") as f:
                st.download_button(f"Download {fname}", f, file_name=fname)

