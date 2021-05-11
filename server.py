#!/usr/bin/python3

import socket
import sys
import threading
import time

# Création de la socket pour la communication client serveur
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Configuration de la socket sur le réseau
hote = '127.0.0.1'
port = 12801
socket_server.bind((hote, port))

socket_server.listen(3)

client_list = []
client_key = [[], []]

def client_method (connection, address):
    
    if len(client_list) == 2: 
        for i in range(15):
            client_key[1].append(connection.recv(4096))
    else: 
        for i in range(15):
            client_key[0].append(connection.recv(4096)) 

    print(client_key)
    message = b""
    count = [0,0] 
    while message != b"fin":
        while len(client_list) == 2: 
            message = connection.recv(2048)
            if message != b'':
                if message == b"key":
                    for i in range(2):
                        if client_list[i] != connection:
                            count[i] += 1 
                            if (count[i] < 15): 
                                key = client_key[i].pop(0)
                                connection.send(key)
                            else:
                                print("plus de clé")
                else: 
                    print(message)
                    for i in client_list:
                        if i != connection:
                            i.send(message)

    client_list.remove(connection)
    connection.close()

while True:

    connection, address = socket_server.accept()

    client_list.append(connection)

    threading.Thread(target=client_method, args=(connection, address,)).start()

    time.sleep(1)

connection.close()
socket_server.close()