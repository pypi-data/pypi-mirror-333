from faker import Faker
import pandas as pd
from flask import Flask, send_file
import io

fake = Faker()
app = Flask(__name__)

def generate_call_id():
    return fake.uuid4()

def generate_agent_id():
    return fake.random_number(digits=6)

def generate_customer_id():
    return fake.uuid4()

def generate_call_duration():
    return fake.random_int(min=1, max=60)

def generate_call_type():
    return fake.random_element(elements=["Inbound", "Outbound"])

def generate_call_status():
    return fake.random_element(elements=["Completed", "Missed", "Dropped"])

def generate_call_timestamp():
    return fake.date_time_this_year()

def generate_customer_satisfaction():
    return fake.random_element(elements=["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"])

def generate_issue_category():
    return fake.random_element(elements=["Billing", "Technical Support", "General Inquiry", "Complaint"])

def generate_resolution_status():
    return fake.random_element(elements=["Resolved", "Pending", "Escalated"])

def generate_call_rating():
    return fake.random_int(min=1, max=5)

def generate_agent_name():
    return fake.name()

def generate_call_center_location():
    return fake.city()

def generate_follow_up_required():
    return fake.boolean(chance_of_getting_true=30)

def generate_escalation_level():
    return fake.random_element(elements=["None", "Level 1", "Level 2", "Level 3"])

def generate_feedback_comments():
    return fake.sentence()

def generate_hold_duration():
    return fake.random_int(min=0, max=15)

def generate_call_language():
    return fake.random_element(elements=["English", "Spanish", "French", "German", "Chinese"])

def generate_call_channel():
    return fake.random_element(elements=["Phone", "Chat", "Email"])

def generate_priority_level():
    return fake.random_element(elements=["Low", "Medium", "High"])

def generate_call_center_data(num_records=100):
    data = [{
        "call_id": generate_call_id(),
        "agent_id": generate_agent_id(),
        "customer_id": generate_customer_id(),
        "call_duration": generate_call_duration(),
        "call_type": generate_call_type(),
        "call_status": generate_call_status(),
        "call_timestamp": generate_call_timestamp(),
        "customer_satisfaction": generate_customer_satisfaction(),
        "issue_category": generate_issue_category(),
        "resolution_status": generate_resolution_status(),
        "call_rating": generate_call_rating(),
        "agent_name": generate_agent_name(),
        "call_center_location": generate_call_center_location(),
        "follow_up_required": generate_follow_up_required(),
        "escalation_level": generate_escalation_level(),
        "feedback_comments": generate_feedback_comments(),
        "hold_duration": generate_hold_duration(),
        "call_language": generate_call_language(),
        "call_channel": generate_call_channel(),
        "priority_level": generate_priority_level()
    } for _ in range(num_records)]

    return pd.DataFrame(data)

# @app.route('/download_call_center_data')
# def download_call_center_data():
#     df = generate_call_center_data(num_records=500000)
#     output = io.BytesIO()
#     df.to_csv(output, index=False)
#     output.seek(0)

#     return send_file(output, mimetype='text/csv', as_attachment=True, download_name='call_center_data.csv')

# if __name__ == '__main__':
#     sample_df = generate_call_center_data(10)
#     print(sample_df.head(10))
#     app.run(debug=True)
