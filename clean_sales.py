import pandas as pd
import numpy as np

df = pd.read_csv('messy_retail_sales.csv')
print(f"BEFORE: {df.shape}")
print(f"Duplicates: {df.duplicated(subset=['ORDER_ID']).sum()}")

# Cleans column names
df.columns = df.columns.str.strip().str.upper().str.replace(' ', '_')

df = df.rename(columns={'SALESPERSON': 'SALES_PERSON'})

# Remove duplicate Order_ID - keep first
df = df.drop_duplicates(subset=['ORDER_ID'], keep='first')

# Fix Branch - strip spaces, make Title Case
df['BRANCH'] = df['BRANCH'].str.strip().str.title()

# Fix Product - strip, Title Case, 50KG -> 50kg
df['PRODUCT'] = df['PRODUCT'].str.strip().str.title()
df['PRODUCT'] = df['PRODUCT'].replace({'Rice 50Kg': 'Rice 50kg', 'Groundnut Oil 5l': 'Groundnut Oil 5L'})

# Fix Payment_Method
df['PAYMENT_METHOD'] = df['PAYMENT_METHOD'].str.strip().str.title()
df['PAYMENT_METHOD'] = df['PAYMENT_METHOD'].fillna('Unknown')

# Fix Dates - pandas will figure out the mixed formats
df['DATE'] = pd.to_datetime(df['DATE'], format='mixed', dayfirst=True, errors='coerce')
df['MONTH'] = df['DATE'].dt.to_period('M').astype(str)

# Fill missing Salesperson and strip spaces + title
df['SALES_PERSON'] = df['SALES_PERSON'].fillna('Unassigned')
df['SALES_PERSON'] = df['SALES_PERSON'].str.strip().str.title()

# Fix wrong prices
price_map = {
    'Rice 50kg': 85000,
    'Peak Milk': 22000,
    'Indomie Carton': 18500,
    'Groundnut Oil 5L': 22000,
    'Bournvita': 12500
  }

# Overwrites Unit_Price with the correct price for that product
df['UNIT_PRICE'] = df['PRODUCT'].map(price_map)

# Coverts str -> numeric for calculations
df['QUANTITY'] = pd.to_numeric(df['QUANTITY'], errors='coerce')
df['UNIT_PRICE'] = pd.to_numeric(df['UNIT_PRICE'], errors='coerce')
# Fix Quantity and Price - fill missing with median
df['QUANTITY'] = df['QUANTITY'].fillna(df['QUANTITY'].median())
df['UNIT_PRICE'] = df['UNIT_PRICE'].fillna(df['UNIT_PRICE'].median())

# Create Revenue - A new column for analysis
df['REVENUE'] = df['QUANTITY'] * df['UNIT_PRICE']

# Save clean file
df.to_csv('cleaned_retail_sales.csv', index=False)

print(f"AFTER: {df.shape}")
print("\nBRANCH counts:")
print(df['BRANCH'].value_counts())
print("\nPRODUCT counts:")
print(df['PRODUCT'].value_counts())
print("\nPAYMENT counts:")
print(df['PAYMENT_METHOD'].value_counts())
print(f"\nTotal Revenue: ₦{df['REVENUE'].sum():,.0f}")