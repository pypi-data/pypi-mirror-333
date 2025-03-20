from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_sensor_id():
    return fake.uuid4()

def generate_air_quality_index():
    return fake.random_int(min=0, max=500)

def generate_temperature_celsius():
    return round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)

def generate_humidity_percent():
    return fake.random_int(min=0, max=100)

def generate_co2_level_ppm():
    return fake.random_int(min=300, max=1000)

def generate_noise_level_db():
    return round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)

def generate_rainfall_mm():
    return round(fake.pyfloat(left_digits=2, right_digits=1, positive=True), 1)

def generate_wind_speed_kph():
    return round(fake.pyfloat(left_digits=2, right_digits=1, positive=True), 1)

def generate_location():
    return fake.city()

def generate_country():
    return fake.country()

def generate_measurement_date():
    return fake.date_this_year()

def generate_measurement_time():
    return fake.time()

def generate_uv_index():
    return fake.random_int(min=0, max=11)

def generate_water_quality_index():
    return fake.random_int(min=0, max=100)

def generate_pm25():
    return round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)

def generate_pm10():
    return round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)

def generate_ozone_level_ppb():
    return fake.random_int(min=10, max=300)

def generate_so2_level_ppb():
    return fake.random_int(min=0, max=200)

def generate_no2_level_ppb():
    return fake.random_int(min=0, max=200)

def generate_pollution_source():
    return fake.random_element(elements=["Industrial", "Traffic", "Natural", "Residential"])

def generate_environmental_data(num_records=100):
    data = [
        {
            "sensor_id": generate_sensor_id(),
            "air_quality_index": generate_air_quality_index(),
            "temperature_celsius": generate_temperature_celsius(),
            "humidity_percent": generate_humidity_percent(),
            "co2_level_ppm": generate_co2_level_ppm(),
            "noise_level_db": generate_noise_level_db(),
            "rainfall_mm": generate_rainfall_mm(),
            "wind_speed_kph": generate_wind_speed_kph(),
            "location": generate_location(),
            "country": generate_country(),
            "measurement_date": generate_measurement_date(),
            "measurement_time": generate_measurement_time(),
            "uv_index": generate_uv_index(),
            "water_quality_index": generate_water_quality_index(),
            "pm25": generate_pm25(),
            "pm10": generate_pm10(),
            "ozone_level_ppb": generate_ozone_level_ppb(),
            "so2_level_ppb": generate_so2_level_ppb(),
            "no2_level_ppb": generate_no2_level_ppb(),
            "pollution_source": generate_pollution_source(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_environmental_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_environmental_data')
# def download_environmental_data():
#     df = generate_environmental_data(500000)
#     file_path = "environmental_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
