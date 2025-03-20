from faker import Faker
import pandas as pd
from flask import Flask, send_file
import io

fake = Faker()
app = Flask(__name__)

def generate_device_id():
    return fake.uuid4()

def generate_device_type():
    return fake.random_element(elements=["Router", "Switch", "Firewall", "Server", "Storage", "Access Point"])

def generate_ip_address():
    return fake.ipv4()

def generate_mac_address():
    return fake.mac_address()

def generate_os_version():
    return fake.random_element(elements=["Windows Server 2022", "Ubuntu 20.04", "CentOS 8", "Cisco IOS 15.2", "VMware ESXi 7.0"])

def generate_location():
    return fake.city() + ", " + fake.country()

def generate_status():
    return fake.random_element(elements=["Active", "Inactive", "Maintenance", "Decommissioned"])

def generate_last_update():
    return fake.date_time_this_year()

def generate_owner_name():
    return fake.name()

def generate_serial_number():
    return fake.bothify("SN-####-????")

def generate_rack_location():
    return fake.bothify("R##-U##")

def generate_power_consumption():
    return round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)

def generate_uptime():
    return fake.random_int(min=0, max=365)

def generate_network_speed():
    return fake.random_element(elements=["1Gbps", "10Gbps", "40Gbps", "100Gbps"])

def generate_firmware_version():
    return fake.random_element(elements=["v1.0.3", "v2.2.1", "v3.1.4", "v4.0.2"])

def generate_device_role():
    return fake.random_element(elements=["Core", "Distribution", "Access", "Edge"])

def generate_security_level():
    return fake.random_element(elements=["High", "Medium", "Low"])

def generate_contract_expiry():
    return fake.date_this_decade()

def generate_it_infrastructure_data(num_records=100):
    data = [{
        "device_id": generate_device_id(),
        "device_type": generate_device_type(),
        "ip_address": generate_ip_address(),
        "mac_address": generate_mac_address(),
        "os_version": generate_os_version(),
        "location": generate_location(),
        "status": generate_status(),
        "last_update": generate_last_update(),
        "owner_name": generate_owner_name(),
        "serial_number": generate_serial_number(),
        "rack_location": generate_rack_location(),
        "power_consumption": generate_power_consumption(),
        "uptime": generate_uptime(),
        "network_speed": generate_network_speed(),
        "firmware_version": generate_firmware_version(),
        "device_role": generate_device_role(),
        "security_level": generate_security_level(),
        "contract_expiry": generate_contract_expiry()
    } for _ in range(num_records)]

    return pd.DataFrame(data)

# @app.route('/download_it_infrastructure_data')
# def download_it_infrastructure_data():
#     df = generate_it_infrastructure_data(num_records=500000)
#     output = io.BytesIO()
#     df.to_csv(output, index=False)
#     output.seek(0)

#     return send_file(output, mimetype='text/csv', as_attachment=True, download_name='it_infrastructure_data.csv')

# if __name__ == '__main__':
#     sample_df = generate_it_infrastructure_data(10)
#     print(sample_df.head(10))
#     app.run(debug=True)
