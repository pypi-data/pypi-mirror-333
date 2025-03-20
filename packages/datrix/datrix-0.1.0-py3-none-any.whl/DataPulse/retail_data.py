from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_product_id():
    return fake.uuid4()

def generate_product_name():
    return fake.word().title() + " " + fake.word().title()

def generate_category():
    return fake.random_element(elements=["Electronics", "Clothing", "Home & Garden", "Toys", "Groceries", "Beauty"])

def generate_price():
    return round(fake.pydecimal(left_digits=3, right_digits=2, positive=True), 2)

def generate_discount():
    return round(fake.pydecimal(left_digits=2, right_digits=2, positive=True), 2)

def generate_stock_quantity():
    return fake.random_int(min=0, max=1000)

def generate_supplier():
    return fake.company()

def generate_brand():
    return fake.company_suffix()

def generate_sku():
    return fake.bothify(text='??-#####')

def generate_store_location():
    return fake.city()

def generate_sale_date():
    return fake.date_between(start_date='-1y', end_date='today')

def generate_customer_id():
    return fake.uuid4()

def generate_payment_method():
    return fake.random_element(elements=["Credit Card", "Debit Card", "Cash", "Online Payment"])

def generate_return_status():
    return fake.random_element(elements=["Not Returned", "Returned", "Exchange"])

def generate_review_score():
    return fake.random_int(min=1, max=5)

def generate_shipping_cost():
    return round(fake.pydecimal(left_digits=2, right_digits=2, positive=True), 2)

def generate_tax_amount():
    return round(fake.pydecimal(left_digits=2, right_digits=2, positive=True), 2)

def generate_delivery_status():
    return fake.random_element(elements=["Delivered", "In Transit", "Pending", "Cancelled"])

def generate_warranty_period():
    return fake.random_element(elements=["6 months", "1 year", "2 years", "No Warranty"])

def generate_sales_channel():
    return fake.random_element(elements=["Online", "In-Store", "Wholesale"])

def generate_retail_data(num_records=100):
    data = [
        {
            "product_id": generate_product_id(),
            "product_name": generate_product_name(),
            "category": generate_category(),
            "price": generate_price(),
            "discount": generate_discount(),
            "stock_quantity": generate_stock_quantity(),
            "supplier": generate_supplier(),
            "brand": generate_brand(),
            "sku": generate_sku(),
            "store_location": generate_store_location(),
            "sale_date": generate_sale_date(),
            "customer_id": generate_customer_id(),
            "payment_method": generate_payment_method(),
            "return_status": generate_return_status(),
            "review_score": generate_review_score(),
            "shipping_cost": generate_shipping_cost(),
            "tax_amount": generate_tax_amount(),
            "delivery_status": generate_delivery_status(),
            "warranty_period": generate_warranty_period(),
            "sales_channel": generate_sales_channel(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_retail_data(10)
print(df_sample.head())

# # Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_retail_data')
# def download_retail_data():
#     df = generate_retail_data(500000)
#     file_path = "retail_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
