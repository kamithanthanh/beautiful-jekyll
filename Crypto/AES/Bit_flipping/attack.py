from oracle import * 
from base64 import b64decode 

def attack() : 
    payload = "Admin" 
    cipher = b64decode(encrypt(payload))
    cipher = chr(ord(cipher[0]) ^ ord("A") ^ ord("a")) + cipher[1:] 
    check(cipher)

if __name__ == "__main__" : 
    attack()

