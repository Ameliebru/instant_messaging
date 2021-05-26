#!/usr/bin/python3

import select
import socket
import sys
import aes 
import expo_rapide
import padding
import os
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, long_to_bytes


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 12801
server.connect((ip_address, port))

a  = bytes_to_long(bytes(os.urandom(1)))
str_a = str(a)
print(a)
iv = b'\x102\xe5\xdf\x7f\xd8\xaf\x81gB\\\x96t\x05\xa7:'

message = ""
good = False
finish = False
while message != "fin":

    sockets_list = [sys.stdin, server]
    
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
    
    for socks in read_sockets:
        if socks == server:
            msg_recu = server.recv(1024)
            if not good:
                
                if msg_recu == b'g':
                    print("\n[LOG]  Donner g\n")
                    print(f"[RECV] {msg_recu}")
                    g = bytes_to_long(bytes(os.urandom(2)))
                    str_g = long_to_bytes(g)
                    server.send(str_g)
                    print(f"[SEND] {g}")
                    ga = expo_rapide.square_and_multiply(g, a)

                if msg_recu == b"g1":
                    print("\n[LOG]  Réception de g et calcul de g^a\n")
                    g = bytes_to_long(server.recv(1024))
                    print(f"[RECV] {g}")
                    ga = expo_rapide.square_and_multiply(g, a)
                
                if msg_recu == b"ga":
                    print("\n[LOG]  Envoi de g^a\n")
                    str_ga = long_to_bytes(ga)
                    server.send(str_ga) 
                    print(f"[SEND] {ga}")
                    finish = True
                
                if finish: 
                    print("\n[LOG]  Reception de g^b et calcul de la clef\n")
                    gb = bytes_to_long(server.recv(1024))
                    print(f"[RECV] {gb}")
                    key = expo_rapide.square_and_multiply(gb, a)
                    key = long_to_bytes(key)[0:16]
                    print(f"[KEY]  {key}")
                    good = True
            else:
                aes = AES.new(key, AES.MODE_CBC, iv)
                msg_recu = aes.decrypt(msg_recu)
                msg_recu = padding.unpadding(msg_recu)
                msg_recu = msg_recu.decode()
                print(f"[MSG]  {msg_recu}")
            
        else:
            aes = AES.new(key, AES.MODE_CBC, iv)
            message = input(">")
            message = aes.encrypt(padding.padding(message, 16))
            #message = message.encode() 
            server.send(message)
            print(f"[SEND] {message}") 

server.close()