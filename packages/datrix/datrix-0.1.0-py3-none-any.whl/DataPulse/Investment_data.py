from faker import Faker
import pandas as pd
from flask import Flask, send_file
import io

fake = Faker()
app = Flask(__name__)

def generate_investor_name():
    return fake.name()

def generate_investment_type():
    return fake.random_element(elements=["Stocks", "Bonds", "Real Estate", "Cryptocurrency", "Mutual Funds", "Commodities"])

def generate_investment_amount():
    return round(fake.pydecimal(left_digits=7, right_digits=2, positive=True), 2)

def generate_currency():
    return fake.currency_code()

def generate_investment_date():
    return fake.date_between(start_date="-5y", end_date="today")

def generate_maturity_date():
    return fake.date_between(start_date="today", end_date="+10y")

def generate_risk_level():
    return fake.random_element(elements=["Low", "Medium", "High", "Very High"])

def generate_return_rate():
    return round(fake.pyfloat(left_digits=2, right_digits=2, positive=True, min_value=1, max_value=20), 2)

def generate_broker_name():
    return fake.company()

def generate_investment_status():
    return fake.random_element(elements=["Active", "Closed", "Pending", "Withdrawn"])

def generate_account_id():
    return fake.bothify("ACCT-####-????")

def generate_portfolio_id():
    return fake.bothify("PORT-####")

def generate_market_sector():
    return fake.random_element(elements=["Technology", "Healthcare", "Finance", "Energy", "Consumer Goods"])

def generate_dividends():
    return round(fake.pydecimal(left_digits=5, right_digits=2, positive=True), 2)

def generate_tax_rate():
    return round(fake.pyfloat(left_digits=1, right_digits=2, positive=True, max_value=0.5), 2)

def generate_investment_id():
    return fake.uuid4()

def generate_advisor_name():
    return fake.name()

def generate_geographical_region():
    return fake.country()

def generate_transaction_fee():
    return round(fake.pydecimal(left_digits=4, right_digits=2, positive=True), 2)

def generate_investment_strategy():
    return fake.random_element(elements=["Growth", "Income", "Value", "Balanced", "Aggressive"])

def generate_investment_data(num_records=100):
    data = [{
        "investor_name": generate_investor_name(),
        "investment_type": generate_investment_type(),
        "investment_amount": generate_investment_amount(),
        "currency": generate_currency(),
        "investment_date": generate_investment_date(),
        "maturity_date": generate_maturity_date(),
        "risk_level": generate_risk_level(),
        "return_rate": generate_return_rate(),
        "broker_name": generate_broker_name(),
        "investment_status": generate_investment_status(),
        "account_id": generate_account_id(),
        "portfolio_id": generate_portfolio_id(),
        "market_sector": generate_market_sector(),
        "dividends": generate_dividends(),
        "tax_rate": generate_tax_rate(),
        "investment_id": generate_investment_id(),
        "advisor_name": generate_advisor_name(),
        "geographical_region": generate_geographical_region(),
        "transaction_fee": generate_transaction_fee(),
        "investment_strategy": generate_investment_strategy()
    } for _ in range(num_records)]

    return pd.DataFrame(data)

# @app.route('/download_investment_data')
# def download_investment_data():
#     df = generate_investment_data(num_records=500000)
#     output = io.BytesIO()
#     df.to_csv(output, index=False)
#     output.seek(0)

#     return send_file(output, mimetype='text/csv', as_attachment=True, download_name='investment_data.csv')

# if __name__ == '__main__':
#     sample_df = generate_investment_data(10)
#     print(sample_df.head(10))
#     app.run(debug=True)
