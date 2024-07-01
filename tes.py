import jpype

jpype.startJVM(classpath=['.'])
TOTPGenerator = jpype.JClass('TOTP')
secret_key = "Ebcj6NCFkxBhQj3dzfmsSaJ4pSgAO9GS"
totp = TOTPGenerator.TOTP(secret_key)
print(totp)