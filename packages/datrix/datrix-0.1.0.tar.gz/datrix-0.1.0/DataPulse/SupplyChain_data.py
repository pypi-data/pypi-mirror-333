from faker import Faker
import pandas as pd
from flask import Flask, send_file

fake = Faker()

def generate_order_id():
    return fake.uuid4()

def generate_product_name():
    return fake.word()

def generate_supplier_name():
    return fake.company()

def generate_order_date():
    return fake.date_this_year()

def generate_delivery_date():
    return fake.date_between(start_date='today', end_date='+30d')

def generate_quantity():
    return fake.random_int(min=1, max=1000)

def generate_unit_price():
    return round(fake.pydecimal(left_digits=4, right_digits=2, positive=True), 2)

def generate_total_cost():
    return round(fake.pydecimal(left_digits=6, right_digits=2, positive=True), 2)

def generate_order_status():
    return fake.random_element(elements=["Pending", "Shipped", "Delivered", "Cancelled"])

def generate_warehouse_location():
    return fake.city()

def generate_transport_mode():
    return fake.random_element(elements=["Air", "Sea", "Rail", "Road"])

def generate_tracking_number():
    return fake.bothify(text="??###-####")

def generate_inventory_level():
    return fake.random_int(min=0, max=10000)

def generate_return_status():
    return fake.random_element(elements=["No Return", "In Process", "Completed"])

def generate_dispatch_center():
    return fake.city()

def generate_shipping_cost():
    return round(fake.pydecimal(left_digits=3, right_digits=2, positive=True), 2)

def generate_order_priority():
    return fake.random_element(elements=["High", "Medium", "Low"])

def generate_supplier_contact():
    return fake.phone_number()

def generate_carrier_name():
    return fake.company()

def generate_supply_chain_data(num_records=100):
    data = [
        {
            "order_id": generate_order_id(),
            "product_name": generate_product_name(),
            "supplier_name": generate_supplier_name(),
            "order_date": generate_order_date(),
            "delivery_date": generate_delivery_date(),
            "quantity": generate_quantity(),
            "unit_price": generate_unit_price(),
            "total_cost": generate_total_cost(),
            "order_status": generate_order_status(),
            "warehouse_location": generate_warehouse_location(),
            "transport_mode": generate_transport_mode(),
            "tracking_number": generate_tracking_number(),
            "inventory_level": generate_inventory_level(),
            "return_status": generate_return_status(),
            "dispatch_center": generate_dispatch_center(),
            "shipping_cost": generate_shipping_cost(),
            "order_priority": generate_order_priority(),
            "supplier_contact": generate_supplier_contact(),
            "carrier_name": generate_carrier_name(),
        } for _ in range(num_records)
    ]
    return pd.DataFrame(data)

# Display sample DataFrame
df_sample = generate_supply_chain_data(10)
print(df_sample.head())

# Flask app to download large datasets
# app = Flask(__name__)

# @app.route('/download_supply_chain_data')
# def download_supply_chain_data():
#     df = generate_supply_chain_data(500000)
#     file_path = "supply_chain_data.csv"
#     df.to_csv(file_path, index=False)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
