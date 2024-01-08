import ctypes,time,math,base64
from memory_profiler import profile

getTruncatedHMACPhoton = ctypes.CDLL('./photon160.so').getTruncatedHMACPhoton

def bytes_to_4bit_array(byte_sequence):
    return [int(format(byte, '08b')[i:i+4], 2) for byte in byte_sequence for i in range(0, 8, 4)]

def getTOTP(secret_key):
    current_epoch = int(time.time())
    time_counter = math.floor(current_epoch//30)
    message = bytes_to_4bit_array(time_counter.to_bytes(8, byteorder='big'))
    totp = getTruncatedHMACPhoton((ctypes.c_int * len(secret_key))(*secret_key), (ctypes.c_int * len(message))(*message), len(secret_key),len(message))
    return str(totp).zfill(6)

secret_key=bytes_to_4bit_array(base64.b32decode("N4fU6lWmUJ7fKJiUR7QgxiCsUURptqfd",True))

# s=time.time()
# totp=getTOTP(secret_key)
# e=time.time()
# print(e-s)
# print("TOTP:",totp)

@profile
def getMemoryUsage():
    getTOTP(secret_key)

if __name__ == '__main__':
    getMemoryUsage()