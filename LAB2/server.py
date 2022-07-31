from concurrent.futures import process
import socket
import threading
import sys
import pickle

class Server():
    def __init__(self, host="localhost", port=4000):
        self.clients = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)
        accept = threading.Thread(target=self.acceptConnection)
        process = threading.Thread(target=self.proccessConnection)
        
        accept.daemon = True
        accept.start()
        process.daemon = True
        process.start()

        while True:
            msg = input('->')
            if msg == 'salir':
                self.sock.close()
                sys.exit()


    def msg_to_all(self, msg, client):
        for c in self.clients:
            try:
                if c != client:
                    print(msg)
                    c.send(msg)
            except:
                self.clients.remove(c)
            
            
    def acceptConnection(self):
		#print("aceptarCon iniciado")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clients.append(conn)
            except:
                pass

    def proccessConnection(self):
        while True:
            if len(self.clients) > 0:
                for c in self.clients:
                    try:
                        data = c.recv(1024)
                        if data:
                            self.msg_to_all(data,c)
                    except:
                        pass


s = Server()