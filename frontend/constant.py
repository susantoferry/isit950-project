from cryptography.fernet import Fernet
import base64

restServer = 'http://localhost:8000/api/'

fernetKey = 'p58QlMoA_F3QEzQSBfhHA7tQzxFHElbgbxsjDPKPQ10='

def encryptString(value):
    fernet = Fernet(fernetKey)
    val = fernet.encrypt(value.encode())
    valBase64 = base64.urlsafe_b64encode(val).decode()

    return valBase64

def decryptString(value):
    fernet = Fernet(fernetKey)
    # val = fernet.decrypt(repr(value)[2:-1]).decode()
    valBase64 = base64.urlsafe_b64decode(value)
    val = fernet.decrypt(valBase64).decode()
    

    return val
