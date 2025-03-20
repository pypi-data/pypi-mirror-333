from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_citizen_id():
    return fake.uuid4()

def generate_full_name():
    return fake.name()

def generate_birth_date():
    return fake.date_of_birth(minimum_age=18, maximum_age=90)

def generate_address():
    return fake.address()

def generate_city():
    return fake.city()

def generate_state():
    return fake.state()

def generate_country():
    return fake.country()

def generate_postal_code():
    return fake.postcode()

def generate_phone_number():
    return fake.phone_number()

def generate_email():
    return fake.email()

def generate_department():
    return fake.random_element(elements=["Health", "Education", "Transportation", "Public Safety", "Housing", "Environment"])

def generate_service_type():
    return fake.random_element(elements=["Social Welfare", "Public Works", "Policy Implementation", "Emergency Response", "Community Outreach"])

def generate_application_id():
    return fake.bothify(text="APP-###-????")

def generate_request_date():
    return fake.date_this_year()

def generate_processing_status():
    return fake.random_element(elements=["Pending", "In Progress", "Completed", "Rejected"])

def generate_service_fee():
    return round(fake.pydecimal(left_digits=3, right_digits=2, positive=True), 2)

def generate_case_officer():
    return fake.name()

def generate_service_location():
    return fake.city()

def generate_beneficiary_type():
    return fake.random_element(elements=["Individual", "Organization", "Community Group"])

def generate_policy_reference():
    return fake.bothify(text="POL-####-????")

def generate_government_data(num_records=100):
    data = [
        {
            "citizen_id": generate_citizen_id(),
            "full_name": generate_full_name(),
            "birth_date": generate_birth_date(),
            "address": generate_address(),
            "city": generate_city(),
            "state": generate_state(),
            "country": generate_country(),
            "postal_code": generate_postal_code(),
            "phone_number": generate_phone_number(),
            "email": generate_email(),
            "department": generate_department(),
            "service_type": generate_service_type(),
            "application_id": generate_application_id(),
            "request_date": generate_request_date(),
            "processing_status": generate_processing_status(),
            "service_fee": generate_service_fee(),
            "case_officer": generate_case_officer(),
            "service_location": generate_service_location(),
            "beneficiary_type": generate_beneficiary_type(),
            "policy_reference": generate_policy_reference(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_government_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_government_data')
# def download_government_data():
#     df = generate_government_data(500000)
#     file_path = "government_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)