import customutils as cu
#con = cu.openDB()
#cur = con.cursor()
#ID = 1
#cur.execute(f"select x, y, waitTime,maxPeople from RIDE where ID = {ID};")
#res = cur.fetchone()
#con.close()
#print([res[0],res[1]],res[2],res[3])

from Crypto.Cipher import AES 
clave = cu.GetKey()
print(len(clave))
cifrar = AES.new(clave, AES.MODE_CBC, 'This is an IV456')

txt = "JAJAXDLOL"

cifrado = cu.EncryptPasswd(txt)
print(cifrado)
print(cu.DecryptPasswd(cifrado))