from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_shipment_id():
    return fake.uuid4()

def generate_origin():
    return fake.city()

def generate_destination():
    return fake.city()

def generate_departure_date():
    return fake.date_between(start_date='-1y', end_date='today')

def generate_arrival_date():
    return fake.date_between(start_date='today', end_date='+1y')

def generate_transport_mode():
    return fake.random_element(elements=["Air", "Sea", "Road", "Rail"])

def generate_carrier_name():
    return fake.company()

def generate_tracking_number():
    return fake.bothify(text="??-########")

def generate_package_weight():
    return round(fake.pydecimal(left_digits=2, right_digits=2, positive=True), 2)

def generate_package_volume():
    return round(fake.pydecimal(left_digits=3, right_digits=2, positive=True), 2)

def generate_status():
    return fake.random_element(elements=["In Transit", "Delivered", "Pending", "Cancelled"])

def generate_customer_name():
    return fake.name()

def generate_contact_number():
    return fake.phone_number()

def generate_shipping_cost():
    return round(fake.pydecimal(left_digits=4, right_digits=2, positive=True), 2)

def generate_priority_level():
    return fake.random_element(elements=["Standard", "Express", "Overnight"])

def generate_vehicle_id():
    return fake.bothify(text="???-####")

def generate_driver_name():
    return fake.name()

def generate_delivery_address():
    return fake.address()

def generate_customs_clearance_status():
    return fake.random_element(elements=["Cleared", "Pending", "Held"])

def generate_insurance_coverage():
    return round(fake.pydecimal(left_digits=5, right_digits=2, positive=True), 2)

def generate_logistics_data(num_records=100):
    data = [
        {
            "shipment_id": generate_shipment_id(),
            "origin": generate_origin(),
            "destination": generate_destination(),
            "departure_date": generate_departure_date(),
            "arrival_date": generate_arrival_date(),
            "transport_mode": generate_transport_mode(),
            "carrier_name": generate_carrier_name(),
            "tracking_number": generate_tracking_number(),
            "package_weight": generate_package_weight(),
            "package_volume": generate_package_volume(),
            "status": generate_status(),
            "customer_name": generate_customer_name(),
            "contact_number": generate_contact_number(),
            "shipping_cost": generate_shipping_cost(),
            "priority_level": generate_priority_level(),
            "vehicle_id": generate_vehicle_id(),
            "driver_name": generate_driver_name(),
            "delivery_address": generate_delivery_address(),
            "customs_clearance_status": generate_customs_clearance_status(),
            "insurance_coverage": generate_insurance_coverage(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_logistics_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_logistics_data')
# def download_logistics_data():
#     df = generate_logistics_data(500000)
#     file_path = "logistics_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
