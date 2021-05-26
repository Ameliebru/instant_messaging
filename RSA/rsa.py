import math
from sympy import *
import random

def encrypt_rsa(m, pk):
    """Fonction qui chiffre un message avec RSA

    m :  message en int à chiffrer 
    pk : couple N, e
    
    retourne m**e % N """ 

    N, e = pk

    return pow(m, e, N)


def decrypt_rsa(c, sk):
    """Fonction qui dechiffre un message avec RSA

    m :  message en int à déchiffrer 
    sk : p, q, d 
    
    retourne m**d % p*q  """

    p, q, d = sk

    return pow(c, d, p * q) 

def bezout(a, b):
    """Int a and b 
    Return d = a*u + b*v 

    """
    (d, r) = (a, b)
    (u, s) = (1, 0)
    (v, t) = (0, 1)

    while r != 0:
        quotient = d // r
        (d, r) = (r, d - quotient * r)
        (u, s) = (s, u - quotient * s)
        (v, t) = (t, v - quotient * t)
    return d, u,v 

def key_rsa(t):
    """ t taille de la clé
    return clé publique et privée""" 
    
    inf = 2**((t // 2  - 1))
    maxi = 2**(t// 2 +1 ) - 1
    N = 1
    while math.log(N) / math.log(2) < t: 
        p = randprime(inf, maxi)
        q = randprime(inf, maxi)
        if p == q: 
            q = randprime(inf, maxi)
        N = p * q
    
    phi = (p - 1)*(q - 1)
    e = random.randint(1, phi)
    while(gcd(phi,e) != 1):
        e = random.randint(1, phi)
    _, u, _ = bezout(e, phi)
    d = u % phi
    return [N, e], [int(p), int(q), int(d)]
