from Crypto.Util.number import bytes_to_long
from Crypto.Util.number import long_to_bytes

def str_to_int(message): 
    """Fonction qui prends une string et qui renvoie un int
    message : string à transformer en int""" 

    message = ''.join(format(ord(i), '08b') for i in message)
    message = int(message, 2)
    return message


def int_to_str(message): 
    """Fonction qui prends un int et qui renvoie une string
    message : int à transformer en string"""

    message_bin = bin(message)[2:]
    
    while(len(message_bin) % 8 != 0):
        message_bin = '0' + message_bin

    res = [] 
    for i in range (0,(len(message_bin)),8):
        m = message_bin[i:i+8]
        res.append(chr(int(m, 2)))

    return "".join(res)


def int_to_hex(int):
    return hex(int)

def hex_to_int(hex): 
    return int(hex) 

def decoupage(message):
    L =  message.split()
    n = L[0]
    e = L[1]
    return n,e

