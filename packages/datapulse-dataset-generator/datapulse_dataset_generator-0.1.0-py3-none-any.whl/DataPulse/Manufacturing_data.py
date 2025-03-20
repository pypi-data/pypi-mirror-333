from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_product_id():
    return fake.uuid4()

def generate_product_name():
    return fake.word().capitalize() + " " + fake.word().capitalize()

def generate_batch_number():
    return fake.bothify(text="BATCH-####")

def generate_manufacturing_date():
    return fake.date_this_decade()

def generate_expiry_date():
    return fake.date_this_decade(after_today=True)

def generate_factory_location():
    return fake.city()

def generate_machine_id():
    return fake.bothify(text="M-###")

def generate_worker_id():
    return fake.random_number(digits=6)

def generate_quality_check_status():
    return fake.random_element(elements=["Passed", "Failed", "Pending"])

def generate_material_used():
    return fake.random_element(elements=["Steel", "Plastic", "Aluminum", "Wood", "Rubber"])

def generate_production_cost():
    return round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2)

def generate_output_quantity():
    return fake.random_int(min=100, max=10000)

def generate_defect_rate():
    return round(fake.pyfloat(left_digits=1, right_digits=3, positive=True), 3)

def generate_shift():
    return fake.random_element(elements=["Day", "Night"])

def generate_supervisor_name():
    return fake.name()

def generate_power_consumption():
    return round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)

def generate_production_line():
    return fake.bothify(text="Line-##")

def generate_storage_condition():
    return fake.random_element(elements=["Cool", "Dry", "Ambient"])

def generate_shipping_status():
    return fake.random_element(elements=["Ready", "In Transit", "Delayed"])

def generate_equipment_used():
    return fake.random_element(elements=["CNC Machine", "Conveyor Belt", "Injection Molder", "Lathe", "Press"])

def generate_manufacturing_data(num_records=100):
    data = [
        {
            "product_id": generate_product_id(),
            "product_name": generate_product_name(),
            "batch_number": generate_batch_number(),
            "manufacturing_date": generate_manufacturing_date(),
            "expiry_date": generate_expiry_date(),
            "factory_location": generate_factory_location(),
            "machine_id": generate_machine_id(),
            "worker_id": generate_worker_id(),
            "quality_check_status": generate_quality_check_status(),
            "material_used": generate_material_used(),
            "production_cost": generate_production_cost(),
            "output_quantity": generate_output_quantity(),
            "defect_rate": generate_defect_rate(),
            "shift": generate_shift(),
            "supervisor_name": generate_supervisor_name(),
            "power_consumption": generate_power_consumption(),
            "production_line": generate_production_line(),
            "storage_condition": generate_storage_condition(),
            "shipping_status": generate_shipping_status(),
            "equipment_used": generate_equipment_used(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_manufacturing_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_manufacturing_data')
# def download_manufacturing_data():
#     df = generate_manufacturing_data(500000)
#     file_path = "manufacturing_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
