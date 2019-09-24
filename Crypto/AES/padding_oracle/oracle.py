from Crypto.Cipher import AES 
from base64 import b64encode, b64decode 
from os import urandom 

key = urandom(16) 
IV = urandom(16) 

def pad(s) : 
    c = 16 - len(s) % 16 
    return s + c * chr(c) 

def encrypt(s) : 
    cipher = AES.new(key, AES.MODE_CBC, IV) 
    return b64encode(IV + cipher.encrypt(pad(s))) 

def decrypt(c) : 
    cipher = AES.new(key, AES.MODE_CBC, IV) 
    return cipher.decrypt(b64decode(c)[16:]) 

def padding_oracle(c) : 
    m = decrypt(c) 
    LB = ord(m[-1])   
    return m[-LB :] == chr(LB) * LB

def padding_oracle2(c) : 
    m = decrypt(c) 
    LB = ord(m[-1])   
    return LB

if __name__ == "__main__" : 
    # Test padding oracle 
    m = "a" * 16 
    c = encrypt(m)  
    print padding_oracle(c) 

   
