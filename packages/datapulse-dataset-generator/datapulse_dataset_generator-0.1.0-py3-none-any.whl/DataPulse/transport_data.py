from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_transport_id():
    return fake.uuid4()

def generate_vehicle_type():
    return fake.random_element(elements=["Car", "Truck", "Bus", "Motorcycle", "Bicycle", "Train"])

def generate_route_number():
    return fake.bothify(text="R-###")

def generate_departure_city():
    return fake.city()

def generate_arrival_city():
    return fake.city()

def generate_departure_time():
    return fake.date_time_this_year()

def generate_arrival_time():
    return fake.date_time_this_year()

def generate_ticket_price():
    return round(fake.pydecimal(left_digits=3, right_digits=2, positive=True), 2)

def generate_driver_name():
    return fake.name()

def generate_passenger_count():
    return fake.random_int(min=1, max=200)

def generate_transport_status():
    return fake.random_element(elements=["On Time", "Delayed", "Cancelled"])

def generate_fuel_type():
    return fake.random_element(elements=["Petrol", "Diesel", "Electric", "Hybrid"])

def generate_license_plate():
    return fake.license_plate()

def generate_transport_company():
    return fake.company()

def generate_cargo_type():
    return fake.random_element(elements=["General", "Perishable", "Hazardous", "Bulk", "Livestock"])

def generate_vehicle_capacity():
    return fake.random_int(min=1000, max=50000)

def generate_trip_distance():
    return round(fake.pyfloat(left_digits=3, right_digits=1, positive=True), 1)

def generate_ticket_id():
    return fake.bothify(text="TICKET-####")

def generate_logistics_partner():
    return fake.company()

def generate_inspection_status():
    return fake.random_element(elements=["Passed", "Failed", "Pending"])

def generate_transportation_data(num_records=100):
    data = [
        {
            "transport_id": generate_transport_id(),
            "vehicle_type": generate_vehicle_type(),
            "route_number": generate_route_number(),
            "departure_city": generate_departure_city(),
            "arrival_city": generate_arrival_city(),
            "departure_time": generate_departure_time(),
            "arrival_time": generate_arrival_time(),
            "ticket_price": generate_ticket_price(),
            "driver_name": generate_driver_name(),
            "passenger_count": generate_passenger_count(),
            "transport_status": generate_transport_status(),
            "fuel_type": generate_fuel_type(),
            "license_plate": generate_license_plate(),
            "transport_company": generate_transport_company(),
            "cargo_type": generate_cargo_type(),
            "vehicle_capacity": generate_vehicle_capacity(),
            "trip_distance": generate_trip_distance(),
            "ticket_id": generate_ticket_id(),
            "logistics_partner": generate_logistics_partner(),
            "inspection_status": generate_inspection_status(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_transportation_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_transportation_data')
# def download_transportation_data():
#     df = generate_transportation_data(500000)
#     file_path = "transportation_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)