from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_student_id():
    return fake.uuid4()

def generate_student_name():
    return fake.name()

def generate_age():
    return fake.random_int(min=18, max=30)

def generate_gender():
    return fake.random_element(elements=["Male", "Female", "Non-Binary"])

def generate_course_name():
    return fake.random_element(elements=["Computer Science", "Mathematics", "Physics", "Biology", "Economics", "History", "Literature", "Engineering"])

def generate_enrollment_year():
    return fake.random_int(min=2015, max=2024)

def generate_gpa():
    return round(fake.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=2.0, max_value=4.0), 2)

def generate_institution_name():
    return fake.company()

def generate_email():
    return fake.email()

def generate_phone_number():
    return fake.phone_number()

def generate_address():
    return fake.address()

def generate_course_code():
    return fake.bothify(text="CSE###")

def generate_credit_hours():
    return fake.random_int(min=1, max=4)

def generate_semester():
    return fake.random_element(elements=["Spring", "Summer", "Fall", "Winter"])

def generate_faculty_name():
    return fake.name()

def generate_classroom_number():
    return fake.bothify(text="Room ###")

def generate_grade():
    return fake.random_element(elements=["A", "B", "C", "D", "F"])

def generate_scholarship_status():
    return fake.random_element(elements=["Yes", "No"])

def generate_graduation_status():
    return fake.random_element(elements=["Graduated", "In Progress", "Dropped Out"])

def generate_student_club():
    return fake.random_element(elements=["Robotics Club", "Drama Society", "Sports Club", "Music Club", "Debate Club"])

def generate_educational_data(num_records=100):
    data = [
        {
            "student_id": generate_student_id(),
            "student_name": generate_student_name(),
            "age": generate_age(),
            "gender": generate_gender(),
            "course_name": generate_course_name(),
            "enrollment_year": generate_enrollment_year(),
            "gpa": generate_gpa(),
            "institution_name": generate_institution_name(),
            "email": generate_email(),
            "phone_number": generate_phone_number(),
            "address": generate_address(),
            "course_code": generate_course_code(),
            "credit_hours": generate_credit_hours(),
            "semester": generate_semester(),
            "faculty_name": generate_faculty_name(),
            "classroom_number": generate_classroom_number(),
            "grade": generate_grade(),
            "scholarship_status": generate_scholarship_status(),
            "graduation_status": generate_graduation_status(),
            "student_club": generate_student_club(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_educational_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_educational_data')
# def download_educational_data():
#     df = generate_educational_data(500000)
#     file_path = "educational_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
