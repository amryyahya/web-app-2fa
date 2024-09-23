import jpype
jpype.startJVM(classpath=['.'])

def getTOTP(secret_key,time):
    TOTPGenerator = jpype.JClass('TOTP')
    totp = TOTPGenerator.TOTP(secret_key,time)
    return totp

obtained_totp = "841586"
obtained_time = 1719885656

import itertools
def birthday_attack():
    characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    combinations = itertools.product(characters, repeat=32)
    getPossibleSecret = False
    for combo in combinations:
        alphanumericstr=''.join(combo)
        tried_secret = alphanumericstr.encode('utf-8')
        tried_secret = b'gbOJmc8at8frcro1bV8MxD2ChcIg99ZV'
        print(tried_secret)
        if getTOTP(tried_secret, obtained_time) == obtained_totp:
        with open("possible_secret.txt", "a") as file:
            file.write(tried_secret.decode('utf-8')+"\n")
            return True

birthday_attack()
