from faker import Faker
import pandas as pd
from flask import Flask, send_file
import io

fake = Faker()
app = Flask(__name__)

def generate_accident_id():
    return fake.uuid4()

def generate_accident_date():
    return fake.date_this_decade()

def generate_accident_time():
    return fake.time()

def generate_location():
    return fake.address()

def generate_vehicle_type():
    return fake.random_element(elements=["Car", "Truck", "Motorcycle", "Bicycle", "Bus"])

def generate_driver_age():
    return fake.random_int(min=18, max=80)

def generate_weather_condition():
    return fake.random_element(elements=["Clear", "Rainy", "Snowy", "Foggy", "Windy"])

def generate_cause_of_accident():
    return fake.random_element(elements=["Speeding", "Distracted Driving", "Drunk Driving", "Weather", "Mechanical Failure"])

def generate_injury_severity():
    return fake.random_element(elements=["None", "Minor", "Moderate", "Severe", "Fatal"])

def generate_number_of_vehicles():
    return fake.random_int(min=1, max=5)

def generate_number_of_injuries():
    return fake.random_int(min=0, max=10)

def generate_number_of_fatalities():
    return fake.random_int(min=0, max=5)

def generate_accident_description():
    return fake.sentence()

def generate_road_type():
    return fake.random_element(elements=["Highway", "City Road", "Rural Road", "Residential Area"])

def generate_police_report_number():
    return fake.bothify("PR###-#####")

def generate_hit_and_run():
    return fake.boolean()

def generate_alcohol_involved():
    return fake.boolean()

def generate_speed_at_time():
    return fake.random_int(min=20, max=150)

def generate_damage_estimation():
    return round(fake.pydecimal(left_digits=5, right_digits=2, positive=True), 2)

def generate_tow_required():
    return fake.boolean()

def generate_traffic_accident_data(num_records=100):
    data = [{
        "accident_id": generate_accident_id(),
        "accident_date": generate_accident_date(),
        "accident_time": generate_accident_time(),
        "location": generate_location(),
        "vehicle_type": generate_vehicle_type(),
        "driver_age": generate_driver_age(),
        "weather_condition": generate_weather_condition(),
        "cause_of_accident": generate_cause_of_accident(),
        "injury_severity": generate_injury_severity(),
        "number_of_vehicles": generate_number_of_vehicles(),
        "number_of_injuries": generate_number_of_injuries(),
        "number_of_fatalities": generate_number_of_fatalities(),
        "accident_description": generate_accident_description(),
        "road_type": generate_road_type(),
        "police_report_number": generate_police_report_number(),
        "hit_and_run": generate_hit_and_run(),
        "alcohol_involved": generate_alcohol_involved(),
        "speed_at_time": generate_speed_at_time(),
        "damage_estimation": generate_damage_estimation(),
        "tow_required": generate_tow_required()
    } for _ in range(num_records)]

    return pd.DataFrame(data)

# @app.route('/download_traffic_accident_data')
# def download_traffic_accident_data():
#     df = generate_traffic_accident_data(num_records=500000)
#     output = io.BytesIO()
#     df.to_csv(output, index=False)
#     output.seek(0)

#     return send_file(output, mimetype='text/csv', as_attachment=True, download_name='traffic_accident_data.csv')

# if __name__ == '__main__':
#     sample_df = generate_traffic_accident_data(10)
#     print(sample_df.head(10))
#     app.run(debug=True)