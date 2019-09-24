"""
Target : recovery plaintext from ciphertext without know key 
Situation : padding oracle 
"""

from oracle import * 
from base64 import b64decode, b64encode 
from os import urandom 

def attack(c) :   
    c = b64decode(c) 
    plaintext = ""
    for i in range(1, len(c) / 16) :     
        block_random = urandom(16)  
        block_prev = c[16*(i-1) : 16*i] 
        target = c[16*i : 16*(i+1)]  
        part = [' '] * 16 

        # generate random block_prev for get valid padding end up with 1 
        for j in range(256) : 
            fake_ciphertext = "a" * 16 + block_random[:15] + chr(j) + target 
            valid = padding_oracle(b64encode(fake_ciphertext))
            if valid : 
                fake_ciphertext = "a" * 16 + block_random[:14] + chr((j+1) % 256) + chr(j) + target
                valid2 = padding_oracle(b64encode(fake_ciphertext))
                if valid2 :
                    # check for valid end is '\x01'  
                    part[-1] = chr(ord(block_prev[-1]) ^ j ^ 1) 
                    break  
        
        # break remainning flag 
        block_random = list(block_random[:-1] + chr(j))   
        for k in range(2,17) : 
            for j in range(1, k) : 
                block_random[-j] = chr(ord(block_random[-j]) ^ (k-1) ^ k) 
            for j in range(256) : 
                fake_ciphertext = "a" * 16 + "".join(block_random[:16-k] + [chr(j)] + block_random[16-k+1:]) + target 
                valid = padding_oracle(b64encode(fake_ciphertext)) 
                if valid :  
                    block_random[-k] = chr(j) 
                    part[-k] = chr(ord(block_prev[-k]) ^ j ^ k) 
                    break  
        plaintext += "".join(part) 
        print plaintext  

if __name__ == "__main__" : 
    flag = "FLAG{this_is_ez_oracle_somethingesle}" 
    flag_enc = encrypt(flag) 
    attack(flag_enc)  

