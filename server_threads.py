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
            sino = sock.recv(1024).decode()
            if sino == "Si":
                sock.send("[SERVER] ¡OK!".encode())
                arte = answ_list
            else:
                sock.send("[SERVER] Vuelve a ingresar tu atefactos".encode())

    nombre = str(sock.getpeername()[1])
    arte_dict[nombre] = arte


    while True:
        data = None

        try:
            msg = sock.recv(1024).decode()
        except:
            break

        #Commands
        if msg[0] == ":":
            msg = msg.split(' ')
            if msg[0] == ":q":
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
            
            elif msg[0] == ":p":
                if len(msg) >= 3:
                    try:
                        user_sock = sock_clientes[list(arte_dict.keys()).index(msg[1])]
                    except:
                        sock.send(f"[SERVER] El usuario {msg[1]} no esta en este servidor. :c".encode())
                    p_msg = ' '.join([str(item) for item in msg[2:]])
                    user_sock.send(f"(privado) Cliente {nombre}: {p_msg}".encode())
                else:
                    sock.send(f'[SERVER] Error de syntaxis (Syntaxis: ":p <Usuario> <Mensaje>")'.encode())

            elif msg[0] == ":u":
                users = list(arte_dict.keys())
                users_string = ', '.join([str(item) for item in users])
                sock.send(f'[SERVER] Los usuarios conectados son {users_string}'.encode())

            elif msg[0] == ":smile":
                data = ":)"

            elif msg[0] == ":angry":
                data = ">:("

            elif msg[0] == ":combito":
                data = "Q('-'Q)"

            elif msg[0] == ":larva":
                data = "(:o)OOOooo"

            elif msg[0] == ":artefactos":
                # Se crea una lista con los nombres (no números) de los artefactos.
                arte_list = [artefactos[k] for k in arte_dict[nombre]]
                sock.send(f"[SERVER] Tus artefactos son {', '.join(arte_list)}".encode())

            elif msg[0] == ":artefacto":
                artef = artefactos[msg[1]]
                sock.send(f"[SERVER] El Id '{msg[1]}' corresponde al artefacto '{artef}'".encode())

            elif msg[0] == ":offer":
                if len(msg) == 4:
                    try:
                        user_sock = sock_clientes[list(arte_dict.keys()).index(msg[1])]
                        if (msg[2] in arte_dict[nombre]) and (msg[3] in arte_dict[msg[1]]):
                            user_sock.send(f"[SERVER] El Cliente {nombre} quiere intercambiar su {artefactos[msg[2]]} por tu {artefactos[msg[3]]}, ¿Aceptas? (:accept/:reject)".encode())
                        elif not (msg[2] in arte_dict[nombre]):
                            sock.send(f"[SERVER] No tienes el articulo {artefactos[msg[2]]}. :c".encode())
                        elif not (msg[3] in arte_dict[msg[1]]):
                            sock.send(f"[SERVER] El cliente {msg[1]} tiene el articulo {artefactos[msg[3]]}. :c".encode())
                    except:
                        sock.send(f"[SERVER] El usuario {msg[1]} no esta en este servidor. :c".encode())
                else:
                    sock.send(f'[SERVER] Error de syntaxis (Syntaxis: ":offer <Usuario> <MiArtefactoId> <SuArtefactoId>")'.encode())

            elif msg[0] == ":accept":
                pass

            elif msg[0] == ":reject":
                pass

            else:
                sock.send(f"[SERVER] El comando '{msg[0]}' no existe.".encode())
    
            
        else:
            data = msg

        # Se manda el mensaje a todos los clientes.
        if data != None:
            for s in sock_clientes:
                if s != sock:
                    s.send(f"Cliente {nombre}: {data}".encode())
                else:
                    s.send(f"Yo: {data}".encode())

# Se configura el servidor para que corra localmente y en el puerto 8889.
HOST = '127.0.0.1'
PORT = 8889

# Se crea el socket y se instancia en las variables anteriores.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

while True:

    # Se acepta la conexión de un cliente
    conn, addr = s.accept()
    print(f"[SERVER] Cliente {conn.getpeername()[1]} conectado.")
    for sck in sock_clientes:
        sck.send(f"[SERVER] Cliente {conn.getpeername()[1]} conectado.".encode())
    sock_clientes.append(conn)   

    # Se manda el mensaje de bienvenida
    conn.send("¡Bienvenid@ al chat de Granjerxs!".encode())

    client_thread = threading.Thread(target=cliente, args=(conn,))
    
    client_thread.daemon = True
    client_thread.start()       