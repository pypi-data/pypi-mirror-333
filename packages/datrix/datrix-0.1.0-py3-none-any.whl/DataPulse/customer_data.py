from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_customer_id():
    return fake.uuid4()

def generate_customer_name():
    return fake.name()

def generate_age():
    return fake.random_int(min=18, max=90)

def generate_gender():
    return fake.random_element(elements=["Male", "Female", "Other"])

def generate_email():
    return fake.email()

def generate_phone_number():
    return fake.phone_number()

def generate_address():
    return fake.address()

def generate_city():
    return fake.city()

def generate_state():
    return fake.state()

def generate_country():
    return fake.country()

def generate_postal_code():
    return fake.postcode()

def generate_registration_date():
    return fake.date_this_decade()

def generate_last_purchase_date():
    return fake.date_between(start_date='-1y', end_date='today')

def generate_loyalty_points():
    return fake.random_int(min=0, max=10000)

def generate_preferred_payment_method():
    return fake.random_element(elements=["Credit Card", "Debit Card", "PayPal", "Bank Transfer"])

def generate_customer_segment():
    return fake.random_element(elements=["Regular", "VIP", "Wholesale", "Online-Only"])

def generate_subscription_status():
    return fake.random_element(elements=["Active", "Inactive", "Cancelled"])

def generate_total_spent():
    return round(fake.pydecimal(left_digits=7, right_digits=2, positive=True), 2)

def generate_feedback_score():
    return fake.random_int(min=1, max=5)

def generate_referral_source():
    return fake.random_element(elements=["Social Media", "Friend", "Advertisement", "Search Engine"])

def generate_customer_data(num_records=100):
    data = []
    for _ in range(num_records):
        data.append({
            "customer_id": generate_customer_id(),
            "customer_name": generate_customer_name(),
            "age": generate_age(),
            "gender": generate_gender(),
            "email": generate_email(),
            "phone_number": generate_phone_number(),
            "address": generate_address(),
            "city": generate_city(),
            "state": generate_state(),
            "country": generate_country(),
            "postal_code": generate_postal_code(),
            "registration_date": generate_registration_date(),
            "last_purchase_date": generate_last_purchase_date(),
            "loyalty_points": generate_loyalty_points(),
            "preferred_payment_method": generate_preferred_payment_method(),
            "customer_segment": generate_customer_segment(),
            "subscription_status": generate_subscription_status(),
            "total_spent": generate_total_spent(),
            "feedback_score": generate_feedback_score(),
            "referral_source": generate_referral_source(),
        })

    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_customer_data(10)
print(df_sample.head())

# # Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_customer_data')
# def download_customer_data():
#     df = generate_customer_data(500000)
#     file_path = "customer_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)