from bitarray import bitarray
import random
import socket
import threading
import pickle
import sys


class Client():
	
    def __init__(self, host="localhost", port=4000,err = 0.1):
        self.err = err
        self.bit_converter = bitarray()
        self.bit_converter_recived = bitarray()
        #socket config 
        self.connect(str(host), int(port))
        #call the recive msg handler fucntion and bind it to a thread
        recive_msg_handler = threading.Thread(target=self.recive_msg_handler)

        recive_msg_handler.daemon = True
        recive_msg_handler.start()

        
        self.send_msg_handler()
        
    def send_msg_handler(self):
        ##############################
        # 1 enviar cadena
        # 2 envar cadena segura/capa de verificacion
        # 3 agregar ruido
        # 4 enviar a traves de sockets
        ##############################
        while True:
            msg = input('->')
            if msg != 'quit':
                #capa de verificacion
                self.convert_msg_to_bytes(msg)
                #add noise to the bits
                self.add_noise()
                #send msg through the socket
                self.send_msg(self.bit_converter)
                #clean the bit array
                self.bit_converter = bitarray()
            else:
                self.close()
                sys.exit()
    
    #capa de verificacion, convertir el mensaje a bits      
    def convert_msg_to_bytes(self,msg): 
        self.bit_converter.frombytes(msg.encode('utf-8'))
    
    # agregar ruido al mensaje, a según cierta probabilidad expresada en errores por bits transmitidos
    def add_noise(self):
        prob = round(random.random(),2) # Gives you a number BETWEEN 0 and 1 as a float
        if prob <= self.err:
            #change a random bit 
            index=random.randint(0, len(self.bit_converter)-1)
            if self.bit_converter[index]==1:
                self.bit_converter[index] = 0
            else:
                self.bit_converter[index] = 1

    
    
    
           
    def recive_msg_handler(self):
        ##############################
        # 1 recivir cadena a traves de sockets
        # 2 enviar cadena segura/capa de verificacion
        # 3 encontrar error o corregirlo con los algoritmos
        # 4 mostralo al usuario
        ##############################
        while True:
            try:
                msg = self.sock.recv(1024)
                if msg:
                    # recibir cadena a traves de sockets
                    self.bit_converter_recived = pickle.loads(msg)
                    # recibir el mensaje en bits y con un algoritmo encontrar o reparar el error del mensaje
                    self.verify()
                    #convertir el msg a string una vez se haya corregido o detectado un error 
                    self.convert_msg()
                    
                    print(self.msg_recived)
                    #print(pickle.loads(msg))
                    
            except:
                pass
            
           
    # recibir el mensaje en bits y con un algoritmo encontrar o reparar el error del mensaje
    def verify(self):
        pass
    #convertir el msg a string una vez se haya corregido o detectado un error      
    def convert_msg(self):
        #convertir el msg a string una vez se haya corregido o detectado un error
        list_of_bytes = self.bit_converter_recived.tolist() # convert the bytes to list
        #convertir bits to string
        self.msg_recived = bitarray(list_of_bytes).tobytes().decode('utf-8')
        
    
    
            
    
    #connection config for the socket
    def connect(self,host,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(host), int(port)))
        self.host = host
        self.port = port
        
    # close socket
    def close(self):
        self.sock.close()
    # send data through the socket
    def send_msg(self, msg):
        self.sock.send(pickle.dumps(msg))