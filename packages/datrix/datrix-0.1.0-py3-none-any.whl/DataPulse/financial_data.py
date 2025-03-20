from faker import Faker
import pandas as pd

fake = Faker()

def generate_transaction_id():
    return fake.uuid4()

def generate_amount():
    return round(fake.pydecimal(left_digits=5, right_digits=2, positive=True), 2)

def generate_currency():
    return fake.currency_code()

def generate_transaction_date():
    return fake.date_time_this_year()

def generate_payment_method():
    return fake.random_element(elements=["Credit Card", "Debit Card", "Bank Transfer"])

def generate_account_number():
    return fake.iban()

def generate_customer_id():
    return fake.uuid4()

def generate_merchant_name():
    return fake.company()

def generate_transaction_status():
    return fake.random_element(elements=["Completed", "Pending", "Failed"])

def generate_country():
    return fake.country()

def generate_city():
    return fake.city()

def generate_zip_code():
    return fake.zipcode()

def generate_reference_number():
    return fake.bothify("??###-###")

def generate_card_type():
    return fake.credit_card_provider()

def generate_card_expiry():
    return fake.credit_card_expire()

def generate_fraud_flag():
    return fake.boolean(chance_of_getting_true=10)

def generate_exchange_rate():
    return round(fake.pyfloat(left_digits=1, right_digits=4, positive=True), 4)

def generate_fee_amount():
    return round(fake.pydecimal(left_digits=3, right_digits=2), 2)

def generate_refund_status():
    return fake.random_element(elements=["None", "Partial", "Full"])

def generate_branch_code():
    return fake.random_number(digits=5)

def generate_data(num_records=100):
    data = [{
        "transaction_id": generate_transaction_id(),
        "amount": generate_amount(),
        "currency": generate_currency(),
        "transaction_date": generate_transaction_date(),
        "payment_method": generate_payment_method(),
        "account_number": generate_account_number(),
        "customer_id": generate_customer_id(),
        "merchant_name": generate_merchant_name(),
        "transaction_status": generate_transaction_status(),
        "country": generate_country(),
        "city": generate_city(),
        "zip_code": generate_zip_code(),
        "reference_number": generate_reference_number(),
        "card_type": generate_card_type(),
        "card_expiry": generate_card_expiry(),
        "fraud_flag": generate_fraud_flag(),
        "exchange_rate": generate_exchange_rate(),
        "fee_amount": generate_fee_amount(),
        "refund_status": generate_refund_status(),
        "branch_code": generate_branch_code(),
    } for _ in range(num_records)]

    return pd.DataFrame(data)


