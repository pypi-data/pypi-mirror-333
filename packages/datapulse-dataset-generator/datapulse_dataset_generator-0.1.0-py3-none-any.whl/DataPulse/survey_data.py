from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_survey_id():
    return fake.uuid4()

def generate_respondent_id():
    return fake.uuid4()

def generate_survey_title():
    return fake.sentence(nb_words=5)

def generate_question():
    return fake.sentence(nb_words=10)

def generate_response():
    return fake.random_element(elements=["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"])

def generate_response_date():
    return fake.date_between(start_date='-1y', end_date='today')

def generate_location():
    return fake.city()

def generate_age():
    return fake.random_int(min=18, max=80)

def generate_gender():
    return fake.random_element(elements=["Male", "Female", "Non-Binary", "Prefer Not to Say"])

def generate_income_level():
    return fake.random_element(elements=["Low", "Medium", "High"])

def generate_education_level():
    return fake.random_element(elements=["High School", "Bachelor's", "Master's", "PhD"])

def generate_satisfaction_score():
    return fake.random_int(min=1, max=10)

def generate_feedback():
    return fake.paragraph(nb_sentences=2)

def generate_device_used():
    return fake.random_element(elements=["Mobile", "Desktop", "Tablet"])

def generate_channel():
    return fake.random_element(elements=["Email", "Website", "In-person", "Phone"])

def generate_follow_up_required():
    return fake.boolean(chance_of_getting_true=20)

def generate_time_spent():
    return fake.random_int(min=1, max=60)  # Time in minutes

def generate_ip_address():
    return fake.ipv4()

def generate_language():
    return fake.random_element(elements=["English", "Spanish", "French", "German", "Chinese"])

def generate_survey_type():
    return fake.random_element(elements=["Customer Satisfaction", "Market Research", "Employee Feedback", "Product Review"])

def generate_survey_data(num_records=100):
    data = [
        {
            "survey_id": generate_survey_id(),
            "respondent_id": generate_respondent_id(),
            "survey_title": generate_survey_title(),
            "question": generate_question(),
            "response": generate_response(),
            "response_date": generate_response_date(),
            "location": generate_location(),
            "age": generate_age(),
            "gender": generate_gender(),
            "income_level": generate_income_level(),
            "education_level": generate_education_level(),
            "satisfaction_score": generate_satisfaction_score(),
            "feedback": generate_feedback(),
            "device_used": generate_device_used(),
            "channel": generate_channel(),
            "follow_up_required": generate_follow_up_required(),
            "time_spent": generate_time_spent(),
            "ip_address": generate_ip_address(),
            "language": generate_language(),
            "survey_type": generate_survey_type(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_survey_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_survey_data')
# def download_survey_data():
#     df = generate_survey_data(500000)
#     file_path = "survey_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)