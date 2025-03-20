from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_property_id():
    return fake.uuid4()

def generate_listing_price():
    return round(fake.pydecimal(left_digits=7, right_digits=2, positive=True), 2)

def generate_property_type():
    return fake.random_element(elements=["Apartment", "House", "Condo", "Villa", "Townhouse"])

def generate_address():
    return fake.address()

def generate_city():
    return fake.city()

def generate_state():
    return fake.state()

def generate_zip_code():
    return fake.zipcode()

def generate_country():
    return fake.country()

def generate_bedrooms():
    return fake.random_int(min=1, max=10)

def generate_bathrooms():
    return fake.random_int(min=1, max=8)

def generate_square_feet():
    return fake.random_int(min=500, max=10000)

def generate_listing_date():
    return fake.date_this_year()

def generate_sale_status():
    return fake.random_element(elements=["Available", "Pending", "Sold"])

def generate_agent_name():
    return fake.name()

def generate_agent_phone():
    return fake.phone_number()

def generate_year_built():
    return fake.random_int(min=1900, max=2023)

def generate_parking_spaces():
    return fake.random_int(min=0, max=5)

def generate_property_tax():
    return round(fake.pydecimal(left_digits=5, right_digits=2, positive=True), 2)

def generate_listing_description():
    return fake.sentence(nb_words=15)

def generate_hoa_fee():
    return round(fake.pydecimal(left_digits=4, right_digits=2, positive=True), 2)

def generate_real_estate_data(num_records=100):
    data = [
        {
            "property_id": generate_property_id(),
            "listing_price": generate_listing_price(),
            "property_type": generate_property_type(),
            "address": generate_address(),
            "city": generate_city(),
            "state": generate_state(),
            "zip_code": generate_zip_code(),
            "country": generate_country(),
            "bedrooms": generate_bedrooms(),
            "bathrooms": generate_bathrooms(),
            "square_feet": generate_square_feet(),
            "listing_date": generate_listing_date(),
            "sale_status": generate_sale_status(),
            "agent_name": generate_agent_name(),
            "agent_phone": generate_agent_phone(),
            "year_built": generate_year_built(),
            "parking_spaces": generate_parking_spaces(),
            "property_tax": generate_property_tax(),
            "listing_description": generate_listing_description(),
            "hoa_fee": generate_hoa_fee(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_real_estate_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_real_estate_data')
# def download_real_estate_data():
#     df = generate_real_estate_data(500000)
#     file_path = "real_estate_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
