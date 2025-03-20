from faker import Faker
import pandas as pd
from flask import Flask, send_file
import io

fake = Faker()
app = Flask(__name__)

def generate_farm_id():
    return fake.uuid4()

def generate_crop_type():
    return fake.random_element(elements=["Wheat", "Corn", "Rice", "Soybean", "Barley", "Cotton"])

def generate_yield_quantity_kg():
    return round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2)

def generate_harvest_date():
    return fake.date_this_year()

def generate_soil_type():
    return fake.random_element(elements=["Sandy", "Clay", "Silt", "Loam", "Peat"])

def generate_irrigation_method():
    return fake.random_element(elements=["Drip", "Flood", "Sprinkler", "Manual"])

def generate_fertilizer_used():
    return fake.random_element(elements=["Nitrogen", "Phosphorus", "Potassium", "Organic", "None"])

def generate_weather_condition():
    return fake.random_element(elements=["Sunny", "Rainy", "Cloudy", "Stormy", "Windy"])

def generate_field_size_hectares():
    return round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)

def generate_pesticide_applied():
    return fake.boolean(chance_of_getting_true=40)

def generate_farmer_name():
    return fake.name()

def generate_farm_location():
    return fake.city()

def generate_seed_variety():
    return fake.word()

def generate_crop_health():
    return fake.random_element(elements=["Healthy", "Diseased", "Pest-Infested", "Drought-Affected"])

def generate_market_price_per_kg():
    return round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)

def generate_organic_certified():
    return fake.boolean(chance_of_getting_true=30)

def generate_machinery_used():
    return fake.random_element(elements=["Tractor", "Combine Harvester", "Plow", "Seeder", "Manual"])

def generate_water_source():
    return fake.random_element(elements=["Well", "River", "Rainwater", "Irrigation Canal"])

def generate_planting_date():
    return fake.date_this_year()

def generate_crop_rotation():
    return fake.boolean(chance_of_getting_true=50)

def generate_agricultural_data(num_records=100):
    data = [{
        "farm_id": generate_farm_id(),
        "crop_type": generate_crop_type(),
        "yield_quantity_kg": generate_yield_quantity_kg(),
        "harvest_date": generate_harvest_date(),
        "soil_type": generate_soil_type(),
        "irrigation_method": generate_irrigation_method(),
        "fertilizer_used": generate_fertilizer_used(),
        "weather_condition": generate_weather_condition(),
        "field_size_hectares": generate_field_size_hectares(),
        "pesticide_applied": generate_pesticide_applied(),
        "farmer_name": generate_farmer_name(),
        "farm_location": generate_farm_location(),
        "seed_variety": generate_seed_variety(),
        "crop_health": generate_crop_health(),
        "market_price_per_kg": generate_market_price_per_kg(),
        "organic_certified": generate_organic_certified(),
        "machinery_used": generate_machinery_used(),
        "water_source": generate_water_source(),
        "planting_date": generate_planting_date(),
        "crop_rotation": generate_crop_rotation()
    } for _ in range(num_records)]

    return pd.DataFrame(data)

# @app.route('/download_agricultural_data')
# def download_agricultural_data():
#     df = generate_agricultural_data(num_records=500000)
#     output = io.BytesIO()
#     df.to_csv(output, index=False)
#     output.seek(0)

#     return send_file(output, mimetype='text/csv', as_attachment=True, download_name='agricultural_data.csv')

# if __name__ == '__main__':
#     sample_df = generate_agricultural_data(10)
#     print(sample_df.head(10))
#     app.run(debug=True)
