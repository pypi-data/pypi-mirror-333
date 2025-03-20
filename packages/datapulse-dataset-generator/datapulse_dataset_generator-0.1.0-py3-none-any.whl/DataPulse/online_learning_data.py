from faker import Faker
import pandas as pd
from flask import Flask, send_file
import io

fake = Faker()
app = Flask(__name__)

def generate_course_id():
    return fake.uuid4()

def generate_course_name():
    return fake.sentence(nb_words=4)

def generate_instructor_name():
    return fake.name()

def generate_student_id():
    return fake.uuid4()

def generate_student_name():
    return fake.name()

def generate_enrollment_date():
    return fake.date_this_year()

def generate_completion_date():
    return fake.date_this_year()

def generate_course_duration():
    return fake.random_int(min=4, max=52)

def generate_grade():
    return fake.random_element(elements=["A", "B", "C", "D", "F"])

def generate_course_level():
    return fake.random_element(elements=["Beginner", "Intermediate", "Advanced"])

def generate_platform():
    return fake.random_element(elements=["Udemy", "Coursera", "edX", "Skillshare", "LinkedIn Learning"])

def generate_student_age():
    return fake.random_int(min=18, max=60)

def generate_country():
    return fake.country()

def generate_language():
    return fake.random_element(elements=["English", "Spanish", "French", "German", "Chinese"])

def generate_certification_awarded():
    return fake.boolean()

def generate_feedback_score():
    return round(fake.pyfloat(left_digits=1, right_digits=2, positive=True, max_value=5.0), 2)

def generate_device_used():
    return fake.random_element(elements=["Laptop", "Desktop", "Tablet", "Smartphone"])

def generate_payment_method():
    return fake.random_element(elements=["Credit Card", "Debit Card", "PayPal", "Bank Transfer"])

def generate_online_learning_data(num_records=100):
    data = [{
        "course_id": generate_course_id(),
        "course_name": generate_course_name(),
        "instructor_name": generate_instructor_name(),
        "student_id": generate_student_id(),
        "student_name": generate_student_name(),
        "enrollment_date": generate_enrollment_date(),
        "completion_date": generate_completion_date(),
        "course_duration_weeks": generate_course_duration(),
        "grade": generate_grade(),
        "course_level": generate_course_level(),
        "platform": generate_platform(),
        "student_age": generate_student_age(),
        "country": generate_country(),
        "language": generate_language(),
        "certification_awarded": generate_certification_awarded(),
        "feedback_score": generate_feedback_score(),
        "device_used": generate_device_used(),
        "payment_method": generate_payment_method()
    } for _ in range(num_records)]

    return pd.DataFrame(data)

# @app.route('/download_online_learning_data')
# def download_online_learning_data():
#     df = generate_online_learning_data(num_records=500000)
#     output = io.BytesIO()
#     df.to_csv(output, index=False)
#     output.seek(0)

#     return send_file(output, mimetype='text/csv', as_attachment=True, download_name='online_learning_data.csv')

# if __name__ == '__main__':
#     sample_df = generate_online_learning_data(10)
#     print(sample_df.head(10))
#     app.run(debug=True)
