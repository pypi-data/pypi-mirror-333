from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_patient_id():
    return fake.uuid4()

def generate_patient_name():
    return fake.name()

def generate_age():
    return fake.random_int(min=0, max=100)

def generate_gender():
    return fake.random_element(elements=["Male", "Female", "Other"])

def generate_diagnosis():
    return fake.random_element(elements=["Hypertension", "Diabetes", "Asthma", "Flu", "Migraine"])

def generate_admission_date():
    return fake.date_this_decade()

def generate_discharge_date():
    return fake.date_between(start_date='-1y', end_date='today')

def generate_doctor_name():
    return fake.name()

def generate_department():
    return fake.random_element(elements=["Cardiology", "Neurology", "Orthopedics", "Pediatrics", "General Medicine"])

def generate_medication():
    return fake.random_element(elements=["Aspirin", "Metformin", "Lisinopril", "Ibuprofen", "Amoxicillin"])

def generate_allergies():
    return fake.random_element(elements=["None", "Penicillin", "Peanuts", "Shellfish", "Latex"])

def generate_blood_type():
    return fake.random_element(elements=["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])

def generate_insurance_provider():
    return fake.company()

def generate_policy_number():
    return fake.bothify("??###-###-####")

def generate_emergency_contact():
    return fake.phone_number()

def generate_visit_type():
    return fake.random_element(elements=["Inpatient", "Outpatient", "Emergency"])

def generate_procedure():
    return fake.random_element(elements=["MRI", "CT Scan", "X-Ray", "Blood Test", "Surgery"])

def generate_hospital_name():
    return fake.company()

def generate_billing_amount():
    return round(fake.pydecimal(left_digits=5, right_digits=2, positive=True), 2)

def generate_followup_date():
    return fake.date_between(start_date='today', end_date='+6m')

def generate_medical_data(num_records=100):
    data = []
    for _ in range(num_records):
        data.append({
            "patient_id": generate_patient_id(),
            "patient_name": generate_patient_name(),
            "age": generate_age(),
            "gender": generate_gender(),
            "diagnosis": generate_diagnosis(),
            "admission_date": generate_admission_date(),
            "discharge_date": generate_discharge_date(),
            "doctor_name": generate_doctor_name(),
            "department": generate_department(),
            "medication": generate_medication(),
            "allergies": generate_allergies(),
            "blood_type": generate_blood_type(),
            "insurance_provider": generate_insurance_provider(),
            "policy_number": generate_policy_number(),
            "emergency_contact": generate_emergency_contact(),
            "visit_type": generate_visit_type(),
            "procedure": generate_procedure(),
            "hospital_name": generate_hospital_name(),
            "billing_amount": generate_billing_amount(),
            "followup_date": generate_followup_date(),
        })

    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_medical_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_medical_data')
# def download_medical_data():
#     df = generate_medical_data(500000)
#     file_path = "medical_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
