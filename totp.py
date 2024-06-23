import ctypes
lib = ctypes.CDLL('./totp-hmac-photon.so')
lib.getTOTP.restype = ctypes.c_int
lib.getTOTP.argtypes = [ctypes.c_char_p]

def getTOTP(secret_key):
    totp = lib.getTOTP(secret_key)
    # print(totp)
    return str(totp).zfill(6)
    
print(getTOTP(b'jhEx7lBWMIdwgJf3IAzALauy4pOe4MqC'))
print(getTOTP(b'jhEx7lBWMIdwgJf3IAzALauy4pOe4MqC'))

print(getTOTP(b'jhEx7lBWMIdwgJf3IAzALauy4pOe4MqC'))
