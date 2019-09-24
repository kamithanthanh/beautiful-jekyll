"""
Purpose : recovery Key  
Situation : get oracle encrypt and decryption
""" 

from oracle import *
from base64 import b64decode, b64encode 

def xor(a, b) : 
    return "".join([chr(ord(a[i]) ^ ord(b[i])) for i in range(len(a))]) 

def attack() : 
    # Step 1 : get ciphertext 
    payload = "A" * 48 
    ciphertext = b64decode(encrypt(payload)) 

    fake_ciphertext = ciphertext[:16] + "\x00" * 16 + ciphertext[:16] 
    fake_plaintext = decrypt(b64encode(fake_ciphertext))
    return xor(fake_plaintext[:16], fake_plaintext[32:48]) 

if __name__ == "__main__" : 
    KEY = attack()
    print KEY 
