from faker import Faker
import pandas as pd
from flask import Flask, send_file
import io

fake = Faker()
app = Flask(__name__)

def generate_compliance_id():
    return fake.uuid4()

def generate_regulation_name():
    return fake.random_element(elements=["GDPR", "HIPAA", "CCPA", "SOX", "PCI DSS", "FISMA"])

def generate_compliance_status():
    return fake.random_element(elements=["Compliant", "Non-Compliant", "Pending Review"])

def generate_audit_date():
    return fake.date_this_decade()

def generate_auditor_name():
    return fake.name()

def generate_violation_flag():
    return fake.boolean(chance_of_getting_true=20)

def generate_fine_amount():
    return round(fake.pydecimal(left_digits=6, right_digits=2, positive=True), 2)

def generate_policy_version():
    return fake.bothify(text="v##.##")

def generate_department():
    return fake.random_element(elements=["Finance", "HR", "IT", "Legal", "Operations"])

def generate_remediation_status():
    return fake.random_element(elements=["Completed", "In Progress", "Not Started"])

def generate_risk_level():
    return fake.random_element(elements=["Low", "Medium", "High", "Critical"])

def generate_data_type():
    return fake.random_element(elements=["Personal Data", "Financial Data", "Medical Data", "Intellectual Property"])

def generate_review_cycle():
    return fake.random_element(elements=["Annual", "Bi-Annual", "Quarterly", "Monthly"])

def generate_internal_control():
    return fake.bs()

def generate_incident_reported():
    return fake.boolean(chance_of_getting_true=15)

def generate_third_party_involvement():
    return fake.boolean(chance_of_getting_true=25)

def generate_compliance_officer():
    return fake.name()

def generate_documentation_status():
    return fake.random_element(elements=["Complete", "Partial", "Missing"])

def generate_penalty_type():
    return fake.random_element(elements=["Monetary", "Operational", "Reputational"])

def generate_compliance_deadline():
    return fake.date_this_year()

def generate_legal_compliance_data(num_records=100):
    data = [{
        "compliance_id": generate_compliance_id(),
        "regulation_name": generate_regulation_name(),
        "compliance_status": generate_compliance_status(),
        "audit_date": generate_audit_date(),
        "auditor_name": generate_auditor_name(),
        "violation_flag": generate_violation_flag(),
        "fine_amount": generate_fine_amount(),
        "policy_version": generate_policy_version(),
        "department": generate_department(),
        "remediation_status": generate_remediation_status(),
        "risk_level": generate_risk_level(),
        "data_type": generate_data_type(),
        "review_cycle": generate_review_cycle(),
        "internal_control": generate_internal_control(),
        "incident_reported": generate_incident_reported(),
        "third_party_involvement": generate_third_party_involvement(),
        "compliance_officer": generate_compliance_officer(),
        "documentation_status": generate_documentation_status(),
        "penalty_type": generate_penalty_type(),
        "compliance_deadline": generate_compliance_deadline()
    } for _ in range(num_records)]

    return pd.DataFrame(data)

# @app.route('/download_legal_compliance_data')
# def download_legal_compliance_data():
#     df = generate_legal_compliance_data(num_records=500000)
#     output = io.BytesIO()
#     df.to_csv(output, index=False)
#     output.seek(0)

#     return send_file(output, mimetype='text/csv', as_attachment=True, download_name='legal_compliance_data.csv')

# if __name__ == '__main__':
#     sample_df = generate_legal_compliance_data(10)
#     print(sample_df.head(10))
#     app.run(debug=True)
