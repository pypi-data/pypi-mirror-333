from faker import Faker
import pandas as pd
from flask import Flask, send_file
import io

fake = Faker()
app = Flask(__name__)

def generate_animal_id():
    return fake.uuid4()

def generate_species():
    return fake.random_element(elements=["Cattle", "Sheep", "Goat", "Pig", "Chicken", "Horse"])

def generate_breed():
    return fake.word().title() + " Breed"

def generate_birth_date():
    return fake.date_of_birth(minimum_age=0, maximum_age=10)

def generate_weight():
    return round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)

def generate_health_status():
    return fake.random_element(elements=["Healthy", "Sick", "Recovered", "Under Observation"])

def generate_farm_location():
    return fake.city() + ", " + fake.country()

def generate_owner_name():
    return fake.name()

def generate_feed_type():
    return fake.random_element(elements=["Grass", "Grain", "Silage", "Mixed Feed"])

def generate_veterinary_checkup_date():
    return fake.date_this_year()

def generate_milk_production():
    return round(fake.pyfloat(left_digits=2, right_digits=1, positive=True, max_value=50.0), 1)

def generate_reproductive_status():
    return fake.random_element(elements=["Pregnant", "Lactating", "Neutered", "Fertile"])

def generate_tag_number():
    return fake.bothify("TAG-###-????")

def generate_vaccination_status():
    return fake.random_element(elements=["Up-to-date", "Pending", "Overdue"])

def generate_transportation_method():
    return fake.random_element(elements=["Truck", "Train", "Air", "Ship"])

def generate_destination():
    return fake.city() + ", " + fake.country()

def generate_inspection_result():
    return fake.random_element(elements=["Passed", "Failed", "Pending"])

def generate_sales_price():
    return round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2)

def generate_livestock_data(num_records=100):
    data = [{
        "animal_id": generate_animal_id(),
        "species": generate_species(),
        "breed": generate_breed(),
        "birth_date": generate_birth_date(),
        "weight": generate_weight(),
        "health_status": generate_health_status(),
        "farm_location": generate_farm_location(),
        "owner_name": generate_owner_name(),
        "feed_type": generate_feed_type(),
        "veterinary_checkup_date": generate_veterinary_checkup_date(),
        "milk_production": generate_milk_production(),
        "reproductive_status": generate_reproductive_status(),
        "tag_number": generate_tag_number(),
        "vaccination_status": generate_vaccination_status(),
        "transportation_method": generate_transportation_method(),
        "destination": generate_destination(),
        "inspection_result": generate_inspection_result(),
        "sales_price": generate_sales_price()
    } for _ in range(num_records)]

    return pd.DataFrame(data)

# @app.route('/download_livestock_data')
# def download_livestock_data():
#     df = generate_livestock_data(num_records=500000)
#     output = io.BytesIO()
#     df.to_csv(output, index=False)
#     output.seek(0)

#     return send_file(output, mimetype='text/csv', as_attachment=True, download_name='livestock_data.csv')

# if __name__ == '__main__':
#     sample_df = generate_livestock_data(10)
#     print(sample_df.head(10))
#     app.run(debug=True)
