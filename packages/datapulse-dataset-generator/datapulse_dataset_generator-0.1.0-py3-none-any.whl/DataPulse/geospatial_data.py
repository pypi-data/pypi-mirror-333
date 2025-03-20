from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_location_id():
    return fake.uuid4()

def generate_latitude():
    return fake.latitude()

def generate_longitude():
    return fake.longitude()

def generate_altitude():
    return round(fake.pyfloat(left_digits=3, right_digits=2, positive=True, min_value=0, max_value=5000), 2)

def generate_country():
    return fake.country()

def generate_city():
    return fake.city()

def generate_zip_code():
    return fake.zipcode()

def generate_region():
    return fake.state()

def generate_continent():
    return fake.random_element(elements=["Africa", "Antarctica", "Asia", "Europe", "North America", "Oceania", "South America"])

def generate_geohash():
    return fake.bothify(text='?????-#####')

def generate_address():
    return fake.address()

def generate_landmark():
    return fake.street_name()

def generate_population_density():
    return fake.random_int(min=1, max=10000)

def generate_urban_rural():
    return fake.random_element(elements=["Urban", "Rural", "Suburban"])

def generate_time_zone():
    return fake.timezone()

def generate_area_size():
    return round(fake.pyfloat(left_digits=4, right_digits=2, positive=True, min_value=1, max_value=10000), 2)

def generate_climate_zone():
    return fake.random_element(elements=["Tropical", "Dry", "Temperate", "Continental", "Polar"])

def generate_transport_access():
    return fake.random_element(elements=["Highway", "Railway", "Airport", "Seaport", "None"])

def generate_environment_type():
    return fake.random_element(elements=["Coastal", "Mountainous", "Plains", "Desert", "Forest"])

def generate_geospatial_data(num_records=100):
    data = []
    for _ in range(num_records):
        data.append({
            "location_id": generate_location_id(),
            "latitude": generate_latitude(),
            "longitude": generate_longitude(),
            "altitude": generate_altitude(),
            "country": generate_country(),
            "city": generate_city(),
            "zip_code": generate_zip_code(),
            "region": generate_region(),
            "continent": generate_continent(),
            "geohash": generate_geohash(),
            "address": generate_address(),
            "landmark": generate_landmark(),
            "population_density": generate_population_density(),
            "urban_rural": generate_urban_rural(),
            "time_zone": generate_time_zone(),
            "area_size": generate_area_size(),
            "climate_zone": generate_climate_zone(),
            "transport_access": generate_transport_access(),
            "environment_type": generate_environment_type(),
        })

    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_geospatial_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_geospatial_data')
# def download_geospatial_data():
#     df = generate_geospatial_data(500000)
#     file_path = "geospatial_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)