from bitarray import bitarray
import random
import socket
import threading
class Client:
    def __init__(self,host, port,err = 0.1):
        self.err = err
        self.bit_converter = bitarray()
        self.bit_converter_recived = bitarray()
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
   
    def get_msg(self):
        self.msg = input("Send msg: ")
        
    
    def convert_msg(self): #capa de verificacion, convertir el mensaje a bits
        self.bit_converter.frombytes(self.msg.encode('utf-8'))
       
        
    def add_noise(self): # agregar ruido al mensaje, a según cierta probabilidad expresada en errores por bits transmitidos
        prob = round(random.random(),2) # Gives you a number BETWEEN 0 and 1 as a float
        if prob == self.err:
            print('hay error')
        else:
            print(prob,self.err)
    
    def send_msg(self): # enviar el mensaje atraves de un socket a otro cliente
        self.sock.send(self.bit_converter)
        
    def receive_msg(self): # recibir el mensaje atraves de un socket a otro cliente
        while True:
            try:
                self.msg_recived = self.sock.recv(1024)
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.socket.close()
    
    def ver_msg(self): # recibir el mensaje en bits y con un algoritmo encontrar o reparar el error del mensaje
        #convertir el msg a string una vez se haya corregido o detectado un error
        list_of_bytes = self.bit_converter_recived.tolist() # convert the bytes to list 
        self.msg_recived = bitarray(list_of_bytes).tobytes().decode('utf-8')
        
    def print_msg(self):
        print(self.msg_recived)
        
    def send_msg_handler(self):
        ##############################
        # 1 enviar cadena
        # 2 envar cadena segura/capa de verificacion
        # 3 agregar ruido
        # 4 enviar a traves de sockets
        ##############################
        
        # falta agregar threads para que sea simulteano
        
        #get the message from the user
        self.get_msg()
        #convert the msg to byte //  capa de verificacion
        self.convert_msg()
        # add_noise to the msg
        self.add_noise()
        # send msg 
        self.send_msg()
    def recive_msg_handler(self):
         ##############################
        # 1 recivir cadena a traves de sockets
        # 2 enviar cadena segura/capa de verificacion
        # 3 encontrar error o corregirlo con los algoritmos
        # 4 mostralo al usuario
        ##############################
        
        # falta agregar threads para que sea simulteano
        self.receive_msg()
        self.convert_msg()
        self.print_msg()