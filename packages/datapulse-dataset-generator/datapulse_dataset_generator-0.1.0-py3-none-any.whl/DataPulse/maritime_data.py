from faker import Faker
import pandas as pd
from flask import Flask, send_file
import io

fake = Faker()
app = Flask(__name__)

def generate_ship_id():
    return fake.uuid4()

def generate_ship_name():
    return fake.company()

def generate_departure_port():
    return fake.city()

def generate_arrival_port():
    return fake.city()

def generate_departure_date():
    return fake.date_this_year()

def generate_arrival_date():
    return fake.date_this_year()

def generate_cargo_type():
    return fake.random_element(elements=["Containers", "Oil", "Gas", "Automobiles", "Electronics", "Food Products"])

def generate_ship_type():
    return fake.random_element(elements=["Cargo", "Tanker", "Cruise", "Fishing", "Naval"])

def generate_weight():
    return round(fake.pydecimal(left_digits=5, right_digits=2, positive=True), 2)

def generate_crew_size():
    return fake.random_int(min=10, max=100)

def generate_vessel_flag():
    return fake.country_code()

def generate_shipping_company():
    return fake.company()

def generate_speed_knots():
    return fake.random_int(min=10, max=40)

def generate_navigation_status():
    return fake.random_element(elements=["Underway", "Anchored", "Moored", "Docked"])

def generate_incident_reported():
    return fake.boolean()

def generate_ship_registration_number():
    return fake.bothify("SHIP-###-????")

def generate_latitude():
    return round(fake.latitude(), 6)

def generate_longitude():
    return round(fake.longitude(), 6)

def generate_maritime_data(num_records=100):
    data = [{
        "ship_id": generate_ship_id(),
        "ship_name": generate_ship_name(),
        "departure_port": generate_departure_port(),
        "arrival_port": generate_arrival_port(),
        "departure_date": generate_departure_date(),
        "arrival_date": generate_arrival_date(),
        "cargo_type": generate_cargo_type(),
        "ship_type": generate_ship_type(),
        "weight_tons": generate_weight(),
        "crew_size": generate_crew_size(),
        "vessel_flag": generate_vessel_flag(),
        "shipping_company": generate_shipping_company(),
        "speed_knots": generate_speed_knots(),
        "navigation_status": generate_navigation_status(),
        "incident_reported": generate_incident_reported(),
        "ship_registration_number": generate_ship_registration_number(),
        "latitude": generate_latitude(),
        "longitude": generate_longitude()
    } for _ in range(num_records)]

    return pd.DataFrame(data)

# @app.route('/download_maritime_data')
# def download_maritime_data():
#     df = generate_maritime_data(num_records=500000)
#     output = io.BytesIO()
#     df.to_csv(output, index=False)
#     output.seek(0)

#     return send_file(output, mimetype='text/csv', as_attachment=True, download_name='maritime_data.csv')

# if __name__ == '__main__':
#     sample_df = generate_maritime_data(10)
#     print(sample_df.head(10))
#     app.run(debug=True)
