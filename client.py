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

def envoi_key(): 

    key_p = [] 
    key_s  = [] 
    for i in range(15):
        pk, sk = rsa.key_rsa(1024)
        server.send(str(pk).encode())
        key_p.append(pk)
        key_s.append(sk)
    return key_p, key_s 

key_p, key_s = envoi_key()

print("Clé envoyé")

recu = 0
message = ""

while message != "fin":

    sockets_list = [sys.stdin, server]
    
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == server:
            i = recu
            msg_recu = server.recv(100000)
            if msg_recu == b"key":
                envoi_key()
                
            msg_recu = msg_recu.decode()
            msg_recu = rsa.decrypt_rsa(int(msg_recu), key_s[i]) 
            msg_recu = tf.int_to_str(msg_recu) 
            print(msg_recu)
            recu +=1
        else:            
            message = input()

            server.send("key".encode())
            key_B = server.recv(1024).decode()
            key_B = tf.str_to_list(key_B)
            
            message = tf.str_to_int(message) #On transforme son message en int 
        
            message = rsa.encrypt_rsa(message, (key_B[0], key_B[1])) #On chiffre son message avec rsa 
            message = str(message)
            message = message.encode()
            
            server.send(message)

server.close()