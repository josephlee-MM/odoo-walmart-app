import pandas as pd

def generate_sales_order_import(po_path, output_path):
    df = pd.read_excel(po_path, sheet_name="Po Details")
    df["Customer"] = "Walmart Seller Center"
    df["Invoice Address"] = "Walmart Seller Center"
    df["Delivery Address"] = "Walmart Seller Center, " + df["Customer Name"].fillna("")
    df["order_line/product_template_id"] = df["SKU"]
    df["order_line/product_uom_qty"] = df["Qty"]
    df["order_line/price_unit"] = df["Item Cost"]
    df["order_line/product_uom"] = "Each - 1"
    df["order_line/sequence"] = 1
    final_df = df[[
        "Customer", "Invoice Address", "Delivery Address", "PO#", "order_line/sequence",
        "order_line/product_uom_qty", "order_line/price_unit",
        "order_line/product_template_id", "order_line/product_uom"
    ]]
    final_df.to_excel(output_path, index=False)
