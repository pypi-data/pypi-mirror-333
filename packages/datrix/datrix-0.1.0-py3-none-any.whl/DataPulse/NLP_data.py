from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_document_id():
    return fake.uuid4()

def generate_text_snippet():
    return fake.text(max_nb_chars=200)

def generate_sentiment():
    return fake.random_element(elements=["Positive", "Negative", "Neutral"])

def generate_language():
    return fake.random_element(elements=["English", "Spanish", "French", "German", "Chinese", "Japanese", "Arabic"])

def generate_author():
    return fake.name()

def generate_publication_date():
    return fake.date_between(start_date='-5y', end_date='today')

def generate_topic():
    return fake.random_element(elements=["Technology", "Health", "Finance", "Education", "Entertainment", "Politics", "Science"])

def generate_text_length():
    return fake.random_int(min=50, max=10000)

def generate_document_type():
    return fake.random_element(elements=["Article", "Review", "Report", "Essay", "Blog Post", "Speech", "Transcript"])

def generate_summary():
    return fake.text(max_nb_chars=300)

def generate_keyword():
    return fake.word()

def generate_readability_score():
    return round(fake.pyfloat(left_digits=2, right_digits=1, positive=True), 1)

def generate_sentiment_score():
    return round(fake.pyfloat(left_digits=1, right_digits=2, positive=True), 2)

def generate_text_source():
    return fake.random_element(elements=["News Website", "Social Media", "Journal", "Blog", "Corporate Report"])

def generate_entity_count():
    return fake.random_int(min=0, max=50)

def generate_named_entities():
    return [fake.company() for _ in range(fake.random_int(min=1, max=5))]

def generate_emotion():
    return fake.random_element(elements=["Joy", "Sadness", "Anger", "Surprise", "Fear", "Neutral"])

def generate_language_model():
    return fake.random_element(elements=["BERT", "GPT", "RoBERTa", "XLNet", "T5"])

def generate_translation():
    return fake.text(max_nb_chars=150)

def generate_source_url():
    return fake.url()

def generate_nlp_data(num_records=100):
    data = [
        {
            "document_id": generate_document_id(),
            "text_snippet": generate_text_snippet(),
            "sentiment": generate_sentiment(),
            "language": generate_language(),
            "author": generate_author(),
            "publication_date": generate_publication_date(),
            "topic": generate_topic(),
            "text_length": generate_text_length(),
            "document_type": generate_document_type(),
            "summary": generate_summary(),
            "keyword": generate_keyword(),
            "readability_score": generate_readability_score(),
            "sentiment_score": generate_sentiment_score(),
            "text_source": generate_text_source(),
            "entity_count": generate_entity_count(),
            "named_entities": generate_named_entities(),
            "emotion": generate_emotion(),
            "language_model": generate_language_model(),
            "translation": generate_translation(),
            "source_url": generate_source_url(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_nlp_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_nlp_data')
# def download_nlp_data():
#     df = generate_nlp_data(500000)
#     file_path = "nlp_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
