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

    # Track line sequences per PO#
    grouped = df.groupby("PO#")
    all_rows = []
    for po, group in grouped:
        for i, (_, row) in enumerate(group.iterrows()):
            sequence = i + 1
            all_rows.append([
                row["Customer"] if sequence == 1 else "",
                row["Invoice Address"] if sequence == 1 else "",
                row["Delivery Address"] if sequence == 1 else "",
                row["PO#"] if sequence == 1 else "",
                sequence,
                row["order_line/product_uom_qty"],
                row["order_line/price_unit"],
                row["order_line/product_template_id"],
                row["order_line/product_uom"]
            ])

    final_df = pd.DataFrame(all_rows, columns=[
        "Customer", "Invoice Address", "Delivery Address", "PO#", "order_line/sequence",
        "order_line/product_uom_qty", "order_line/price_unit",
        "order_line/product_template_id", "order_line/product_uom"
    ])
    final_df.to_excel(output_path, index=False)
