from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_match_id():
    return fake.uuid4()

def generate_sport_type():
    return fake.random_element(elements=["Football", "Basketball", "Tennis", "Cricket", "Baseball", "Hockey", "Soccer", "Rugby"])

def generate_team_1():
    return fake.company()

def generate_team_2():
    return fake.company()

def generate_match_date():
    return fake.date_between(start_date='-1y', end_date='today')

def generate_match_location():
    return fake.city()

def generate_score_team_1():
    return fake.random_number(digits=2)

def generate_score_team_2():
    return fake.random_number(digits=2)

def generate_winner():
    return fake.random_element(elements=["Team 1", "Team 2", "Draw"])

def generate_referee_name():
    return fake.name()

def generate_duration():
    return fake.random_int(min=60, max=180)

def generate_tournament_name():
    return fake.catch_phrase()

def generate_player_of_the_match():
    return fake.name()

def generate_attendance():
    return fake.random_number(digits=5)

def generate_ticket_price():
    return round(fake.pydecimal(left_digits=3, right_digits=2, positive=True), 2)

def generate_weather_conditions():
    return fake.random_element(elements=["Sunny", "Rainy", "Cloudy", "Windy", "Snowy"])

def generate_broadcast_channel():
    return fake.company()

def generate_sponsor_name():
    return fake.company()

def generate_injury_report():
    return fake.random_element(elements=["None", "Minor", "Severe"])

def generate_match_status():
    return fake.random_element(elements=["Completed", "Ongoing", "Scheduled"])

def generate_sports_data(num_records=100):
    data = [
        {
            "match_id": generate_match_id(),
            "sport_type": generate_sport_type(),
            "team_1": generate_team_1(),
            "team_2": generate_team_2(),
            "match_date": generate_match_date(),
            "match_location": generate_match_location(),
            "score_team_1": generate_score_team_1(),
            "score_team_2": generate_score_team_2(),
            "winner": generate_winner(),
            "referee_name": generate_referee_name(),
            "duration": generate_duration(),
            "tournament_name": generate_tournament_name(),
            "player_of_the_match": generate_player_of_the_match(),
            "attendance": generate_attendance(),
            "ticket_price": generate_ticket_price(),
            "weather_conditions": generate_weather_conditions(),
            "broadcast_channel": generate_broadcast_channel(),
            "sponsor_name": generate_sponsor_name(),
            "injury_report": generate_injury_report(),
            "match_status": generate_match_status(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_sports_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_sports_data')
# def download_sports_data():
#     df = generate_sports_data(500000)
#     file_path = "sports_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
