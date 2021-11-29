import socket
import re
import sys 
import time
import kafka
from kafka.admin import KafkaAdminClient,NewTopic 
from os.path import exists
import os
import sqlite3
from Crypto.Cipher import AES 
from Crypto.Hash import SHA256 
import requests
from kafka.producer.kafka import KafkaProducer
from Ride import *
from Visitor import *
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
    #try:
    #    admin_clinet = KafkaAdminClient(bootstrap_servers=ip, client_id='test')
    #    admin_clinet.create_topics(new_topics=[NewTopic(name=topic, num_partitions=1, replication_factor=1)],validate_only=False)
    #except Exception as e:
    #    print("No se ha podido crear el nuevo topic",e)
    while nexit:
        try:
            return kafka.KafkaConsumer(topic,bootstrap_servers=ip,group_id=None)
        except Exception as e:
            print("No se ha podido conectar a kafka. Reintentando en 1 segundo.\n",e)
            time.sleep(1)
            if(not nexit):
                quit()

def getMap(addr,name):
    s = socket.socket()
    for i in range(5):
        try:
            #print("Connecting to ",addr)
            s.connect((addr[0],int(addr[1])))
            #print("Sent",name)
            s.send(name.encode('utf-8'))
            res = s.recv(4096).decode('utf-8')
            #print("Recibidos datos del engine en ",addr)
            if(res=="NO"):
                return -1
            elif(res=="403"):
                print("No se puede iniciar sesion.")
                return 403
            elif(res=="420"):
                print("Parque lleno. Espere unos minutos.")
                return -1
            else:
                return strToMap(res)
        except Exception as e:
            print("Cannot connect to engine: ",e)
    return -1
    #time.sleep(2)
    #kafkaConsumer = kc(ip,name+"_map")
    #print(name+'_map')
    ##ste = False
    ##while not ste:
    ##    try:
    ##        kafkaConsumer.seek_to_end()
    ##
    ##    except Exception as e:
    ##        print("waiting for engine",e)
    ##        time.sleep(1)
    #message = ""
    #for msg in kafkaConsumer:
    #    print("premsg")
    #    
    #    break
    #msg = next(kafkaConsumer)
    #message =str(msg.value).replace('b','').replace("'",'')
    #print("postmsg")
    ##message = str(msg.value).replace('b','').replace("'",'')
    #print(message)
    #if(message == "NO"):
    #    return "NO"
    #else:
    #    return strToMap(message)
    #return message

def sendMap(ip,map,name):
    print(name+"_map")
    s = mapToStr(map)
    print(name+"_map")
    kafkaProducer=kp(ip)
    print(name+"_map")
    kafkaProducer.send(name+'_map',value=s.encode('utf-8'))
    print(s)
    kafkaProducer.close()
    
def mapToStr(map):
    s = ""
    for i in range(20):
            for j in range(20):
                if(isinstance(map[j][i], Ride)):
                    s+="r"+str(map[j][i].waitingTime)
                elif(isinstance(map[j][i], Visitor)):
                    s+="u"+str(map[j][i].id)
                else:
                    s+='-'
    #print("str:",s)
    return s


def strToMap(s):
    #print("str:",s)
    m = [ [0 for j in range(20)] for i in range(20)]
    mapStr = [char for char in s]
    currentCount = 0
    toskip=0
    for i in range(len(mapStr)):
        if(toskip>0):
            toskip-=1
            continue
        if(mapStr[i]=='r'):
            #print("ride")
            auxStr = ""
            i+=1
            #toskip+=1
            while(i<len(mapStr)and mapStr[i].isdigit()):
                auxStr+=mapStr[i]
                i+=1
                toskip+=1
            m[currentCount-(currentCount//20)*20][currentCount//20]=Ride(currentCount-(currentCount//20)*20, currentCount//20, int(auxStr))
        elif(mapStr[i]=='u'):
            #print("user")
            auxStr = ""
            i+=1
            #toskip+=1
            while(i<len(mapStr)and mapStr[i].isdigit()):
                auxStr+=mapStr[i]
                i+=1
                toskip+=1
            v = Visitor(int(auxStr))
            v.x=currentCount-(currentCount//20)*20
            v.y=currentCount//20
            m[currentCount-(currentCount//20)*20][currentCount//20]=v
        #print(i)
        currentCount+=1
    #print(currentCount)
    return m

    



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


def checkUserName(username):
    con = openDB()
    cur = con.cursor()
    try:
        cur.execute(f'select id from CLIENT where username = "{username}"')
    except Exception as e:
        print(e)
        con.close()
        return -1
    res = cur.fetchone()
    con.close()
    if(res is not None):
        return True
    else:
        return False


def loginDB(username, password):
    con = openDB()
    cur = con.cursor()
    try:
        cur.execute(f'select * from CLIENT where username = "{username}" and password = "{password}"')
    except Exception as e:
        print(e)
        con.close()
        return -1
    res = cur.fetchone()
    con.close()
    if(res):
        return res
    else:
        return [-1]

def modifyUserDB(id,username,password):
    con = openDB()
    cur = con.cursor()
    try:
        cur.execute(f'update CLIENT set username="{username}",password="{password}" where ID = {id}')
        con.commit()
    except Exception as e:
        print(e)
        return False
    con.close()
    return True

def crearUserDB(username,password):
    con = openDB()
    cur = con.cursor()
    try:
        cur.execute(f'insert into CLIENT(username, password) VALUES("{username}", "{password}")')
        con.commit()
    except Exception as e:
        print(e)
        return False
    con.close()
    return True

def stopAll():
    print("stopping all")
    global nexit
    nexit = False

def mapaVacio():
    mapaActualizado = []
    for x in range(20):
        mapaActualizado.append([])
        for y in range(20):
            mapaActualizado[x].append(-1)
    return mapaActualizado


def GetWeather():
    weather = []
    file = open("cities.txt", "r")
    url = file.readline().split()
    apiKey = file.readline().split()[0]
    for i in range(4):
        try:
            city = file.readline().split()[0]
            tiempo = requests.get(url[0]+city+url[1]+apiKey)
            weather.append([city, round(tiempo.json()["main"]["temp"]-273, 2)]) # t-273 porque esta en kelvin y queremos celsius
        except:
            weather.append(["error", -1])
    return weather

# ENCRIPTACION / HASHES

def HashPassword(password):
    hash = SHA256.new()
    hash.update(password.encode("utf-8"))
    return str(hash.digest())


def GetKey():
    file = open("clave", "r")
    key = file.readline()
    file.close()
    return key



'''
Esto hay que adaptarlo para el api rest

def EncryptPasswd(password):
    cifrar = AES.new(GetKey(), AES.MODE_CBC, 'This is an IV456')
    while(len(password) < 16):
        password += " "
    return cifrar.encrypt(password)


def DecryptPasswd(password):
    cifrar = AES.new(GetKey(), AES.MODE_CBC, 'This is an IV456')
    return cifrar.decrypt(password).split()[0]'''
