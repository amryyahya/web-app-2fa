import jpype

jpype.startJVM(classpath=['.'])
TOTPGenerator = jpype.JClass('TOTP')
secret_key = "gbOJmc8at8frcro1bV8MxD2ChcIg99ZV"
time = 1719885656
totp = TOTPGenerator.TOTP(secret_key,time)
print(totp)