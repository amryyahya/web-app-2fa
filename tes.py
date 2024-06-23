import ctypes

# Load the shared library
# On Linux/macOS
lib = ctypes.CDLL('./totp-hmac-photon.so')
# On Windows
# lib = ctypes.CDLL('./totp.dll')

# Define the argument and return types of the C function
lib.getTOTP.argtypes = [ctypes.c_char_p]
lib.getTOTP.restype = ctypes.c_int

# Function to call the C function
def get_totp(keystring):
    # Convert the Python string to a C string
    keystring_c = ctypes.c_char_p(keystring.encode('utf-8'))
    # Call the C function and get the result
    result = lib.getTOTP(keystring_c)
    return result

# Example usage
key = "example"
totp = get_totp(key)
print(f"The TOTP for key '{key}' is: {totp}")
totp = get_totp(key)
print(f"The TOTP for key '{key}' is: {totp}")
totp = get_totp(key)
print(f"The TOTP for key '{key}' is: {totp}")

# print(oll(b'jhEx7lBWMIdwgJf3IAzALauy4pOe4MqC'))
# print(oll(b'jhEx7lBWMIdwgJf3IAzALauy4pOe4MqC'))

