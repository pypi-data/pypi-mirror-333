from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_station_id():
    return fake.uuid4()

def generate_station_name():
    return fake.city() + " Weather Station"

def generate_temperature():
    return round(fake.pyfloat(left_digits=2, right_digits=1, positive=False, min_value=-30, max_value=50), 1)

def generate_humidity():
    return fake.random_int(min=10, max=100)

def generate_wind_speed():
    return round(fake.pyfloat(left_digits=2, right_digits=1, positive=True, min_value=0, max_value=50), 1)

def generate_wind_direction():
    return fake.random_element(elements=["N", "NE", "E", "SE", "S", "SW", "W", "NW"])

def generate_precipitation():
    return round(fake.pyfloat(left_digits=2, right_digits=1, positive=True, min_value=0, max_value=300), 1)

def generate_pressure():
    return round(fake.pyfloat(left_digits=4, right_digits=1, positive=True, min_value=900, max_value=1100), 1)

def generate_visibility():
    return round(fake.pyfloat(left_digits=2, right_digits=1, positive=True, min_value=0, max_value=50), 1)

def generate_cloud_cover():
    return fake.random_int(min=0, max=100)

def generate_weather_condition():
    return fake.random_element(elements=["Sunny", "Cloudy", "Rainy", "Stormy", "Snowy", "Foggy", "Windy"])

def generate_recorded_at():
    return fake.date_time_this_year()

def generate_uv_index():
    return fake.random_int(min=0, max=11)

def generate_air_quality_index():
    return fake.random_int(min=0, max=500)

def generate_dew_point():
    return round(fake.pyfloat(left_digits=2, right_digits=1, positive=False, min_value=-20, max_value=30), 1)

def generate_solar_radiation():
    return round(fake.pyfloat(left_digits=3, right_digits=1, positive=True, min_value=0, max_value=1500), 1)

def generate_fog_density():
    return round(fake.pyfloat(left_digits=1, right_digits=2, positive=True, min_value=0, max_value=1), 2)

def generate_rainfall_probability():
    return fake.random_int(min=0, max=100)

def generate_snow_depth():
    return round(fake.pyfloat(left_digits=2, right_digits=1, positive=True, min_value=0, max_value=100), 1)

def generate_weather_data(num_records=100):
    data = []
    for _ in range(num_records):
        data.append({
            "station_id": generate_station_id(),
            "station_name": generate_station_name(),
            "temperature": generate_temperature(),
            "humidity": generate_humidity(),
            "wind_speed": generate_wind_speed(),
            "wind_direction": generate_wind_direction(),
            "precipitation": generate_precipitation(),
            "pressure": generate_pressure(),
            "visibility": generate_visibility(),
            "cloud_cover": generate_cloud_cover(),
            "weather_condition": generate_weather_condition(),
            "recorded_at": generate_recorded_at(),
            "uv_index": generate_uv_index(),
            "air_quality_index": generate_air_quality_index(),
            "dew_point": generate_dew_point(),
            "solar_radiation": generate_solar_radiation(),
            "fog_density": generate_fog_density(),
            "rainfall_probability": generate_rainfall_probability(),
            "snow_depth": generate_snow_depth(),
        })

    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_weather_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_weather_data')
# def download_weather_data():
#     df = generate_weather_data(500000)
#     file_path = "weather_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)