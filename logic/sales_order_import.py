def generate_sales_order_import(po_data, output_path):
    import pandas as pd
    import re

    orders = []

    for _, row in po_data.iterrows():
        order_id = row['PO#']
        customer = row['Customer']
        delivery_name = row['Delivery Address']
        delivery_phone = ""  # Not provided

        # Parse shipping address
        full_address = str(row['Customer Shipping Address'])
        match = re.search(r'^(.*?),\s*(.*?),\s*([A-Z]{2})\s+(\d{5})$', full_address)
        if match:
            delivery_street = match.group(1).strip()
            delivery_city = match.group(2).strip()
            delivery_state = match.group(3).strip()
            delivery_zip = match.group(4).strip()
        else:
            delivery_street = delivery_city = delivery_state = delivery_zip = ''

        delivery_country = "United States"
        sku = row['order_line/product_template_id']
        qty = row['order_line/product_uom_qty']
        price = row['order_line/price_unit']

        existing_order = next((o for o in orders if o['order_id'] == order_id), None)
        if existing_order:
            existing_order['items'].append({'sku': sku, 'qty': qty, 'price': price})
        else:
            orders.append({
                'order_id': order_id,
                'customer': customer,
                'delivery_name': delivery_name,
                'delivery_phone': delivery_phone,
                'delivery_street': delivery_street,
                'delivery_city': delivery_city,
                'delivery_state': delivery_state,
                'delivery_zip': delivery_zip,
                'delivery_country': delivery_country,
                'items': [{'sku': sku, 'qty': qty, 'price': price}]
            })

    rows = []
    for order in orders:
        first_line = True
        for item in order['items']:
            row = [
                order['order_id'] if first_line else '',
                order['customer'] if first_line else '',
                order['delivery_name'] if first_line else '',
                order['delivery_phone'] if first_line else '',
                order['delivery_street'] if first_line else '',
                order['delivery_city'] if first_line else '',
                order['delivery_state'] if first_line else '',
                order['delivery_zip'] if first_line else '',
                order['delivery_country'] if first_line else '',
                item['sku'],
                item['qty'],
                item['price']
            ]
            rows.append(row)
            first_line = False

    df = pd.DataFrame(rows, columns=[
        'Order ID', 'Customer', 'Delivery Name', 'Delivery Phone',
        'Delivery Street', 'Delivery City', 'Delivery State',
        'Delivery Zip', 'Delivery Country', 'Item SKU', 'Quantity', 'Price'
    ])
    df.to_excel(output_path, index=False)

