import socket
import rsa
import transformation 

hote = "127.0.0.1"
port = 12801

connexion_avec_serveur = socket.socket()
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))
message = b""
keys = []
keys_B = []
message_B = []


while message!= b"fin":
    pk, sk = rsa.key_rsa(2048)
    n, e  = pk 
    keys.append((pk, sk))

    key = str(n) + " " + str(e)
    key = str(key)
    key = key.encode() 
    connexion_avec_serveur.send(key)

    key_Bob = connexion_avec_serveur.recv(2048)
    n_B, e_B = transformation.decoupage(key_Bob)
    keys_B.append((n_B, e_B))

    message = input("> ")  #Bob ecrit un message au serveur 
    if message == "fin":
        break
    message = transformation.str_to_int(message) #On transforme son message en int 
    message = rsa.encrypt_rsa(message, (int(n_B), int(e_B))) #On chiffre son message avec rsa 
    message = str(message)

    message = message.encode()
    connexion_avec_serveur.send(message)

    msg_recu = connexion_avec_serveur.recv(2048)
    if msg_recu == b"":
        print("ok")
    i = len(message_B)
    msg_recu = msg_recu.decode()
    msg_recu = rsa.decrypt_rsa(int(msg_recu), keys[i][1]) 
    msg_recu = transformation.int_to_str(msg_recu) 
    message_B.append(msg_recu)
    print(msg_recu)

    print(message_B)
print("Fermeture de la connexion")
connexion_avec_serveur.close()




