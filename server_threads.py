import socket
import threading
import json

sock_clientes = []
arte_dict = {}
mutex = threading.Lock()

# Se cargan los datos de los artefactos.
with open("artefactos.json", "r") as j:
    artefactos = json.load(j)

def cliente(sock):
    global sock_clientes, arte_dict, artefactos

    #Ask for artefacts
    arte = None
    while arte == None:
        sock.send("[SERVER] Cuéntame, ¿qué artefactos tienes?".encode())
        try:
            answ = sock.recv(1024).decode()
        except:
            break
        answ_list = answ.split(',')
        art_list = [artefactos[k] for k in answ_list]
        if len(art_list) > 6:
            sock.send("[SERVER] No puedes tener mas de 6 artefactos!".encode())
        else:
            sock.send(f"[SERVER] Tus artefactos son {', '.join(art_list)}. ¿Esta bien? (Si/No)".encode())
            try:
                sino = sock.recv(1024).decode()
            except:
                break
            if sino == "Si":
                sock.send("[SERVER] ¡OK!".encode())
                arte = art_list
            else:
                pass

    nombre = sock.getpeername()[1]
    arte_dict[nombre] = arte


    while True:
        try:
            data = sock.recv(1024).decode()
        except:
            break

        #Commands
        if data[0] == ":":
            data = data.split(' ')
            if data[0] == ":q":
                print(f"[SERVER] Cliente {nombre} desconectado.")
                for s in sock_clientes:
                    if s != sock:
                        s.send(f"[SERVER] Cliente {nombre} desconectado.".encode())
                    else:
                        s.send("¡Adiós y suerte completando tu colección!".encode())
                # Se modifican las variables globales usando un mutex.
                with mutex:
                    sock_clientes.remove(sock)
                    arte_dict.pop(nombre)
                sock.close()
                break
            
            elif data[0] == ":p"
                pass

            elif data[0] == ":artefactos":
                # Se crea una lista con los nombres (no números) de los artefactos.
                arte_list = [artefactos[k] for k in arte_dict[nombre]]
                sock.send(f"[SERVER] Tus artefactos son {', '.join(arte_list)}".encode())
    
            elif data[0] == ":larva":
                data = "(:o)OOOooo"

        # Se manda el mensaje a todos los clientes.
        for s in sock_clientes:
            if s != sock:
                s.send(f"CLIENTE {nombre}: {data}".encode())
            else:
                s.send(f"Yo: {data}".encode())

# Se configura el servidor para que corra localmente y en el puerto 8889.
HOST = '127.0.0.1'
PORT = 8889

# Se crea el socket y se instancia en las variables anteriores.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

# Se buscan clientes que quieran conectarse.
while True:

    # Se acepta la conexión de un cliente
    conn, addr = s.accept()
    print(f"[SERVER] Cliente {conn.getpeername()[1]} conectado.")
    for s in sock_clientes:
        s.send(f"[SERVER] Cliente {conn.getpeername()[1]} conectado.".encode())
    sock_clientes.append(conn)

    # Se manda el mensaje de bienvenida
    conn.send("¡Bienvenid@ al chat de Granjerxs!".encode())

    # Se inicia el thread del cliente
    client_thread = threading.Thread(target=cliente, args=(conn,))
    client_thread.start()