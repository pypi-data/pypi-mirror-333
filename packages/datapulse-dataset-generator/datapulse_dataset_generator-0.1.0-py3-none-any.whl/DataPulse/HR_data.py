from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_employee_id():
    return fake.uuid4()

def generate_first_name():
    return fake.first_name()

def generate_last_name():
    return fake.last_name()

def generate_department():
    return fake.random_element(elements=["HR", "IT", "Finance", "Marketing", "Sales", "Operations"])

def generate_position():
    return fake.job()

def generate_hire_date():
    return fake.date_between(start_date='-10y', end_date='today')

def generate_salary():
    return round(fake.pyfloat(left_digits=5, right_digits=2, positive=True, min_value=30000, max_value=150000), 2)

def generate_email():
    return fake.company_email()

def generate_phone_number():
    return fake.phone_number()

def generate_performance_rating():
    return fake.random_element(elements=["Excellent", "Good", "Average", "Below Average", "Poor"])

def generate_employment_status():
    return fake.random_element(elements=["Active", "On Leave", "Terminated"])

def generate_manager_id():
    return fake.uuid4()

def generate_birth_date():
    return fake.date_of_birth(minimum_age=18, maximum_age=65)

def generate_gender():
    return fake.random_element(elements=["Male", "Female", "Other"])

def generate_address():
    return fake.address()

def generate_work_location():
    return fake.city()

def generate_contract_type():
    return fake.random_element(elements=["Full-Time", "Part-Time", "Contract", "Internship"])

def generate_benefit_plan():
    return fake.random_element(elements=["Basic", "Standard", "Premium", "Executive"])

def generate_leave_balance():
    return fake.random_int(min=0, max=30)

def generate_promotion_status():
    return fake.boolean(chance_of_getting_true=20)

def generate_hr_data(num_records=100):
    data = [
        {
            "employee_id": generate_employee_id(),
            "first_name": generate_first_name(),
            "last_name": generate_last_name(),
            "department": generate_department(),
            "position": generate_position(),
            "hire_date": generate_hire_date(),
            "salary": generate_salary(),
            "email": generate_email(),
            "phone_number": generate_phone_number(),
            "performance_rating": generate_performance_rating(),
            "employment_status": generate_employment_status(),
            "manager_id": generate_manager_id(),
            "birth_date": generate_birth_date(),
            "gender": generate_gender(),
            "address": generate_address(),
            "work_location": generate_work_location(),
            "contract_type": generate_contract_type(),
            "benefit_plan": generate_benefit_plan(),
            "leave_balance": generate_leave_balance(),
            "promotion_status": generate_promotion_status(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_hr_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_hr_data')
# def download_hr_data():
#     df = generate_hr_data(500000)
#     file_path = "hr_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
