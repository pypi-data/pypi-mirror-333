from faker import Faker
import pandas as pd
from flask import Flask, send_file
import io

fake = Faker()
app = Flask(__name__)

def generate_asset_id():
    return fake.uuid4()

def generate_asset_name():
    return fake.random_element(elements=["Computer", "Vehicle", "Machinery", "Furniture", "Building"])

def generate_purchase_date():
    return fake.date_this_decade()

def generate_asset_value():
    return round(fake.pydecimal(left_digits=7, right_digits=2, positive=True), 2)

def generate_depreciation_rate():
    return round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)

def generate_current_value():
    return round(fake.pydecimal(left_digits=7, right_digits=2, positive=True), 2)

def generate_location():
    return fake.city()

def generate_asset_status():
    return fake.random_element(elements=["Active", "In Maintenance", "Retired", "Disposed"])

def generate_responsible_person():
    return fake.name()

def generate_serial_number():
    return fake.bothify("??-####-??")

def generate_warranty_expiration():
    return fake.date_this_decade()

def generate_asset_category():
    return fake.random_element(elements=["Electronics", "Vehicles", "Buildings", "Tools", "Furniture"])

def generate_supplier():
    return fake.company()

def generate_purchase_price():
    return round(fake.pydecimal(left_digits=7, right_digits=2, positive=True), 2)

def generate_last_maintenance():
    return fake.date_this_year()

def generate_next_maintenance():
    return fake.date_this_year()

def generate_usage_hours():
    return fake.random_int(min=0, max=10000)

def generate_asset_condition():
    return fake.random_element(elements=["New", "Good", "Fair", "Poor"])

def generate_insurance_policy():
    return fake.bothify("POL-####-###")

def generate_insurance_expiration():
    return fake.date_this_decade()

def generate_asset_management_data(num_records=100):
    data = [{
        "asset_id": generate_asset_id(),
        "asset_name": generate_asset_name(),
        "purchase_date": generate_purchase_date(),
        "asset_value": generate_asset_value(),
        "depreciation_rate": generate_depreciation_rate(),
        "current_value": generate_current_value(),
        "location": generate_location(),
        "asset_status": generate_asset_status(),
        "responsible_person": generate_responsible_person(),
        "serial_number": generate_serial_number(),
        "warranty_expiration": generate_warranty_expiration(),
        "asset_category": generate_asset_category(),
        "supplier": generate_supplier(),
        "purchase_price": generate_purchase_price(),
        "last_maintenance": generate_last_maintenance(),
        "next_maintenance": generate_next_maintenance(),
        "usage_hours": generate_usage_hours(),
        "asset_condition": generate_asset_condition(),
        "insurance_policy": generate_insurance_policy(),
        "insurance_expiration": generate_insurance_expiration()
    } for _ in range(num_records)]

    return pd.DataFrame(data)

# @app.route('/download_asset_management_data')
# def download_asset_management_data():
#     df = generate_asset_management_data(num_records=500000)
#     output = io.BytesIO()
#     df.to_csv(output, index=False)
#     output.seek(0)

#     return send_file(output, mimetype='text/csv', as_attachment=True, download_name='asset_management_data.csv')

# if __name__ == '__main__':
#     sample_df = generate_asset_management_data(10)
#     print(sample_df.head(10))
#     app.run(debug=True)
