import jpype

jpype.startJVM(classpath=['.'])
TOTPGenerator = jpype.JClass('TOTP')
secret_key = "jj4nbkFRCzKwvuAhgBOjoFhIi3k7Z3j8"
totp = TOTPGenerator.TOTP(secret_key)
print(totp)