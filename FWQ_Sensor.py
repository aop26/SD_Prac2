#!/usr/bin/python3

import sys
import customutils as cu
from random import randrange
from kafka import KafkaProducer
import time



        
class inputThread(threading.Thread):
    def __init__(self,ipaddr):
        threading.Thread.__init__(self)
        self.name = "FWQ_WaitingTimeServer kafkaConsumer"


    def run(self):
        global n
        global change 
        while(True):
            newValue = int(input())
            if(newValue != -1):
                n, change= newValue, 0
            else:
                n, change = GetValue()
    




def GetValue(n):
    return randrange(10, 100), 1


def UpdateValue(n, change):
    if(change != 0):
        n += 5 if change==1 else -5
        if(n < 0):
            n = 0
        
        if(randrange(1, 10) < 3): # solo cambia 1 tercio de las veces
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

producer = KafkaProducer(bootstrap_servers=sys.argv[1])




def exit_handler():
    global exit
    exit = True
    #cerrar cosas y tal
atexit.register(exit_handler)


global n, global change = GetValue() # se enciende el sensor y empieza a enviar datos
fixedValue = inputThread()
fixedValue.start()

while(True):
    global n, global change = UpdateValue(n, change)
    producer.send('sensors',str(ID).encode('utf-8')+'-'.encode('utf-8')+ str(n).encode('utf-8'))
    time.sleep(randrange(1, 3))
