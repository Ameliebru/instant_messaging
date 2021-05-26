"""
AES de 128 bits 
"""

from data import * 

def bytes2matrix(text): 
    """ 
    text : 16-bytes 
    return une matrice 4*4 
    """
    return [list(text[i:i+4]) for i in range(0, len(text) , 4)]

def matrix2bytes(matrix):
    """
    matrix 4*4 
    return un 16-bytes 
    """
    res = b""
    for i in range(4):
        for j in range(4):
            res += bytes([matrix[i][j]])
    return res 
 

def sub_bytes(s, sbox=sBox):
    for i in range(len(s)):
        for j in range (len(s[i])): 
            s[i][j] = sbox[s[i][j]]

def shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]

def inv_shift_rows(s):
    s[1][1], s[2][1], s[3][1], s[0][1] = s[0][1], s[1][1], s[2][1], s[3][1] 
    s[2][2], s[3][2], s[0][2], s[1][2] = s[0][2], s[1][2], s[2][2], s[3][2] 
    s[3][3], s[0][3], s[1][3], s[2][3] = s[0][3], s[1][3], s[2][3], s[3][3] 
 
xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


def mix_single_column(a):
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)


def mix_columns(s):
    for i in range(4):
        mix_single_column(s[i])

def inv_mix_columns(s):
    for i in range(4):
        u = xtime(xtime(s[i][0] ^ s[i][2]))
        v = xtime(xtime(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v
    mix_columns(s)


def add_round_key(s, k):
    for i in range(4):
        for j in range(4):
            s[i][j] = s[i][j] ^ k[i][j]


N_ROUNDS = 10 

def expand_key(master_key):

    r_con = (
        0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
        0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
        0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
        0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
    )

    key_columns = bytes2matrix(master_key)
    iteration_size = len(master_key) // 4
    columns_per_iteration = len(key_columns)
    i = 1
    while len(key_columns) < (N_ROUNDS + 1) * 4:
        word = list(key_columns[-1])

        if len(key_columns) % iteration_size == 0:
            word.append(word.pop(0))
            word = [sBox[b] for b in word]
            word[0] ^= r_con[i]
            i += 1
        elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
            word = [sBox[b] for b in word]

        word = bytes(i^j for i, j in zip(word, key_columns[-iteration_size]))
        key_columns.append(word)

    return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]


def decrypt(key, ciphertext):
    round_keys = expand_key(key) 

    # On convertit le bytes en matrice
    state = bytes2matrix(ciphertext)
    # Initialisation de la cle 
    add_round_key(state,round_keys[10]) 
    for i in range(N_ROUNDS - 1, 0, -1): 
        inv_shift_rows(state)
        sub_bytes(state, inverse_sBox)
        add_round_key(state,round_keys[i]) 
        inv_mix_columns(state)

    # Tour final 
    inv_shift_rows(state)
    sub_bytes(state, inverse_sBox)
    add_round_key(state,round_keys[0]) 
    # On convertir la matrice en buytes
    plaintext = matrix2bytes(state)
    return plaintext

def encrypt(key, plaintext):
    round_keys = expand_key(key) #
    state = bytes2matrix(plaintext)
    add_round_key(state,round_keys[0]) 
    for i in range(N_ROUNDS - 1): 
        sub_bytes(state, sBox)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state,round_keys[i+1]) 

    sub_bytes(state, sBox)
    shift_rows(state)
    add_round_key(state,round_keys[10]) 
    cipher = matrix2bytes(state)
    return cipher

