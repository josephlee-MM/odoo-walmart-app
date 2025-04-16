import pandas as pd


def generate_sales_order_import(po_data, output_path):
    import pandas as pd

    orders = []

    for _, row in po_data.iterrows():
        order_id = row['PO Number']
        customer = row['Customer Name']
        delivery_name = row['Customer Name']
        delivery_phone = row['Customer Phone']
        delivery_street = row['Street']
        delivery_city = row['City']
        delivery_state = row['State']
        delivery_zip = str(row['Zip']).zfill(5)
        delivery_country = "United States"
        sku = row['Item SKU']
        qty = row['Quantity']
        price = row['Item Cost']

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
