#!/usr/bin/python3

import sys, signal
import customutils as cu
from random import randrange
from kafka import KafkaProducer
import time
import threading
import atexit

def ainput():
    try:
            foo = raw_input()
            return foo
    except:
            # timeout
            return

def interrupted(signum, frame):
    print("Stopping program")

exit = False
class inputThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "FWQ_WaitingTimeServer kafkaConsumer"
        self.exit = False


    def run(self):
        global n
        global change
        while(not exit):
            n, change = UpdateValue(n, change)
            producer.send('sensors',str(ID).encode('utf-8')+'-'.encode('utf-8')+ str(n).encode('utf-8'))
            time.sleep(randrange(1, 3))
    def close(self):
        producer.close()
        quit()
    




def GetValue():
    return randrange(10, 100), 1


def UpdateValue(n, change):
    if(change != 0):
        n += 5 if change==1 else -5
        if(n < 0):
            n = 0
        
        if(randrange(1, 10) < 2): # solo cambia 1 decimo de las veces
            change *= -1
    
    return n, change



#Lectura y comprobación de argumentos
cu.uso = "FWQ_Sensor [ip:puerto(gestor de colas)] [ID atracción]"


if len(sys.argv) != 3:
    print("Número erróneo de argumentos.")
    cu.printUso()


addressGestor = cu.checkIP(sys.argv[1],"gestor de colas")

ID= 0
try:
    ID = int(sys.argv[2])
except:
    print("La ID no es un número")
    cu.printUso()


producer = cu.kp(sys.argv[1])







#global n
#global change # se enciende el sensor y empieza a enviar datos

n, change = GetValue()
fixedValue = inputThread()
fixedValue.start()

def exit_handler():
    global exit
    exit = True
    fixedValue.close()
    #producer.close()
    #cerrar cosas y tal
atexit.register(exit_handler)

#signal.signal(signal.SIGALRM,interrupted)
while(not exit):
    newValue = 0
    try:
        newValue = int(input())
        if(newValue != -1):
            n, change= newValue, 0
        else:
            n, change = GetValue()
    except KeyboardInterrupt:
        print("Stopping program")
        exit = True
        fixedValue.close()
        break


