from faker import Faker
import pandas as pd
from flask import Flask, send_file
import io

fake = Faker()
app = Flask(__name__)

def generate_species_name():
    return fake.random_element(elements=["Tiger", "Elephant", "Panda", "Lion", "Rhino", "Gorilla", "Leopard", "Sea Turtle", "Snow Leopard", "Orangutan"])

def generate_habitat():
    return fake.random_element(elements=["Forest", "Grassland", "Wetland", "Desert", "Mountain", "Marine", "Savannah"])

def generate_conservation_status():
    return fake.random_element(elements=["Endangered", "Critically Endangered", "Vulnerable", "Near Threatened", "Least Concern"])

def generate_population_estimate():
    return fake.random_int(min=10, max=10000)

def generate_protected_area():
    return fake.random_element(elements=["National Park", "Wildlife Sanctuary", "Biosphere Reserve", "Marine Reserve", "Game Reserve"])

def generate_location():
    return fake.city() + ", " + fake.country()

def generate_tracking_id():
    return fake.uuid4()

def generate_last_sighting():
    return fake.date_time_this_year()

def generate_researcher_name():
    return fake.name()

def generate_project_name():
    return fake.catch_phrase()

def generate_funding_source():
    return fake.company()

def generate_monitoring_method():
    return fake.random_element(elements=["Camera Trap", "GPS Collar", "Direct Observation", "Acoustic Monitoring", "Satellite Imaging"])

def generate_health_status():
    return fake.random_element(elements=["Healthy", "Injured", "Deceased", "Unknown"])

def generate_species_behavior():
    return fake.random_element(elements=["Migrating", "Foraging", "Resting", "Breeding", "Hunting"])

def generate_climate_condition():
    return fake.random_element(elements=["Sunny", "Rainy", "Snowy", "Cloudy", "Stormy"])

def generate_conservation_agency():
    return fake.company()

def generate_protection_level():
    return fake.random_element(elements=["High", "Medium", "Low"])

def generate_field_station():
    return fake.bothify("FS-##-??")

def generate_species_id():
    return fake.bothify("SP-####")

def generate_wildlife_conservation_data(num_records=100):
    data = [{
        "species_name": generate_species_name(),
        "habitat": generate_habitat(),
        "conservation_status": generate_conservation_status(),
        "population_estimate": generate_population_estimate(),
        "protected_area": generate_protected_area(),
        "location": generate_location(),
        "tracking_id": generate_tracking_id(),
        "last_sighting": generate_last_sighting(),
        "researcher_name": generate_researcher_name(),
        "project_name": generate_project_name(),
        "funding_source": generate_funding_source(),
        "monitoring_method": generate_monitoring_method(),
        "health_status": generate_health_status(),
        "species_behavior": generate_species_behavior(),
        "climate_condition": generate_climate_condition(),
        "conservation_agency": generate_conservation_agency(),
        "protection_level": generate_protection_level(),
        "field_station": generate_field_station(),
        "species_id": generate_species_id()
    } for _ in range(num_records)]

    return pd.DataFrame(data)

# @app.route('/download_wildlife_conservation_data')
# def download_wildlife_conservation_data():
#     df = generate_wildlife_conservation_data(num_records=500000)
#     output = io.BytesIO()
#     df.to_csv(output, index=False)
#     output.seek(0)

#     return send_file(output, mimetype='text/csv', as_attachment=True, download_name='wildlife_conservation_data.csv')

# if __name__ == '__main__':
#     sample_df = generate_wildlife_conservation_data(10)
#     print(sample_df.head(10))
#     app.run(debug=True)
