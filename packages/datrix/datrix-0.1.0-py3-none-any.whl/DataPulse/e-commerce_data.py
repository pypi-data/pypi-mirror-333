from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_order_id():
    return fake.uuid4()

def generate_customer_id():
    return fake.uuid4()

def generate_product_name():
    return fake.word().capitalize() + " " + fake.word().capitalize()

def generate_category():
    return fake.random_element(elements=["Electronics", "Clothing", "Home & Kitchen", "Beauty", "Books", "Sports"])

def generate_price():
    return round(fake.pydecimal(left_digits=4, right_digits=2, positive=True), 2)

def generate_order_date():
    return fake.date_between(start_date='-1y', end_date='today')

def generate_shipping_date():
    return fake.date_between(start_date='-30d', end_date='today')

def generate_payment_method():
    return fake.random_element(elements=["Credit Card", "Debit Card", "PayPal", "Bank Transfer", "Cash on Delivery"])

def generate_order_status():
    return fake.random_element(elements=["Processing", "Shipped", "Delivered", "Cancelled", "Returned"])

def generate_quantity():
    return fake.random_int(min=1, max=10)

def generate_discount():
    return round(fake.pyfloat(left_digits=2, right_digits=2, positive=True, min_value=0.0, max_value=50.0), 2)

def generate_shipping_cost():
    return round(fake.pydecimal(left_digits=3, right_digits=2, positive=True), 2)

def generate_total_amount():
    return round(fake.pydecimal(left_digits=5, right_digits=2, positive=True), 2)

def generate_customer_name():
    return fake.name()

def generate_customer_email():
    return fake.email()

def generate_delivery_address():
    return fake.address()

def generate_tracking_id():
    return fake.bothify(text='??###-#####')

def generate_review_rating():
    return fake.random_int(min=1, max=5)

def generate_review_comment():
    return fake.sentence(nb_words=12)

def generate_return_reason():
    return fake.random_element(elements=["Defective", "Wrong Item", "Size Issue", "Changed Mind", "Other"])

def generate_ecommerce_data(num_records=100):
    data = []
    for _ in range(num_records):
        data.append({
            "order_id": generate_order_id(),
            "customer_id": generate_customer_id(),
            "product_name": generate_product_name(),
            "category": generate_category(),
            "price": generate_price(),
            "order_date": generate_order_date(),
            "shipping_date": generate_shipping_date(),
            "payment_method": generate_payment_method(),
            "order_status": generate_order_status(),
            "quantity": generate_quantity(),
            "discount": generate_discount(),
            "shipping_cost": generate_shipping_cost(),
            "total_amount": generate_total_amount(),
            "customer_name": generate_customer_name(),
            "customer_email": generate_customer_email(),
            "delivery_address": generate_delivery_address(),
            "tracking_id": generate_tracking_id(),
            "review_rating": generate_review_rating(),
            "review_comment": generate_review_comment(),
            "return_reason": generate_return_reason(),
        })

    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_ecommerce_data(10)
print(df_sample.head())

# # Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_ecommerce_data')
# def download_ecommerce_data():
#     df = generate_ecommerce_data(500000)
#     file_path = "ecommerce_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
