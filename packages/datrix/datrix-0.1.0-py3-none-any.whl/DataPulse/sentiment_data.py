from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_text_id():
    return fake.uuid4()

def generate_text():
    return fake.sentence(nb_words=20)

def generate_sentiment():
    return fake.random_element(elements=["Positive", "Negative", "Neutral"])

def generate_sentiment_score():
    return round(fake.pyfloat(left_digits=1, right_digits=2, positive=True, max_value=1.0), 2)

def generate_language():
    return fake.random_element(elements=["English", "Spanish", "French", "German", "Chinese"])

def generate_source():
    return fake.random_element(elements=["Social Media", "News", "Product Review", "Customer Feedback", "Survey"])

def generate_timestamp():
    return fake.date_time_this_year()

def generate_author():
    return fake.name()

def generate_topic():
    return fake.random_element(elements=["Politics", "Technology", "Health", "Sports", "Entertainment"])

def generate_location():
    return fake.city()

def generate_emotion():
    return fake.random_element(elements=["Happy", "Sad", "Angry", "Excited", "Frustrated"])

def generate_device_type():
    return fake.random_element(elements=["Mobile", "Desktop", "Tablet"])

def generate_platform():
    return fake.random_element(elements=["Twitter", "Facebook", "YouTube", "Instagram", "LinkedIn"])

def generate_url():
    return fake.url()

def generate_keyword():
    return fake.word()

def generate_length_of_text():
    return fake.random_int(min=50, max=500)

def generate_category():
    return fake.random_element(elements=["Positive Review", "Complaint", "Inquiry", "General Feedback"])

def generate_language_confidence():
    return round(fake.pyfloat(left_digits=1, right_digits=2, positive=True, max_value=1.0), 2)

def generate_user_type():
    return fake.random_element(elements=["Registered", "Guest", "Anonymous"])

def generate_sentiment_data(num_records=100):
    data = [
        {
            "text_id": generate_text_id(),
            "text": generate_text(),
            "sentiment": generate_sentiment(),
            "sentiment_score": generate_sentiment_score(),
            "language": generate_language(),
            "source": generate_source(),
            "timestamp": generate_timestamp(),
            "author": generate_author(),
            "topic": generate_topic(),
            "location": generate_location(),
            "emotion": generate_emotion(),
            "device_type": generate_device_type(),
            "platform": generate_platform(),
            "url": generate_url(),
            "keyword": generate_keyword(),
            "length_of_text": generate_length_of_text(),
            "category": generate_category(),
            "language_confidence": generate_language_confidence(),
            "user_type": generate_user_type(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_sentiment_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_sentiment_data')
# def download_sentiment_data():
#     df = generate_sentiment_data(500000)
#     file_path = "sentiment_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
