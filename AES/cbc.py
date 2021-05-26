
import aes  
from Crypto.Cipher import AES
import padding as pd
import os

key = b'\xc3,\\\xa6\xb5\x80^\x0c\xdb\x8d\xa5z*\xb6\xfe\\'
 
def xor( key1, key2):
    return [a ^ b for a,b in zip(key1, key2)] 

#generation d'une cle iv 
def gen_iv():
    IV = bytes(os.urandom(16))
    return IV

#Transformation en ascii 
def ascii(text):
    plaintext = ""
    for i in text:
        plaintext += chr(i)
    return plaintext
 

def cbc(key, message): 
    message = pd.padding(message,16).encode() #On ajoute du padding afin que le message soit de la bonne taille
    t = len(message)
    M = []
    iv = gen_iv()
    cipher = [iv] 
    for i in range(0,len(message),16): #On decoupe le message 
        M.append(message[i:i+16])
        
    print(M[0])
    #Debut du mode CBC
    m = ascii(xor(M[0], iv)).encode()
    m1 = aes.encrypt(key, m) #On chiffre le message avec AES
    cipher.append(m1)
    for i in range (1,len(M)) :
        print(i,cipher[i], M[i])
        m = ascii(xor(M[i], cipher[i])).encode()
        m1 = aes.encrypt(key, m)
        cipher.append(m1)
    
    a = AES.new(key, AES.MODE_CBC, iv)
    result = a.encrypt(b"".join(M))
    print(result)

    return b"".join( cipher)

#print(cbc(key, "salut ca va? Bien et toi?0000000")[16:])

#cipher = b'1111101000100101\xcb\x08\xfe\x0e\xbe\xcc|J\xc8j\x91\xb8d\xb5e\xb4{\x18\x11\xaf%K\x9a\x19\x0f\xab\x0c\x13ln\xb1\x87\xc2\x05j\xca\xce\x08\xc6%T\x19\x9f$\xe3\xc4\xd1\x8b'

def inv_cbc(key, cipher): 
    iv = cipher[0:16]
    C = [] 
    message = [] 
    print(cipher)

    for i in range(16,len(cipher),16): #On decoupe le chiffré
        C.append(cipher[i:i+16])

    c1 = aes.decrypt(key, C[0]) #On dechiffre le message
    m = ascii(xor(c1, iv)).encode() 
    message.append(m)  
    print(message, C[0])
    #Premier bloc ok mais le reste non 
    c2 = aes.decrypt(key, C[1])
    m = ascii(xor(c2, C[0])).encode()
    message.append(m)  
    print(message, C[1])

    # for i in range (1, len(C) - 1, 1) : 
    #     #print("mi = "  ,M[i], M[i-1])
    #     cn = aes.decrypt(key, C[i])
    #     #print(f"After decrypt: {m}")
    #     m = ascii(xor(cn, C[i-1])).encode()
    #     message.append(m)  
    

    return b"".join( message)

#print(inv_cbc(key, cbc(key, "salut ca va? Bien et toi?0000000")))