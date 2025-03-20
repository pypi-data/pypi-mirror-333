from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_device_id():
    return fake.uuid4()

def generate_device_type():
    return fake.random_element(elements=["Sensor", "Smart Light", "Smart Thermostat", "Smart Camera", "Wearable", "Smart Plug"])

def generate_temperature():
    return round(fake.pyfloat(left_digits=2, right_digits=2, positive=True, min_value=-30, max_value=50), 2)

def generate_humidity():
    return round(fake.pyfloat(left_digits=2, right_digits=2, positive=True, min_value=0, max_value=100), 2)

def generate_battery_level():
    return fake.random_int(min=0, max=100)

def generate_signal_strength():
    return fake.random_int(min=-100, max=-30)

def generate_firmware_version():
    return fake.bothify(text="v?.##")

def generate_location():
    return fake.city()

def generate_connection_status():
    return fake.random_element(elements=["Online", "Offline", "Error"])

def generate_last_active():
    return fake.date_time_this_year()

def generate_data_rate():
    return round(fake.pyfloat(left_digits=1, right_digits=4, positive=True), 4)

def generate_ip_address():
    return fake.ipv4()

def generate_mac_address():
    return fake.mac_address()

def generate_power_consumption():
    return round(fake.pyfloat(left_digits=2, right_digits=3, positive=True), 3)

def generate_alert_status():
    return fake.random_element(elements=["Normal", "Warning", "Critical"])

def generate_uptime_hours():
    return fake.random_int(min=0, max=8760)

def generate_device_owner():
    return fake.name()

def generate_network_type():
    return fake.random_element(elements=["WiFi", "Ethernet", "Cellular"])

def generate_data_packet_size():
    return fake.random_int(min=64, max=1500)

def generate_device_model():
    return fake.bothify(text="Model-###")

def generate_iot_data(num_records=100):
    data = []
    for _ in range(num_records):
        data.append({
            "device_id": generate_device_id(),
            "device_type": generate_device_type(),
            "temperature": generate_temperature(),
            "humidity": generate_humidity(),
            "battery_level": generate_battery_level(),
            "signal_strength": generate_signal_strength(),
            "firmware_version": generate_firmware_version(),
            "location": generate_location(),
            "connection_status": generate_connection_status(),
            "last_active": generate_last_active(),
            "data_rate": generate_data_rate(),
            "ip_address": generate_ip_address(),
            "mac_address": generate_mac_address(),
            "power_consumption": generate_power_consumption(),
            "alert_status": generate_alert_status(),
            "uptime_hours": generate_uptime_hours(),
            "device_owner": generate_device_owner(),
            "network_type": generate_network_type(),
            "data_packet_size": generate_data_packet_size(),
            "device_model": generate_device_model(),
        })

    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_iot_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_iot_data')
# def download_iot_data():
#     df = generate_iot_data(500000)
#     file_path = "iot_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)