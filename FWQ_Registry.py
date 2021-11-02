#!/usr/bin/python3

import sys
import customutils as cu
import socket
import threading


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
FIN = "FIN"
MAX_CONEXIONES = 2


def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} connected.")

    connected = True
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
        elif(msg == "l"):
            # login perfil
            option = conn.recv(msg_length).decode(FORMAT)
            
            while(option != "q"):
                if(option == "n"):
                    name = conn.recv(msg_length).decode(FORMAT)
                elif(option == "p"):
                    password = conn.recv(msg_length).decode(FORMAT)

                option = conn.recv(msg_length).decode(FORMAT)
        


    conn.close()
    
        

def start():
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")
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



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print("[STARTING] Servidor inicializándose...")

start()



