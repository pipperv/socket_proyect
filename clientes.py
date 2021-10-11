import socket
import select
import threading
import sys


class Conexion_Servidor():
    def _init_(self, HOST = "127.0.0.1", PORT=8889): 
       #Se reciben los clientes, para esto se crea una lista
       self.clientes = []
       # Se crea el socket y se conecta al servidor.
       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       # Conexión con el equipo de manera interna
       self.s.bind((str(HOST),int(PORT)))
       # Se avisara al cliente que se ha conectado
       s.connect((HOST, PORT))
       print("Conectado al servidor")

       #Aqui deberia activar el threading
       # Threading para ingresar a cada cliente
       aceptado = threading.Thread(target = self.bienvenida)
       cargando = threading.Thread(target = self.cargando)

       aceptado.daemon = True
       aceptado.start()

       cargando.daemon = True
       cargando.start()


       #Aqui se leera los distintos comandos 
       while True:
           msg = input("->")
           if msg == "q":
               self.s.close()
               sys.exit()
            # Envía un mensaje privado al usuario especificado por <Identificador>   
           if msg == "p":
               pass
               # mandar mensaje privado
               #Muestra los identificadores de los usuarios que se encuentran conectados 
           if msg == "u":
               pass
           if msg == "smile":
               print(":)")
           if msg == "angry":
               print(">:(")
           if msg == "combito":
               print("Q(’- ’Q)")
           if msg == "larva":
               print("(:o)OOOooo")
           if msg == "artefactos":
               pass
               # entrega una lista de artefactos que el usuario tiene en la cuenta
           else:
               pass
    # Se crea la función que manda mensajes privador
    # recibe como parametros (msg, cliente)
    
    # Se crea la función que manda mensajes al chat general 
    def msg_chat_general(self,msg,cliente):
        for i in self.clientes:
            try:
                if i != cliente:
                    print("[SERVER] Cliente sunombre connect")
            except:
                pass
    # Se define la función bienvenida que le da la bienvenida al cliente, solo debe llegarle a este
    def bienvenida(self):
        while True:
            try:
                sclient,addr = self.s.accept()
                # obtenemos el identificador del cliente
                nombre = str(sclient.getpeername)
                # agregamos el cliente a la lista
                self.clientes.append(sclient)
            except:
                pass
            


    #¡Bienvenid@ al chat de Granjerxs!
    #[SERVER] Cuéntame, ¿qué artefactos tienes?
    #6, 13, 14, 20, 25, 26
    #[SERVER] Tus artefactos son: Punta de flecha, Espada antigua,
    #Cuchara oxidada, Estrella de mar seca, Yelmo enano, Dispositivo enano.
    #¿Está bien? (Sí/No)
    #Sí
    #[SERVER] ¡OK
    # Se define la funicón cargando donde recibe los datos del servidor y se imprimen 
    def cargando(self):
        while True:
            if len(self.clientes)>0:
                for i in self.clientes:
                    try:
                        data = c.recv(1024)
                        # si se recibe info
                        if data:
                            # llama a la función de los mensajes que aparecen en chat general
                            self.msg_chat_general(data, c)
                    except:
                        pass



   



# se llama la clase de nuevo

s = Conexion_Servidor()
    
# Se cierra el socket.
#s.close()