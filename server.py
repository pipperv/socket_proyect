import socket

# Se configura el servidor para que corra localmente y en el puerto 8889.
HOST = '127.0.0.1'
PORT = 8889

# Se crea el socket y se instancia en las variables anteriores, aceptando clientes.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

# Se buscan clientes que quieran conectarse.
while True:

    # Se acepta la conexión de un cliente
    conn, addr = s.accept()
    print("Cliente conectado")
    
    # Se ejecuta lo siguiente en un loop hasta que el cliente se desconecte.
    while True:
    
        # Se reciben los datos que ha enviado el cliente.
        data = conn.recv(1024)
        
        # Si el cliente se desconecta, al leer los datos se recibirá un string vacío.
        if not data:
            
            # Salir de este loop y permitir la conexión de otro cliente.
            break
        
        # Responder con los mismos datos que fueron recibidos.
        conn.send(data)
    
    # Terminar la conexión con el cliente.
    conn.close()