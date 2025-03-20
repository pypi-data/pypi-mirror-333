from faker import Faker
import pandas as pd
from flask import Flask, send_file
import io

fake = Faker()
app = Flask(__name__)

def generate_copyright_id():
    return fake.uuid4()

def generate_title():
    return fake.catch_phrase()

def generate_owner_name():
    return fake.name()

def generate_registration_date():
    return fake.date_this_decade()

def generate_expiration_date():
    return fake.date_between(start_date='+10y', end_date='+20y')

def generate_work_type():
    return fake.random_element(elements=["Literary", "Musical", "Artistic", "Software", "Broadcast"])

def generate_jurisdiction():
    return fake.country()

def generate_infringement_cases():
    return fake.random_int(min=0, max=20)

def generate_license_type():
    return fake.random_element(elements=["Exclusive", "Non-exclusive", "Public Domain"])

def generate_license_fee():
    return round(fake.pydecimal(left_digits=6, right_digits=2, positive=True), 2)

def generate_ip_status():
    return fake.random_element(elements=["Active", "Expired", "Pending", "Disputed"])

def generate_renewal_flag():
    return fake.boolean()

def generate_application_number():
    return fake.bothify("APP###-#####")

def generate_grant_number():
    return fake.bothify("GRN###-#####")

def generate_publication_date():
    return fake.date_this_decade()

def generate_court_decision():
    return fake.random_element(elements=["Upheld", "Overturned", "Settled", "Pending"])

def generate_agent_name():
    return fake.name()

def generate_agency_name():
    return fake.company()

def generate_related_works():
    return fake.random_int(min=0, max=10)

def generate_commercial_use():
    return fake.boolean()

def generate_copyright_data(num_records=100):
    data = [{
        "copyright_id": generate_copyright_id(),
        "title": generate_title(),
        "owner_name": generate_owner_name(),
        "registration_date": generate_registration_date(),
        "expiration_date": generate_expiration_date(),
        "work_type": generate_work_type(),
        "jurisdiction": generate_jurisdiction(),
        "infringement_cases": generate_infringement_cases(),
        "license_type": generate_license_type(),
        "license_fee": generate_license_fee(),
        "ip_status": generate_ip_status(),
        "renewal_flag": generate_renewal_flag(),
        "application_number": generate_application_number(),
        "grant_number": generate_grant_number(),
        "publication_date": generate_publication_date(),
        "court_decision": generate_court_decision(),
        "agent_name": generate_agent_name(),
        "agency_name": generate_agency_name(),
        "related_works": generate_related_works(),
        "commercial_use": generate_commercial_use()
    } for _ in range(num_records)]

    return pd.DataFrame(data)

# @app.route('/download_copyright_data')
# def download_copyright_data():
#     df = generate_copyright_data(num_records=500000)
#     output = io.BytesIO()
#     df.to_csv(output, index=False)
#     output.seek(0)

#     return send_file(output, mimetype='text/csv', as_attachment=True, download_name='copyright_data.csv')

# if __name__ == '__main__':
#     sample_df = generate_copyright_data(10)
#     print(sample_df.head(10))
#     app.run(debug=True)
