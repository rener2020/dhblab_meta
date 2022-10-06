from module.client import Client
from config.client import ip, port, name


client = Client(ip, port, name)
client.start()
