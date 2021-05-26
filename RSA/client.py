#!/usr/bin/python3

import select
import socket
import sys
import rsa
import transformation as tf

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 12801
server.connect((ip_address, port))

nb = 10

#On commence par envoyer 10 cles au serveur  

def envoi_key(): 
    key_p = [] 
    key_s  = [] 
    for i in range(nb):
        pk, sk = rsa.key_rsa(1024)
        server.send(str(pk).encode())
        key_p.append(pk)
        key_s.append(sk)
    return key_p, key_s 

key_p, key_s = envoi_key()

print("Send key!")

recu = 0
message = ""

while message != "fin":

    sockets_list = [sys.stdin, server]
    
    read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == server:
            i = recu
            msg_recu = server.recv(1024)
            # Ici, nous avons essayer que l'envoie un nouveau jeu de cle par les clients quand le serveur n'en a plus. Mais nous avons un probleme de reseau 
            # if msg_recu == b"key": #Le serveur demande des clés 
            #     recu = 0 
            #     key_p, key_s = envoi_key() #On lui envoie donc un jeu de clé 
            #     print("[SEND KEY]")
            # else: 
            msg_recu = msg_recu.decode()
            msg_recu = rsa.decrypt_rsa(int(msg_recu), key_s[i]) #Le client dechiffre le message 
            msg_recu = tf.int_to_str(msg_recu) #On transforme le message en string 
            print(f"[MSG]  {msg_recu}")
            recu +=1 
        else:            
            message = input() #Le client ecrit son message
            server.send("key".encode()) #Il demande une cle au serveur 
            key_B = server.recv(1024).decode()
            # Ici, nous rentrons dans le cas ou le serveur n'as plus de cle. Il demande au client d'attendre 5 secondes, le temps que le deuxieme client lui envoie les cles neccessaire. 
            # if key_B == "Wait":
            #     print("[WAIT 5 Secondes]")
            #     time.sleep(5) 
            #     key_B = server.recv(1024).decode()
            #     print("[SEND NEW KEY]")


            key_B = tf.str_to_list(key_B)  #Les clés sont dans le même message, alors on les mets n et e dans une liste à la place d'une string 
            message = tf.str_to_int(message) #On transforme son message en int 
            message = rsa.encrypt_rsa(message, (key_B[0], key_B[1])) #On chiffre son message avec rsa 
            message = str(message)
            message = message.encode()
            server.send(message) #On envoie le message au serveur 
            print(f"[SEND]  {message}")

server.close()