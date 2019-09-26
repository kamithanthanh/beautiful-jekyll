from oracle import *  

def xor(a, b) : 
    return  "".join([chr(ord(a[i]) ^ ord(b[i])) for i in range(len(a))]) 

"""
Length Extension Attack to CBC-MAC-hash 
Create 2 message with same hash from given string m1, m2 
""" 
def attack(m1, m2) :  
    mac_hash = CBC_MAC_hash(m1)  
    IV = mac_hash[:16] 
    hash1 = mac_hash[16:]   
    padd = xor(xor(hash1, IV), pad(m2)[:16])  
    forged_msg = pad(m1) + padd + m2[16:] 

    if CBC_MAC_hash(m2)[16:] == CBC_MAC_hash(forged_msg)[16:] : 
        print "OK" 
    else : 
        print "FAIL" 

if __name__ == "__main__" : 
    m1 = "Admin" 
    m2 = "Some thing not important"
    attack(m1, m2) 
