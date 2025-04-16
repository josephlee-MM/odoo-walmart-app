import pandas as pd
import re

def parse_address(addr):
    try:
        parts = addr.split(',')
        street = parts[1].strip() if len(parts) > 1 else ''
        city = parts[2].strip() if len(parts) > 2 else ''
        state_zip = parts[3].strip() if len(parts) > 3 else ''
        match = re.search(r'([A-Z]{2})\s+(\d{5})', state_zip)
        state = match.group(1) if match else ''
        zip_code = match.group(2) if match else ''
        return pd.Series([street, city, state, zip_code])
    except:
        return pd.Series(['', '', '', ''])

def us_state_full(abbrev):
    mapping = {
        "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
        "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
        "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
        "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
        "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
        "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
        "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
        "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
        "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
        "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"
    }
    return mapping.get(abbrev, abbrev) + " (US)"

def generate_customer_import(po_path, output_path):
    df = pd.read_excel(po_path, sheet_name="Po Details")
    df[['street', 'city', 'state_code', 'zip']] = df['Customer Shipping Address'].apply(parse_address)
    df['state_id'] = df['state_code'].apply(us_state_full).apply(lambda x: f"{x} (US)")
    df['is_company'] = 0
    df['company_name'] = "Walmart Seller Center"
    df['country_id'] = 'US'
    df['name'] = df['Customer Name']
    df['phone'] = df['Customer Phone Number']
    df['street2'] = df['mobile'] = df['email'] = df['vat'] = ''
    df['bank_ids/bank'] = df['bank_ids/acc_number'] = ''
    odoo_customers = df[[
        'name', 'is_company', 'company_name', 'country_id', 'state_id', 'zip',
        'city', 'street', 'street2', 'phone', 'mobile', 'email', 'vat',
        'bank_ids/bank', 'bank_ids/acc_number'
    ]].drop_duplicates().fillna("")
    odoo_customers.to_excel(output_path, index=False)
