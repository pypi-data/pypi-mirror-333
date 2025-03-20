from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_person_id():
    return fake.uuid4()

def generate_first_name():
    return fake.first_name()

def generate_last_name():
    return fake.last_name()

def generate_gender():
    return fake.random_element(elements=["Male", "Female", "Non-Binary", "Other"])

def generate_age():
    return fake.random_int(min=1, max=100)

def generate_birth_date():
    return fake.date_of_birth(minimum_age=1, maximum_age=100)

def generate_ethnicity():
    return fake.random_element(elements=["Asian", "Black", "Hispanic", "White", "Mixed", "Other"])

def generate_nationality():
    return fake.country()

def generate_language():
    return fake.language_name()

def generate_education_level():
    return fake.random_element(elements=["Primary", "Secondary", "High School", "Bachelor's", "Master's", "Doctorate"])

def generate_occupation():
    return fake.job()

def generate_income_level():
    return fake.random_element(elements=["Low", "Middle", "High"])

def generate_marital_status():
    return fake.random_element(elements=["Single", "Married", "Divorced", "Widowed"])

def generate_household_size():
    return fake.random_int(min=1, max=10)

def generate_religion():
    return fake.random_element(elements=["Christianity", "Islam", "Hinduism", "Buddhism", "Judaism", "None", "Other"])

def generate_residence_type():
    return fake.random_element(elements=["Urban", "Suburban", "Rural"])

def generate_employment_status():
    return fake.random_element(elements=["Employed", "Unemployed", "Retired", "Student"])

def generate_health_status():
    return fake.random_element(elements=["Excellent", "Good", "Fair", "Poor"])

def generate_political_affiliation():
    return fake.random_element(elements=["Liberal", "Conservative", "Independent", "Other"])

def generate_citizenship_status():
    return fake.random_element(elements=["Citizen", "Permanent Resident", "Temporary Resident", "Undocumented"])

def generate_demographic_data(num_records=100):
    data = []
    for _ in range(num_records):
        data.append({
            "person_id": generate_person_id(),
            "first_name": generate_first_name(),
            "last_name": generate_last_name(),
            "gender": generate_gender(),
            "age": generate_age(),
            "birth_date": generate_birth_date(),
            "ethnicity": generate_ethnicity(),
            "nationality": generate_nationality(),
            "language": generate_language(),
            "education_level": generate_education_level(),
            "occupation": generate_occupation(),
            "income_level": generate_income_level(),
            "marital_status": generate_marital_status(),
            "household_size": generate_household_size(),
            "religion": generate_religion(),
            "residence_type": generate_residence_type(),
            "employment_status": generate_employment_status(),
            "health_status": generate_health_status(),
            "political_affiliation": generate_political_affiliation(),
            "citizenship_status": generate_citizenship_status(),
        })

    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_demographic_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_demographic_data')
# def download_demographic_data():
#     df = generate_demographic_data(500000)
#     file_path = "demographic_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)