from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_campaign_id():
    return fake.uuid4()

def generate_campaign_name():
    return fake.catch_phrase()

def generate_channel():
    return fake.random_element(elements=["Email", "Social Media", "TV", "Radio", "Online Ads", "Print Media"])

def generate_budget():
    return round(fake.pydecimal(left_digits=7, right_digits=2, positive=True), 2)

def generate_start_date():
    return fake.date_between(start_date='-2y', end_date='-1y')

def generate_end_date():
    return fake.date_between(start_date='-1y', end_date='today')

def generate_target_audience():
    return fake.random_element(elements=["Teenagers", "Adults", "Seniors", "Businesses", "Students"])

def generate_conversion_rate():
    return round(fake.pyfloat(left_digits=1, right_digits=4, positive=True, min_value=0.01, max_value=0.5), 4)

def generate_impressions():
    return fake.random_int(min=1000, max=1000000)

def generate_clicks():
    return fake.random_int(min=100, max=100000)

def generate_cost_per_click():
    return round(fake.pydecimal(left_digits=3, right_digits=2, positive=True), 2)

def generate_roi():
    return round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)

def generate_region():
    return fake.random_element(elements=["North America", "Europe", "Asia", "South America", "Africa", "Oceania"])

def generate_ad_type():
    return fake.random_element(elements=["Banner", "Video", "Pop-up", "Native"])

def generate_campaign_status():
    return fake.random_element(elements=["Active", "Completed", "Paused", "Cancelled"])

def generate_lead_count():
    return fake.random_int(min=10, max=10000)

def generate_customer_acquisition_cost():
    return round(fake.pydecimal(left_digits=4, right_digits=2, positive=True), 2)

def generate_engagement_rate():
    return round(fake.pyfloat(left_digits=1, right_digits=4, positive=True, min_value=0.01, max_value=0.3), 4)

def generate_revenue():
    return round(fake.pydecimal(left_digits=8, right_digits=2, positive=True), 2)

def generate_feedback():
    return fake.sentence(nb_words=10)

def generate_marketing_data(num_records=100):
    data = []
    for _ in range(num_records):
        data.append({
            "campaign_id": generate_campaign_id(),
            "campaign_name": generate_campaign_name(),
            "channel": generate_channel(),
            "budget": generate_budget(),
            "start_date": generate_start_date(),
            "end_date": generate_end_date(),
            "target_audience": generate_target_audience(),
            "conversion_rate": generate_conversion_rate(),
            "impressions": generate_impressions(),
            "clicks": generate_clicks(),
            "cost_per_click": generate_cost_per_click(),
            "roi": generate_roi(),
            "region": generate_region(),
            "ad_type": generate_ad_type(),
            "campaign_status": generate_campaign_status(),
            "lead_count": generate_lead_count(),
            "customer_acquisition_cost": generate_customer_acquisition_cost(),
            "engagement_rate": generate_engagement_rate(),
            "revenue": generate_revenue(),
            "feedback": generate_feedback(),
        })

    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_marketing_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_marketing_data')
# def download_marketing_data():
#     df = generate_marketing_data(500000)
#     file_path = "marketing_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)