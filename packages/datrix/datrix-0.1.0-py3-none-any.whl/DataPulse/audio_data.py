from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_audio_id():
    return fake.uuid4()

def generate_title():
    return fake.sentence(nb_words=5)

def generate_duration():
    return fake.random_int(min=30, max=7200)  # Duration in seconds (30 secs to 2 hours)

def generate_bitrate():
    return fake.random_int(min=64, max=320)  # Bitrate in kbps

def generate_sample_rate():
    return fake.random_element(elements=[44100, 48000, 96000])  # Sample rate in Hz

def generate_format():
    return fake.random_element(elements=["MP3", "WAV", "FLAC", "AAC", "OGG"])

def generate_codec():
    return fake.random_element(elements=["AAC", "MP3", "Opus", "FLAC", "Vorbis"])

def generate_file_size():
    return round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)  # Size in MB

def generate_artist():
    return fake.name()

def generate_album():
    return fake.sentence(nb_words=3)

def generate_genre():
    return fake.random_element(elements=["Pop", "Rock", "Jazz", "Classical", "Hip-Hop", "Electronic"])

def generate_release_date():
    return fake.date_between(start_date='-10y', end_date='today')

def generate_language():
    return fake.random_element(elements=["English", "Spanish", "French", "German", "Chinese", "Japanese"])

def generate_license_type():
    return fake.random_element(elements=["Creative Commons", "Public Domain", "Standard", "Royalty-Free"])

def generate_publisher():
    return fake.company()

def generate_explicit_content():
    return fake.boolean(chance_of_getting_true=15)

def generate_channels():
    return fake.random_element(elements=["Mono", "Stereo", "Surround 5.1", "Surround 7.1"])

def generate_mood():
    return fake.random_element(elements=["Happy", "Sad", "Relaxing", "Energetic", "Romantic", "Dramatic"])

def generate_listens():
    return fake.random_int(min=0, max=1000000)

def generate_likes():
    return fake.random_int(min=0, max=500000)

def generate_dislikes():
    return fake.random_int(min=0, max=50000)

def generate_audio_data(num_records=100):
    data = [
        {
            "audio_id": generate_audio_id(),
            "title": generate_title(),
            "duration": generate_duration(),
            "bitrate": generate_bitrate(),
            "sample_rate": generate_sample_rate(),
            "format": generate_format(),
            "codec": generate_codec(),
            "file_size": generate_file_size(),
            "artist": generate_artist(),
            "album": generate_album(),
            "genre": generate_genre(),
            "release_date": generate_release_date(),
            "language": generate_language(),
            "license_type": generate_license_type(),
            "publisher": generate_publisher(),
            "explicit_content": generate_explicit_content(),
            "channels": generate_channels(),
            "mood": generate_mood(),
            "listens": generate_listens(),
            "likes": generate_likes(),
            "dislikes": generate_dislikes(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_audio_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_audio_data')
# def download_audio_data():
#     df = generate_audio_data(500000)
#     file_path = "audio_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)