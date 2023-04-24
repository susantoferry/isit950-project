from cryptography.fernet import Fernet

restServer = 'http://localhost:8000/api/'

fernetKey = 'p58QlMoA_F3QEzQSBfhHA7tQzxFHElbgbxsjDPKPQ10='

def encryptString(value):
    fernet = Fernet(fernetKey)
    val = fernet.encrypt(value.encode())

    return val

def decryptString(value):
    fernet = Fernet(fernetKey)
    val = fernet.decrypt(repr(value)[2:-1]).decode()

    return val