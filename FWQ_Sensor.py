#!/usr/bin/python3

import sys
import customutils as cu
from random import randrange
from kafka import KafkaProducer
from time import sleep

def GetValue(n):
    if(n == ""):
        return randrange(10, 100), 1
    return n, 0


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

n, change = GetValue(input("input number"))

while(True):
    n, change = UpdateValue(n, change)
    producer.send('sensors',str(ID).encode('utf-8')+'-'.encode('utf-8')+ str(n).encode('utf-8'))
    time.sleep(randrange(1, 3))