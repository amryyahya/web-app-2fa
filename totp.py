import time, math

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

FieldMult  = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
              [0, 2, 4, 6, 8, 10, 12, 14, 3, 1, 7, 5, 11, 9, 15, 13],
              [0, 3, 6, 5, 12, 15, 10, 9, 11, 8, 13, 14, 7, 4, 1, 2],
              [0, 4, 8, 12, 3, 7, 11, 15, 6, 2, 14, 10, 5, 1, 13, 9],
              [0, 5, 10, 15, 7, 2, 13, 8, 14, 11, 4, 1, 9, 12, 3, 6],
              [0, 6, 12, 10, 11, 13, 7, 1, 5, 3, 9, 15, 14, 8, 2, 4],
              [0, 7, 14, 9, 15, 8, 1, 6, 13, 10, 3, 4, 2, 5, 12, 11],
              [0, 8, 3, 11, 6, 14, 5, 13, 12, 4, 15, 7, 10, 2, 9, 1],
              [0, 9, 1, 8, 2, 11, 3, 10, 4, 13, 5, 12, 6, 15, 7, 14],
              [0, 10, 7, 13, 14, 4, 9, 3, 15, 5, 8, 2, 1, 11, 6, 12],
              [0, 11, 5, 14, 10, 1, 15, 4, 7, 12, 2, 9, 13, 6, 8, 3],
              [0, 12, 11, 7, 5, 9, 14, 2, 10, 6, 1, 13, 15, 3, 4, 8],
              [0, 13, 9, 4, 1, 12, 8, 5, 2, 15, 11, 6, 3, 14, 10, 7],
              [0, 14, 15, 1, 13, 3, 2, 12, 9, 7, 6, 8, 4, 10, 11, 5],
              [0, 15, 13, 2, 9, 6, 4, 11, 1, 14, 12, 3, 8, 7, 5, 10]]

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
                sum ^= FieldMult[M[i][k]][X[k][j]]
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
    hashVal=0
    while(len(hex(hashVal))-2<N//S):
        ro=R_OUT
        for i in range(D):
            if ro<=0:break
            for j in range(D):
                if ro<=0: break
                hashVal = (hashVal << 4) | (State[i][j]&0xf)
                ro-=S
        State=permutation(State)
    return hashVal.to_bytes(10, 'big')

def hmac(key: bytes, message: bytes, hash_function):
    key = hash_function(key)
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
