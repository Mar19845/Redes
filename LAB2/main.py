
from http import client
from client import Client
HOST = '127.0.0.1'
PORT = 9090

cliente = Client(host=HOST, port=PORT)
cliente.send_msg_handler()