'''Byte-at-a-time ECB decryption (Harder)
AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)
attack to find target-bytes
In this challenge I use a random-prefix with length 3-10 , if it greater just need do some ez step ''' 
from Crypto.Cipher import AES 
from os import urandom 
from random import randint 

random_prefix = urandom (randint(3,10)) 
targets_bytes = urandom(randint(3,10))

def PKCS7(m,length):
    ch = length - len(m) % length 
    return m + bytes([ch]) * ch  

def unPad(c):
    return c[:-c[-1]] 

def encrypt_oracle (s):
    s = random_prefix + s + targets_bytes
    s = PKCS7(s,16)
    cipher = AES.new(key,AES.MODE_ECB)
    return cipher.encrypt(s) 

def length_detect(encrypt_oracle):
    for length in range(2,41):
        s = b'0' * (3*length) 
        encode_s = encrypt_oracle(s)
        if encode_s[2*length : 3*length] == encode_s[length : 2*length]:
            return length
            
def detect_length_prefix(encrypt_oracle):
    s1 = b'0'
    s2 = b'1'
    length = 15 
    while True : 
        e_s1 = encrypt_oracle(s1)
        e_s2 = encrypt_oracle(s2) 
        if e_s1[16:32] != e_s2[16:32] :  # when s1 + prefix is a block 
            return length + 1
        length -= 1 
        s1 = b'0' + s1 
        s2 = b'0' + s2 
    
def detect_length_suffix_prefix(encrypt_oracle):
    s = b""
    l1 = len(encrypt_oracle(s)) 
    l2 = l1 
    i = 0 
    while l2 == l1 : 
        s += b"0"
        l2 = len(encrypt_oracle(s))
        i+= 1 
    return l1 - i 

def next_bytes(knowbytes,encrypt_oracle):
    string = b"0" * (KEYSIZE - len_prefix) + b"0" * (KEYSIZE - len(knowbytes) % KEYSIZE - 1 ) 
    encode_s = encrypt_oracle(string)
    for ch in range(256):
        string_guess = string + knowbytes + bytes([ch])
        encode_s_guess = encrypt_oracle(string_guess)
        if encode_s_guess[:len(string_guess) ] == encode_s[:len(string_guess)]:
            return bytes([ch])

def attack() : 
    print("[*] attack to find suffix.........")
    knowbytes = b""
    for i in range(len_target):
        knowbytes += next_bytes(knowbytes,encrypt_oracle)
    return knowbytes 

key = urandom(16)          
if __name__ == "__main__": 
    global KEYSIZE 
    print("[*] detect keysize........")
    KEYSIZE = length_detect(encrypt_oracle)
    print("KEYSIZE = %d" % KEYSIZE)

    print("[*] Detecting prefix length.......")
    len_prefix = detect_length_prefix(encrypt_oracle)
    assert len_prefix == len(random_prefix)
    print("Prefix length is %d " % len_prefix)

    print("[*] Detecting target length........")
    len_target = detect_length_suffix_prefix(encrypt_oracle) - len_prefix
    assert len_target == len(targets_bytes)
    print("Target length is %d " %  len_target)

    print(attack())
