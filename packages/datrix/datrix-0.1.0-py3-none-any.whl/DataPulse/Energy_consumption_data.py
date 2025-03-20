from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_meter_id():
    return fake.uuid4()

def generate_energy_type():
    return fake.random_element(elements=["Electricity", "Gas", "Solar", "Wind", "Hydro"])

def generate_consumption_value():
    return round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2)

def generate_unit():
    return fake.random_element(elements=["kWh", "MJ", "Therms", "m³"])

def generate_billing_cycle():
    return fake.random_element(elements=["Monthly", "Quarterly", "Annual"])

def generate_customer_id():
    return fake.uuid4()

def generate_city():
    return fake.city()

def generate_country():
    return fake.country()

def generate_meter_read_date():
    return fake.date_this_year()

def generate_tariff_rate():
    return round(fake.pyfloat(left_digits=2, right_digits=4, positive=True), 4)

def generate_peak_usage():
    return round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)

def generate_off_peak_usage():
    return round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)

def generate_total_cost():
    return round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2)

def generate_provider_name():
    return fake.company()

def generate_energy_efficiency_rating():
    return fake.random_element(elements=["A", "B", "C", "D", "E"])

def generate_usage_category():
    return fake.random_element(elements=["Residential", "Commercial", "Industrial"])

def generate_power_factor():
    return round(fake.pyfloat(left_digits=1, right_digits=3, positive=True), 3)

def generate_carbon_emissions():
    return round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)

def generate_invoice_number():
    return fake.bothify(text="INV-#######")

def generate_payment_status():
    return fake.random_element(elements=["Paid", "Pending", "Overdue"])

def generate_energy_consumption_data(num_records=100):
    data = [
        {
            "meter_id": generate_meter_id(),
            "energy_type": generate_energy_type(),
            "consumption_value": generate_consumption_value(),
            "unit": generate_unit(),
            "billing_cycle": generate_billing_cycle(),
            "customer_id": generate_customer_id(),
            "city": generate_city(),
            "country": generate_country(),
            "meter_read_date": generate_meter_read_date(),
            "tariff_rate": generate_tariff_rate(),
            "peak_usage": generate_peak_usage(),
            "off_peak_usage": generate_off_peak_usage(),
            "total_cost": generate_total_cost(),
            "provider_name": generate_provider_name(),
            "energy_efficiency_rating": generate_energy_efficiency_rating(),
            "usage_category": generate_usage_category(),
            "power_factor": generate_power_factor(),
            "carbon_emissions": generate_carbon_emissions(),
            "invoice_number": generate_invoice_number(),
            "payment_status": generate_payment_status(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_energy_consumption_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_energy_consumption_data')
# def download_energy_consumption_data():
#     df = generate_energy_consumption_data(500000)
#     file_path = "energy_consumption_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
