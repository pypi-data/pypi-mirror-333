from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_sale_id():
    return fake.uuid4()

def generate_product_name():
    return fake.word().title()

def generate_customer_id():
    return fake.uuid4()

def generate_sale_date():
    return fake.date_time_this_year()

def generate_quantity():
    return fake.random_int(min=1, max=100)

def generate_unit_price():
    return round(fake.pydecimal(left_digits=4, right_digits=2, positive=True), 2)

def generate_total_amount(quantity, unit_price):
    return round(quantity * unit_price, 2)

def generate_discount():
    return round(fake.pydecimal(left_digits=2, right_digits=2, positive=True), 2)

def generate_payment_method():
    return fake.random_element(elements=["Credit Card", "Debit Card", "Cash", "Bank Transfer"])

def generate_salesperson():
    return fake.name()

def generate_region():
    return fake.state()

def generate_country():
    return fake.country()

def generate_invoice_number():
    return fake.bothify("INV###-###")

def generate_customer_type():
    return fake.random_element(elements=["Retail", "Wholesale", "Online"])

def generate_return_status():
    return fake.random_element(elements=["No Return", "Partial Return", "Full Return"])

def generate_shipping_method():
    return fake.random_element(elements=["Standard", "Express", "Overnight"])

def generate_delivery_status():
    return fake.random_element(elements=["Delivered", "Pending", "Cancelled"])

def generate_product_category():
    return fake.random_element(elements=["Electronics", "Clothing", "Home Appliances", "Books", "Beauty"])

def generate_loyalty_points():
    return fake.random_int(min=0, max=1000)

def generate_channel():
    return fake.random_element(elements=["Online", "In-Store", "Phone"])

def generate_sales_data(num_records=100):
    data = []
    for _ in range(num_records):
        quantity = generate_quantity()
        unit_price = generate_unit_price()
        data.append({
            "sale_id": generate_sale_id(),
            "product_name": generate_product_name(),
            "customer_id": generate_customer_id(),
            "sale_date": generate_sale_date(),
            "quantity": quantity,
            "unit_price": unit_price,
            "total_amount": generate_total_amount(quantity, unit_price),
            "discount": generate_discount(),
            "payment_method": generate_payment_method(),
            "salesperson": generate_salesperson(),
            "region": generate_region(),
            "country": generate_country(),
            "invoice_number": generate_invoice_number(),
            "customer_type": generate_customer_type(),
            "return_status": generate_return_status(),
            "shipping_method": generate_shipping_method(),
            "delivery_status": generate_delivery_status(),
            "product_category": generate_product_category(),
            "loyalty_points": generate_loyalty_points(),
            "channel": generate_channel(),
        })

    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_sales_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_sales_data')
# def download_sales_data():
#     df = generate_sales_data(500000)
#     file_path = "sales_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
