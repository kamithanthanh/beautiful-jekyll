from Crypto.Cipher import AES 
from os import urandom 

KEY = "hacmaohacmaohacc"

def pad(msg) : 
    c = 16 - len(msg) % 16 
    return msg + chr(c) * c  

"""
CBC-MAC : CBC - Messages authenticate code  
Encode msg input by CBC then return msg + IV + MAC   
"""
def CBC_MAC(msg) : 
    IV =  urandom(16)
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    MAC = cipher.encrypt(pad(msg))[-16:]                  
    return msg + IV + MAC  

def confirm(msg_mac) : 
    iv = msg_mac[-32 : -16]  
    mac = msg_mac[-16:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)  
    mac2 = cipher.encrypt(pad(msg_mac[: -32]))[-16 :] 
    if mac == mac2 : 
        return 1 
    else : 
        return 0 

if __name__ == "__main__" : 
    print "Testing CBC-MAC ..........."  
    msg_mac = CBC_MAC("hacmao"*3) 
    if confirm(msg_mac) : 
        print "OK" 
    else : 
        print "NO"