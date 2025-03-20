from faker import Faker
import pandas as pd
from flask import Flask, send_file
import io

fake = Faker()
app = Flask(__name__)

def generate_banking_transaction_data(num_records=100):
    data = [{
        "transaction_id": fake.uuid4(),
        "account_number": fake.iban(),
        "transaction_date": fake.date_time_this_year(),
        "amount": round(fake.pydecimal(left_digits=6, right_digits=2, positive=True), 2),
        "currency": fake.currency_code(),
        "transaction_type": fake.random_element(elements=["Deposit", "Withdrawal", "Transfer", "Payment"]),
        "account_balance": round(fake.pydecimal(left_digits=7, right_digits=2, positive=True), 2),
        "customer_id": fake.uuid4(),
        "branch_code": fake.random_number(digits=5),
        "transaction_status": fake.random_element(elements=["Completed", "Pending", "Failed"]),
        "merchant_name": fake.company(),
        "payment_method": fake.random_element(elements=["Online", "ATM", "In-Branch", "Mobile"]),
        "card_number": fake.credit_card_number(),
        "card_type": fake.credit_card_provider(),
        "authorization_code": fake.bothify(text='??###-###'),
        "reference_number": fake.bothify(text='?????-#####'),
        "customer_name": fake.name(),
        "customer_email": fake.email(),
        "fraud_flag": fake.boolean(chance_of_getting_true=5),
        "fee_amount": round(fake.pydecimal(left_digits=3, right_digits=2), 2),
        "exchange_rate": round(fake.pyfloat(left_digits=1, right_digits=4, positive=True), 4)
    } for _ in range(num_records)]

    return pd.DataFrame(data)

# @app.route('/download_banking_transaction_data')
# def download_banking_transaction_data():
#     df = generate_banking_transaction_data(num_records=500000)
#     output = io.BytesIO()
#     df.to_csv(output, index=False)
#     output.seek(0)

#     return send_file(output, mimetype='text/csv', as_attachment=True, download_name='banking_transaction_data.csv')

# if __name__ == '__main__':
#     sample_df = generate_banking_transaction_data(10)
#     print(sample_df.head(10))
#     app.run(debug=True)
