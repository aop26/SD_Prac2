import socket
import re
import sys 
import time
import kafka
from os.path import exists
import os
import sqlite3
uso = ""

nexit = True

def printUso():
    print("Uso del programa:")
    print(uso)
    print("\n\tPROGRAMA DETENIDO\n")
    sys.exit()

def getIP():
    auxS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        auxS.connect(('8.8.8.8',1))
        IP = auxS.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        auxS.close()
    return IP

def checkIP(ip2check, que):
    datos = re.split(':', ip2check)
    puerto = 0
    if (len(re.split(r'\D', ip2check)) != 5 or len(re.split(':', ip2check))!=2) and datos[0]!='localhost':
        print("Error leyendo ip del " + que)
        printUso()

    try:
        puerto = int(datos[1])
    except:
        print("Error leyendo ip del " + que)
        printUso()

    ip = datos[0]
    return (ip,puerto)

def kp(ip):
    while nexit:
        try:
            return kafka.KafkaProducer(bootstrap_servers=ip)
        except:
            print("No se ha podido conectar a kafka. Reintentando en 1 segundo.")
            time.sleep(1)

def kc(ip, topic):
    global nexit
    while nexit:
        try:
            print(ip)
            return kafka.KafkaConsumer(topic,bootstrap_servers=ip)
        except Exception as e:
            print("No se ha podido conectar a kafka. Reintentando en 1 segundo.\n",e)
            time.sleep(1)
            if(not nexit):
                quit()

def openDB():
    if(not exists('database.db')):
        con = sqlite3.connect('database.db')
        with open('scriptBD', 'r') as file:
            script = file.read()
        scriptlines = script.split(';')
        cur = con.cursor()
        for line in scriptlines:
            print("ejecutando ",line+';')
            try:
                cur.execute(line+';')
                con.commit()
            except Exception as e:
                print("Error creating db",e)
                os.remove("database.db")
                con.close()
                quit()
        return con
    else:
        return sqlite3.connect('database.db')

def leerAtr(ID):
    con = openDB()
    cur = con.cursor()
    cur.execute(f"select x, y, waitTime,maxPeople from RIDE where ID = {ID}")
    res = cur.fetchone()
    con.close()
    return [res[0],res[1]], res[2], res[3]

def stopAll():
    global nexit
    nexit = False