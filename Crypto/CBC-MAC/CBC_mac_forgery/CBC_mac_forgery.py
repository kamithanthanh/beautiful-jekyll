
from oracle import * 

def xor(a, b) : 
    return "".join([chr(ord(a[i]) ^ ord(b[i])) for i in range(len(a))]) 

def attack(msg, target) :  
    assert len(target) <= 16  
    msg_MAC1 = CBC_MAC(msg) 
    IV = msg_MAC1[-32 : -16]    
    MAC1 = msg_MAC1[-16 :]    
    target = target.ljust(16, "\x00")  
    forged_msg = target + msg[16 :]
    IV_forged = xor(xor(target, msg[: 16]), IV)     
    if confirm(forged_msg + IV_forged + MAC1) : 
        print "OK"   
    else :  
        print "FAIL" 

if __name__ == "__main__" : 
    msg = "I'm not adminnnnnnnnnnnnnn"  
    target = "I'm admin" 
    attack(msg, target) 


    