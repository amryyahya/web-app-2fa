import binascii
import time
import math

sbox = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
RC = [1, 3, 7, 14, 13, 11, 6, 12, 9, 2, 5, 10]
IC = [0, 1, 3, 6, 4]
M = [
    [1,2,9,9,2],
    [2,5,3,8,13],
    [13,11,10,12,1],
    [1,15,2,3,14],
    [14,14,8,5,12],
    ]
D=5
S=4
N=80
R=20
R_OUT=16

def fieldMult(a, b):
    x = a
    ret = 0
    for i in range(S):
        if (b>>i)&1:
            ret ^= x
        if (x>>(S-1))&1:
            x<<=1
            x^=0x3
        else:
            x<<=1
    return ret &(1<<S)-1

def addConstant(X, k):
    for i in range(D):
        X[i][0] = X[i][0] ^ RC[k] ^ IC[i]
    return X

def subCells(X):
    for i in range(D):
        for j in range(D):
            X[i][j]=sbox[X[i][j]]
    return X

def shiftRows(X):
    X_prime = [[0 for j in range(D)] for i in range(D)]
    for i in range(D):
        for j in range(D):
            new_col_index = (j + i) % D
            X_prime[i][j] = X[i][new_col_index]
    return X_prime

def mixColumnSerial(X):
    tmp=[0 for _ in range(D)]
    for j in range(D):
        for i in range(D):
            sum = 0
            for k in range(D):
                sum ^= fieldMult(M[i][k], X[k][j])
            tmp[i]=sum
        for i in range(D):
            X[i][j] = tmp[i]
    return X

def permutation(State):
    for i in range(12):
        State = addConstant(State, i)
        State = subCells(State)
        State = shiftRows(State)
        State = mixColumnSerial(State)
    return State

def padding(m, r):
    m = m << 1 | 1
    length = len(bin(m)) - 1
    m <<= r - length % r
    return m

def splitTo4BitsChunks(number):
    chunks = []
    while number > 0:
        chunk = number & 0xF
        chunks.append(chunk)
        number >>= S
    chunks.reverse()
    return chunks

def photon80(plain):
    State = [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,1],
             [4,1,4,1,0]]
    m=int.from_bytes(plain, byteorder='big')
    m=padding(m,R)
    m=splitTo4BitsChunks(m)
    for i in range(0,len(m),R//S):
        k=0
        m_index=i
        j=0
        for _ in range(0,R//S):
            if j==D:
                k+=1
                j=0
            State[k][j]=State[k][j]^m[m_index]
            j+=1
            m_index+=1
        State = permutation(State)
    hashVal=bytearray()
    while(len(hashVal)<N//S):
        ro=R_OUT
        for i in range(D):
            if ro<=0:break
            for j in range(D):
                if ro<=0: break
                hashVal.append(State[i][j])
                ro-=S
        State=permutation(State)
    return hashVal

def hmac(key: bytes, message: bytes, hash_function):
    block_size = 32
    key = key + b'\x00' * (block_size - len(key))
    inner_padding = bytes(x ^ 0x36 for x in key)
    outer_padding = bytes(x ^ 0x5C for x in key)
    inner_hash_input = inner_padding + message
    inner_hash = hash_function(inner_hash_input)
    outer_hash_input = outer_padding + inner_hash
    outer_hash = hash_function(outer_hash_input)
    return outer_hash

def getTOTP(secret_key):
    current_epoch = int(time.time())
    time_counter = math.floor(current_epoch/30)
    message = time_counter.to_bytes(8, byteorder='big')
    hmac_value = hmac(secret_key, message, photon80)
    offset = hmac_value[-1]%16
    truncated_hash = hmac_value[offset:offset+4]
    totp = int.from_bytes(truncated_hash, byteorder='big') % (10**6)
    return str(totp).zfill(6)