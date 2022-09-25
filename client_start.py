from django import db
from config.client import server_ip, server_port, e_type, e_number
from module.client import Client
from module.db import devices


client = Client(ip=server_ip, port=server_port, e_data_drivers=devices,
                e_type=e_type, e_number=e_number)
client.start()
