from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_policy_id():
    return fake.uuid4()

def generate_policy_holder_name():
    return fake.name()

def generate_policy_type():
    return fake.random_element(elements=["Health", "Auto", "Home", "Life", "Travel", "Business"])

def generate_premium_amount():
    return round(fake.pydecimal(left_digits=5, right_digits=2, positive=True, min_value=100, max_value=10000), 2)

def generate_policy_start_date():
    return fake.date_between(start_date='-5y', end_date='today')

def generate_policy_end_date():
    return fake.date_between(start_date='today', end_date='+5y')

def generate_claim_status():
    return fake.random_element(elements=["Approved", "Pending", "Denied", "In Progress"])

def generate_claim_amount():
    return round(fake.pydecimal(left_digits=5, right_digits=2, positive=True, min_value=500, max_value=50000), 2)

def generate_insurer_name():
    return fake.company()

def generate_policy_number():
    return fake.bothify(text="??-#####")

def generate_beneficiary_name():
    return fake.name()

def generate_contact_number():
    return fake.phone_number()

def generate_email():
    return fake.email()

def generate_address():
    return fake.address()

def generate_policy_renewal_status():
    return fake.boolean(chance_of_getting_true=70)

def generate_risk_category():
    return fake.random_element(elements=["Low", "Medium", "High"])

def generate_policy_discount():
    return round(fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=0, max_value=500), 2)

def generate_underwriter():
    return fake.name()

def generate_claim_date():
    return fake.date_between(start_date='-3y', end_date='today')

def generate_policy_status():
    return fake.random_element(elements=["Active", "Lapsed", "Cancelled"])

def generate_insurance_data(num_records=100):
    data = [
        {
            "policy_id": generate_policy_id(),
            "policy_holder_name": generate_policy_holder_name(),
            "policy_type": generate_policy_type(),
            "premium_amount": generate_premium_amount(),
            "policy_start_date": generate_policy_start_date(),
            "policy_end_date": generate_policy_end_date(),
            "claim_status": generate_claim_status(),
            "claim_amount": generate_claim_amount(),
            "insurer_name": generate_insurer_name(),
            "policy_number": generate_policy_number(),
            "beneficiary_name": generate_beneficiary_name(),
            "contact_number": generate_contact_number(),
            "email": generate_email(),
            "address": generate_address(),
            "policy_renewal_status": generate_policy_renewal_status(),
            "risk_category": generate_risk_category(),
            "policy_discount": generate_policy_discount(),
            "underwriter": generate_underwriter(),
            "claim_date": generate_claim_date(),
            "policy_status": generate_policy_status(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_insurance_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_insurance_data')
# def download_insurance_data():
#     df = generate_insurance_data(500000)
#     file_path = "insurance_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
