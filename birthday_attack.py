def getTOTP(secret_key, message):
    # current_epoch = int(time.time())
    # time_counter = math.floor(current_epoch/30)
    # message = time_counter.to_bytes(8, byteorder='big')
    hmac_value = hmac(secret_key, message)
    offset = (hmac_value[-1]%16)//2
    truncated_hash = hmac_value[offset:offset+4]
    totp = int.from_bytes(truncated_hash, byteorder='big') % (10**6)
    return str(totp).zfill(6)

import itertools
characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
compinations = itertools.product(characters, repeat=16)
for combo in compinations:
    alphanumericstr=''.join(combo)
    tried_secret = alphanumericstr.encode('utf-8')
    if getTOTP(tried_secret, message=b'\x00\x00\x00\x00\x03b\x85\xbf') == '930075':
        print(tried_secret)
