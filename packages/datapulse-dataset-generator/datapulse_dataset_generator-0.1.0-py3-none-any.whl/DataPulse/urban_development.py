from faker import Faker
import pandas as pd
from flask import Flask, send_file
import io

fake = Faker()
app = Flask(__name__)

def generate_project_id():
    return fake.uuid4()

def generate_project_name():
    return fake.company() + " Urban Development"

def generate_location():
    return fake.city()

def generate_start_date():
    return fake.date_this_decade()

def generate_end_date():
    return fake.date_this_decade()

def generate_budget():
    return round(fake.pydecimal(left_digits=8, right_digits=2, positive=True), 2)

def generate_project_status():
    return fake.random_element(elements=["Planning", "In Progress", "Completed", "On Hold"])

def generate_project_manager():
    return fake.name()

def generate_contractor():
    return fake.company()

def generate_building_type():
    return fake.random_element(elements=["Residential", "Commercial", "Industrial", "Mixed-Use"])

def generate_zone():
    return fake.random_element(elements=["Urban", "Suburban", "Rural"])

def generate_environmental_impact():
    return fake.random_element(elements=["Low", "Moderate", "High"])

def generate_permits_issued():
    return fake.boolean()

def generate_population_served():
    return fake.random_int(min=500, max=100000)

def generate_green_certification():
    return fake.random_element(elements=["LEED", "BREEAM", "None"])

def generate_public_transport_access():
    return fake.random_element(elements=["High", "Medium", "Low"])

def generate_infrastructure_type():
    return fake.random_element(elements=["Roads", "Parks", "Utilities", "Mixed"])

def generate_funding_source():
    return fake.random_element(elements=["Government", "Private", "Public-Private Partnership"])

def generate_land_area():
    return round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2)

def generate_community_involvement():
    return fake.random_element(elements=["High", "Medium", "Low"])

def generate_urban_development_data(num_records=100):
    data = [{
        "project_id": generate_project_id(),
        "project_name": generate_project_name(),
        "location": generate_location(),
        "start_date": generate_start_date(),
        "end_date": generate_end_date(),
        "budget": generate_budget(),
        "project_status": generate_project_status(),
        "project_manager": generate_project_manager(),
        "contractor": generate_contractor(),
        "building_type": generate_building_type(),
        "zone": generate_zone(),
        "environmental_impact": generate_environmental_impact(),
        "permits_issued": generate_permits_issued(),
        "population_served": generate_population_served(),
        "green_certification": generate_green_certification(),
        "public_transport_access": generate_public_transport_access(),
        "infrastructure_type": generate_infrastructure_type(),
        "funding_source": generate_funding_source(),
        "land_area": generate_land_area(),
        "community_involvement": generate_community_involvement()
    } for _ in range(num_records)]

    return pd.DataFrame(data)

# @app.route('/download_urban_development_data')
# def download_urban_development_data():
#     df = generate_urban_development_data(num_records=500000)
#     output = io.BytesIO()
#     df.to_csv(output, index=False)
#     output.seek(0)

#     return send_file(output, mimetype='text/csv', as_attachment=True, download_name='urban_development_data.csv')

# if __name__ == '__main__':
#     sample_df = generate_urban_development_data(10)
#     print(sample_df.head(10))
#     app.run(debug=True)
