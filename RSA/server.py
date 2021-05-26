#!/usr/bin/python3

import socket
import threading
import time

# Création de la socket pour la communication client serveur
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Configuration dse la socket sur le réseau
hote = '127.0.0.1'
port = 12801
socket_server.bind((hote, port))

socket_server.listen(3)
nb = 10
client_list = []
client_key = [[], []]

def client_method (connection, address):
    #On stocke les clés des deux clients 
    if len(client_list) == 2: 
        for _ in range(nb):
            client_key[1].append(connection.recv(4096))
    else: 
        for _ in range(nb):
            client_key[0].append(connection.recv(4096)) 

    message = b""
    count = [0,0] 
    while message != b"fin":
        while len(client_list) == 2: 
            message = connection.recv(2048) #Le serveur a reçu un message de connection 
            if message != b'':
                if message == b"key": #Le client a besoin d'une clé 
                    for i in range(2):
                        if client_list[i] != connection:
                            count[i] += 1 
                            if (count[i] <= nb):  
                                key = client_key[i].pop(0) #On prends la valeur et on la supprime aussitôt 
                                connection.send(key) #On envoie la clé au client
                            else:
                                print("plus de clé")

                                # count[i] = 1
                                # client_list[i].send(b"key")
                                # connection.send(b"Wait")
                                # print("ok")
                                # client_key[i] = []
                                # for _ in range(nb): 
                                #     key = client_list[i].recv(2048)
                                #     time.sleep(0.2)
                                #     client_key[i].append(key)
                                #     client_list[i].send("ok".encode())
                                #     print("c'est ok !")
                                # key = client_key[i].pop(0)
                                # connection.send(key)
                                # print("clé envoie!" )
                                # message = connection.recv(2048)
                                # print(message)
                                # client_list[i].send(message)

                else: 
                    print(message)
                    for i in client_list:
                        if i != connection: #On cherche le client a qui le mesage doit être envoyer 
                            i.send(message) #On envoie le message 

    client_list.remove(connection)
    connection.close()

while True:

    connection, address = socket_server.accept()

    client_list.append(connection)

    threading.Thread(target=client_method, args=(connection, address,)).start()

    time.sleep(1)

connection.close()
socket_server.close()