from Crypto.Cipher import AES 
from base64 import b64encode  
from os import urandom 

KEY = 'hacmaohacmao1234' 
IV = urandom(16)
def pad(s) : 
    c = 16 - len(s) % 16
    s = s +  c * chr(c) 
    return s 

def encrypt(string) : 
    cipher = AES.new(KEY, AES.MODE_CBC, IV) 
    if "admin" in string : 
        return False 
    return b64encode(IV + cipher.encrypt(pad(string)))

def check(c) : 
    cipher = AES.new(KEY, AES.MODE_CBC, IV) 
    plaintext = cipher.decrypt(c) 
    if "admin" in plaintext : 
        print "Welcome admin." 
    else : 
        print "Go away hacker."
        
if __name__ == "__main__" : 
    print encrypt("admin")