#!/usr/bin/python3

import socket
import sys
import threading
import time

# Création de la socket pour la communication client serveur
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Configuration de la socket sur le réseau
ip_address = '127.0.0.1'
port = 12801
socket_server.bind((ip_address, port))

socket_server.listen(3)

client_list = []
list_key = [] 
g = 0

# Alice connectée en première 
def client_method (connection, address):

    message = b""
    
    if len(client_list) == 1:
        # Demande de g à Alice
        print("\n[LOG]  Demande de g à Alice\n")
        connection.send(b"g")
        print("[SEND] g")
        g = connection.recv(1024)
        print(f"[RECV] {g}")
        list_key.append(g)
        
    if len(client_list) == 2: 
        print("\n[LOG]  Envoi de g à Bob\n")
        connection.send(b"g1")
        print("[SEND] g1")
        connection.send(list_key[0])
        print(f"[SEND] {list_key[0]}")

        time.sleep(1)
        connection.send(b"ga")
        print("[SEND] ga")
        g_a = connection.recv(1014)
        print(f"[RECV] {g_a}")
        list_key.append(g_a)

        for i in client_list: 
            if i != connection:
                print("[LOG]  Envoi de g^a à Bob et g^b à Alice")
                i.send(b"ga")
                print("[SEND] ga")
                # Reception de la clef d'Alice
                gb = i.recv(1024)
                list_key.append(gb)
                print(f"[RECV] {gb}")
                # Envoi a Bob
                # connection.send(b"gb")
                print("[SEND] gb")
                connection.send(gb)
                print(f"[SEND] {gb}")
                #Envoi de ga à Alice
                # i.send(b"gb")
                i.send(g_a)
                print(f"[SEND] {g_a}")
        
        print(f"[LOG] END KEY EXCHANGE")

    while message != b"fin":

        message = connection.recv(1024)

        if message != b'':
            print(f"[MSG]  {message}")
            for i in client_list:
                if i != connection:
                    i.send(message)

    client_list.remove(connection)
    connection.close()

i = 0

while True:

    connection, address = socket_server.accept()

    client_list.append(connection)

    print(client_list)

    threading.Thread(target=client_method, args=(connection, address,)).start()

    time.sleep(1)

connection.close()
socket_server.close()