import socket
import re
import sys 
uso = ""

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