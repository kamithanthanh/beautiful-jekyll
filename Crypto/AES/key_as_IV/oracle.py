# python2 

from Crypto.Cipher import AES 
from base64 import b64encode, b64decode 

def pad(s) : 
    c = 16 - len(s) % 16 
    return s + c * chr(c) 
key = "hacmaohacmao1234" 
IV = key 

def encrypt(string) :  
    cipher = AES.new(key, AES.MODE_CBC, IV) 
    return b64encode(cipher.encrypt(pad(string))) 

def decrypt(c) : 
    cipher = AES.new(key, AES.MODE_CBC, IV) 
    return cipher.decrypt(b64decode(c)) 




