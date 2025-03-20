from faker import Faker
import pandas as pd
from flask import Flask, send_file
import io

fake = Faker()
app = Flask(__name__)

def generate_pensioner_name():
    return fake.name()

def generate_pension_type():
    return fake.random_element(elements=["Government Pension", "Private Pension", "Social Security", "Retirement Savings Plan"])

def generate_pension_amount():
    return round(fake.pydecimal(left_digits=6, right_digits=2, positive=True), 2)

def generate_currency():
    return fake.currency_code()

def generate_retirement_date():
    return fake.date_between(start_date="-30y", end_date="today")

def generate_pension_status():
    return fake.random_element(elements=["Active", "Inactive", "Suspended", "Terminated"])

def generate_contribution_amount():
    return round(fake.pydecimal(left_digits=5, right_digits=2, positive=True), 2)

def generate_beneficiary_name():
    return fake.name()

def generate_benefit_frequency():
    return fake.random_element(elements=["Monthly", "Quarterly", "Annually"])

def generate_plan_id():
    return fake.bothify("PLAN-####")

def generate_insurer_name():
    return fake.company()

def generate_payout_amount():
    return round(fake.pydecimal(left_digits=6, right_digits=2, positive=True), 2)

def generate_tax_rate():
    return round(fake.pyfloat(left_digits=1, right_digits=2, positive=True, max_value=0.5), 2)

def generate_pension_id():
    return fake.uuid4()

def generate_advisor_name():
    return fake.name()

def generate_geographical_region():
    return fake.country()

def generate_employer_contribution():
    return round(fake.pydecimal(left_digits=5, right_digits=2, positive=True), 2)

def generate_retirement_age():
    return fake.random_int(min=55, max=70)

def generate_withdrawal_date():
    return fake.date_between(start_date="today", end_date="+20y")

def generate_investment_strategy():
    return fake.random_element(elements=["Conservative", "Balanced", "Growth", "Aggressive"])

def generate_pension_data(num_records=100):
    data = [{
        "pensioner_name": generate_pensioner_name(),
        "pension_type": generate_pension_type(),
        "pension_amount": generate_pension_amount(),
        "currency": generate_currency(),
        "retirement_date": generate_retirement_date(),
        "pension_status": generate_pension_status(),
        "contribution_amount": generate_contribution_amount(),
        "beneficiary_name": generate_beneficiary_name(),
        "benefit_frequency": generate_benefit_frequency(),
        "plan_id": generate_plan_id(),
        "insurer_name": generate_insurer_name(),
        "payout_amount": generate_payout_amount(),
        "tax_rate": generate_tax_rate(),
        "pension_id": generate_pension_id(),
        "advisor_name": generate_advisor_name(),
        "geographical_region": generate_geographical_region(),
        "employer_contribution": generate_employer_contribution(),
        "retirement_age": generate_retirement_age(),
        "withdrawal_date": generate_withdrawal_date(),
        "investment_strategy": generate_investment_strategy()
    } for _ in range(num_records)]

    return pd.DataFrame(data)

# @app.route('/download_pension_data')
# def download_pension_data():
#     df = generate_pension_data(num_records=500000)
#     output = io.BytesIO()
#     df.to_csv(output, index=False)
#     output.seek(0)

#     return send_file(output, mimetype='text/csv', as_attachment=True, download_name='pension_data.csv')

# if __name__ == '__main__':
#     sample_df = generate_pension_data(10)
#     print(sample_df.head(10))
#     app.run(debug=True)
