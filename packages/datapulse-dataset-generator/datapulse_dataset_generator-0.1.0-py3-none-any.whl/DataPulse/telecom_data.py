from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_subscriber_id():
    return fake.uuid4()

def generate_phone_number():
    return fake.phone_number()

def generate_plan_type():
    return fake.random_element(elements=["Prepaid", "Postpaid", "Family", "Business"])

def generate_data_usage_gb():
    return round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)

def generate_call_duration_min():
    return round(fake.pyfloat(left_digits=3, right_digits=1, positive=True), 1)

def generate_sms_count():
    return fake.random_int(min=0, max=500)

def generate_billing_amount():
    return round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)

def generate_service_provider():
    return fake.company()

def generate_country():
    return fake.country()

def generate_city():
    return fake.city()

def generate_connection_type():
    return fake.random_element(elements=["4G", "5G", "Fiber", "DSL"])

def generate_activation_date():
    return fake.date_this_decade()

def generate_payment_status():
    return fake.random_element(elements=["Paid", "Pending", "Overdue"])

def generate_customer_age():
    return fake.random_int(min=18, max=85)

def generate_device_type():
    return fake.random_element(elements=["Smartphone", "Tablet", "Router", "Smartwatch"])

def generate_network_latency_ms():
    return fake.random_int(min=10, max=500)

def generate_contract_duration_months():
    return fake.random_int(min=1, max=36)

def generate_ip_address():
    return fake.ipv4()

def generate_customer_satisfaction():
    return fake.random_element(elements=["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"])

def generate_data_roaming():
    return fake.boolean(chance_of_getting_true=20)

def generate_telecommunication_data(num_records=100):
    data = [
        {
            "subscriber_id": generate_subscriber_id(),
            "phone_number": generate_phone_number(),
            "plan_type": generate_plan_type(),
            "data_usage_gb": generate_data_usage_gb(),
            "call_duration_min": generate_call_duration_min(),
            "sms_count": generate_sms_count(),
            "billing_amount": generate_billing_amount(),
            "service_provider": generate_service_provider(),
            "country": generate_country(),
            "city": generate_city(),
            "connection_type": generate_connection_type(),
            "activation_date": generate_activation_date(),
            "payment_status": generate_payment_status(),
            "customer_age": generate_customer_age(),
            "device_type": generate_device_type(),
            "network_latency_ms": generate_network_latency_ms(),
            "contract_duration_months": generate_contract_duration_months(),
            "ip_address": generate_ip_address(),
            "customer_satisfaction": generate_customer_satisfaction(),
            "data_roaming": generate_data_roaming(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_telecommunication_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_telecommunication_data')
# def download_telecommunication_data():
#     df = generate_telecommunication_data(500000)
#     file_path = "telecommunication_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
