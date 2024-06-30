import jpype

jpype.startJVM(classpath=['.'])
TOTPGenerator = jpype.JClass('TOTP')
secret_key = "rDeaUyAbteB7fvdO2IGfE5PIsn9e2hTm"
totp = TOTPGenerator.TOTP(secret_key)
print(totp)