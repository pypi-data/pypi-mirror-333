from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_user_id():
    return fake.uuid4()

def generate_fingerprint_hash():
    return fake.sha256()

def generate_face_id():
    return fake.sha256()

def generate_iris_scan():
    return fake.sha256()

def generate_voice_sample():
    return fake.random_element(elements=["Male", "Female", "Neutral"])

def generate_hand_geometry():
    return fake.sha256()

def generate_retina_scan():
    return fake.sha256()

def generate_signature_pattern():
    return fake.sha256()

def generate_dna_sequence():
    return fake.sha256()

def generate_gait_pattern():
    return fake.sha256()

def generate_keystroke_dynamics():
    return fake.sha256()

def generate_palm_vein_pattern():
    return fake.sha256()

def generate_ear_shape():
    return fake.random_element(elements=["Round", "Oval", "Pointed"])

def generate_skin_texture():
    return fake.random_element(elements=["Smooth", "Rough", "Scarred"])

def generate_facial_landmarks():
    return fake.random_element(elements=["High Cheekbones", "Wide Jaw", "Pointed Chin"])

def generate_voice_pitch():
    return round(fake.pyfloat(left_digits=3, right_digits=2, positive=True, max_value=300.0), 2)

def generate_eye_color():
    return fake.random_element(elements=["Brown", "Blue", "Green", "Hazel", "Gray"])

def generate_body_temperature():
    return round(fake.pyfloat(left_digits=2, right_digits=1, positive=True, max_value=42.0), 1)

def generate_heart_rate():
    return fake.random_int(min=60, max=100)

def generate_blood_pressure():
    return f"{fake.random_int(min=90, max=140)}/{fake.random_int(min=60, max=90)}"

def generate_biometric_data(num_records=100):
    data = [
        {
            "user_id": generate_user_id(),
            "fingerprint_hash": generate_fingerprint_hash(),
            "face_id": generate_face_id(),
            "iris_scan": generate_iris_scan(),
            "voice_sample": generate_voice_sample(),
            "hand_geometry": generate_hand_geometry(),
            "retina_scan": generate_retina_scan(),
            "signature_pattern": generate_signature_pattern(),
            "dna_sequence": generate_dna_sequence(),
            "gait_pattern": generate_gait_pattern(),
            "keystroke_dynamics": generate_keystroke_dynamics(),
            "palm_vein_pattern": generate_palm_vein_pattern(),
            "ear_shape": generate_ear_shape(),
            "skin_texture": generate_skin_texture(),
            "facial_landmarks": generate_facial_landmarks(),
            "voice_pitch": generate_voice_pitch(),
            "eye_color": generate_eye_color(),
            "body_temperature": generate_body_temperature(),
            "heart_rate": generate_heart_rate(),
            "blood_pressure": generate_blood_pressure(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_biometric_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_biometric_data')
# def download_biometric_data():
#     df = generate_biometric_data(500000)
#     file_path = "biometric_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)