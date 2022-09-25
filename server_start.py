from module.server import Server
from config.server import ip, port

server = Server(ip, port)
server.start()
