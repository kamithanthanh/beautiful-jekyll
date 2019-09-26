from Crypto.Cipher import AES  
from os import urandom 

KEY = "hacmaohacmao1234" 
IV = urandom(16)
def pad(s) : 
    c = 16 - len(s) % 16 
    return s + chr(c) * c  

def CBC_MAC(msg) : 
    cipher = AES.new(KEY, AES.MODE_CBC, IV) 
    mac = cipher.encrypt(pad(msg))[-16 :] 
    return msg + IV + mac 

def CBC_MAC_hash(msg) : 
    cipher = AES.new(KEY, AES.MODE_CBC, IV) 
    mac = cipher.encrypt(pad(msg))[-16 :] 
    return IV + mac  


if __name__ == "__main__" : 
    msg = "Hello hacmao" 
    msg_mac = CBC_MAC(msg) 
