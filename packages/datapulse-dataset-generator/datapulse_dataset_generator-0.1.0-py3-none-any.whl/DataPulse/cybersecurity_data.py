from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_incident_id():
    return fake.uuid4()

def generate_incident_type():
    return fake.random_element(elements=["Phishing", "Malware", "Data Breach", "DDoS", "Ransomware"])

def generate_incident_date():
    return fake.date_time_this_year()

def generate_severity_level():
    return fake.random_element(elements=["Low", "Medium", "High", "Critical"])

def generate_source_ip():
    return fake.ipv4()

def generate_destination_ip():
    return fake.ipv4()

def generate_attack_vector():
    return fake.random_element(elements=["Email", "Network", "Application", "Physical Access"])

def generate_compromised_system():
    return fake.random_element(elements=["Database Server", "Web Server", "User Workstation", "Mobile Device"])

def generate_detection_method():
    return fake.random_element(elements=["Firewall", "IDS/IPS", "User Report", "SIEM"])

def generate_response_action():
    return fake.random_element(elements=["Isolated", "Patched", "Monitored", "No Action"])

def generate_affected_department():
    return fake.random_element(elements=["IT", "Finance", "HR", "Marketing"])

def generate_exfiltrated_data_size():
    return f"{fake.random_int(min=1, max=100)} MB"

def generate_malware_family():
    return fake.random_element(elements=["Trojan", "Worm", "Ransomware", "Spyware"])

def generate_patch_status():
    return fake.random_element(elements=["Patched", "Unpatched", "Pending"])

def generate_reported_by():
    return fake.name()

def generate_incident_duration():
    return f"{fake.random_int(min=1, max=72)} hours"

def generate_risk_score():
    return round(fake.pyfloat(left_digits=2, right_digits=1, positive=True, min_value=0, max_value=10), 1)

def generate_attack_motivation():
    return fake.random_element(elements=["Financial Gain", "Espionage", "Revenge", "Accidental"])

def generate_data_encrypted():
    return fake.boolean(chance_of_getting_true=70)

def generate_threat_actor_type():
    return fake.random_element(elements=["Internal", "External", "Third-party"])

def generate_cybersecurity_data(num_records=100):
    data = [
        {
            "incident_id": generate_incident_id(),
            "incident_type": generate_incident_type(),
            "incident_date": generate_incident_date(),
            "severity_level": generate_severity_level(),
            "source_ip": generate_source_ip(),
            "destination_ip": generate_destination_ip(),
            "attack_vector": generate_attack_vector(),
            "compromised_system": generate_compromised_system(),
            "detection_method": generate_detection_method(),
            "response_action": generate_response_action(),
            "affected_department": generate_affected_department(),
            "exfiltrated_data_size": generate_exfiltrated_data_size(),
            "malware_family": generate_malware_family(),
            "patch_status": generate_patch_status(),
            "reported_by": generate_reported_by(),
            "incident_duration": generate_incident_duration(),
            "risk_score": generate_risk_score(),
            "attack_motivation": generate_attack_motivation(),
            "data_encrypted": generate_data_encrypted(),
            "threat_actor_type": generate_threat_actor_type(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_cybersecurity_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_cybersecurity_data')
# def download_cybersecurity_data():
#     df = generate_cybersecurity_data(500000)
#     file_path = "cybersecurity_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)