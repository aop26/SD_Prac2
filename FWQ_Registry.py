#!/usr/bin/python3

import sys
import customutils as cu
import socket
import threading


HEADER = 64
FORMAT = 'utf-8'
FIN = "FIN"
MAX_CONEXIONES = 2

#Lectura y comprobación de argumentos
cu.uso = "FWQ_Registry [Puerto de escucha]"

if len(sys.argv) != 2:
    print("Número erróneo de argumentos.")
    cu.printUso()

puerto = 0
try:
    puerto = int(sys.argv[1])
except:
    print("El puerto no es un número")
    cu.printUso()



ADDR = (cu.getIP(), puerto)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print("[STARTING] Servidor inicializándose...")


def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} connected.")

    connected = True
    userData = [-1]
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)

        if(msg == FIN):
            connected = False
        elif(msg == "c"):
            # crea perfil
            name = conn.recv(msg_length).decode(FORMAT)
            password = conn.recv(msg_length).decode(FORMAT)
            if(cu.checkUserName(name)):
                cu.crearUserDB(name, password)
                conn.send("Nueva cuenta creada.".encode(FORMAT))
                conn.send("1".encode(FORMAT))
            else:
                conn.send("Error al crear la cuenta.".encode(FORMAT))
                conn.send("0".encode(FORMAT))


        elif(msg == "l"):
            name = conn.recv(msg_length).decode(FORMAT)
            password = conn.recv(msg_length).decode(FORMAT)
            userData = cu.loginDB(name, password)
            if(userData[0] != -1):
                conn.send("Sesion inciada!".encode(FORMAT))
                conn.send(str(userData[0]).encode(FORMAT))
            else:
                conn.send("Error en el incio de sesion.".encode(FORMAT))
                conn.send("-1".encode(FORMAT))

        elif(msg == "m"):
            # modifica perfil

            if(userData[0] != 1):
                name = conn.recv(msg_length).decode(FORMAT)
                password = conn.recv(msg_length).decode(FORMAT)

                if(name == ""):
                    name = userData[3]
                if(password == ""):
                    password = userData[4]
                
                if(cu.modifyUserDB(userData[0], name, password)):
                    conn.send("Cuenta modificada.".encode(FORMAT))
                    conn.send("1".encode(FORMAT))
                else:
                    conn.send("Error al modificar la cuenta.".encode(FORMAT))
                    conn.send("0".encode(FORMAT))

    conn.close()
    
        

def start():
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {ADDR}")
    CONEX_ACTIVAS = threading.active_count()-1
    print(CONEX_ACTIVAS)
    while True:
        conn, addr = server.accept()
        CONEX_ACTIVAS = threading.active_count()
        if (CONEX_ACTIVAS <= MAX_CONEXIONES): 
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
            print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
        else:
            print("OOppsss... DEMASIADAS CONEXIONES. ESPERANDO A QUE ALGUIEN SE VAYA")
            conn.send("OOppsss... DEMASIADAS CONEXIONES. Tendrás que esperar a que alguien se vaya".encode(FORMAT))
            conn.close()
            CONEX_ACTUALES = threading.active_count()-1
        



######################### MAIN ##########################


start()



