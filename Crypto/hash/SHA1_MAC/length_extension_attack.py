''' Break a SHA-1 keyed MAC using length extension
SHA1(key || original-message || glue-padding || new-message)
SHA1(key || original-message || gluepadding) = old-hash
There are 3 things you want to know : 
1 - padding "1" and "0" 
2 - length padding to the end 
3 - the hash base on h value so change h to change hash''' 
from Crypto.Util.number import long_to_bytes
from Crypto.Random import urandom 
from random import randint 
from binascii import hexlify 
import struct 
import time 

def padSHA1 (message):
    ''' just copy from SHA1 ''' 
    length = bin(len(message) * 8)[2:].rjust(64, "0")
    ''' padding to enough 512 bit block ''' 
    message = ''.join(bin(i)[2:].rjust(8, "0") for i in message) + "1"
    padding = "1" + "0" * ((448 - len(message) % 512) % 512) + length
    padding_bytes = b"" 
    for i in range(len(padding) // 8):
        padding_bytes += bytes([int(padding[8*i:8*(i+1)],2)])  
    return padding_bytes

class SHA1_fixed :
    def __init__(self, message,_h0 = 0x67452301,_h1= 0xefcdab89,_h2 = 0x98badcfe,_h3 = 0x10325476,_h4 = 0xc3d2e1f0,length = None):
        self._h0 = _h0 
        self._h1 = _h1 
        self._h2 = _h2 
        self._h3 = _h3 
        self._h4 = _h4 
        if length == None : 
            length = len(message) * 8 
        length = bin(length)[2:].rjust(64, "0")
        while len(message) > 64:
            self._handle(''.join(bin(i)[2:].rjust(8, "0")
                for i in message[:64]))
            message = message[64:]
        ''' padding to enough 512 bit block ''' 
        message = ''.join(bin(i)[2:].rjust(8, "0") for i in message) + "1"
        message += "0" * ((448 - len(message) % 512) % 512) + length
        for i in range(len(message) // 512):
            self._handle(message[i * 512:i * 512 + 512])

    def _handle(self, chunk):

        lrot = lambda x, n: (x << n) | (x >> (32 - n))
        w = []

        for j in range(len(chunk) // 32):
            w.append(int(chunk[j * 32:j * 32 + 32], 2))

        for i in range(16, 80):
            w.append(lrot(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)
                & 0xffffffff)

        a = self._h0
        b = self._h1
        c = self._h2
        d = self._h3
        e = self._h4

        for i in range(80):

            if i <= i <= 19:
                f, k = d ^ (b & (c ^ d)), 0x5a827999
            elif 20 <= i <= 39:
                f, k = b ^ c ^ d, 0x6ed9eba1
            elif 40 <= i <= 59:
                f, k = (b & c) | (d & (b | c)), 0x8f1bbcdc
            elif 60 <= i <= 79:
                f, k = b ^ c ^ d, 0xca62c1d6

            temp = lrot(a, 5) + f + e + k + w[i] & 0xffffffff
            a, b, c, d, e = temp, a, lrot(b, 30), c, d

        self._h0 = (self._h0 + a) & 0xffffffff
        self._h1 = (self._h1 + b) & 0xffffffff
        self._h2 = (self._h2 + c) & 0xffffffff
        self._h3 = (self._h3 + d) & 0xffffffff
        self._h4 = (self._h4 + e) & 0xffffffff

    def _digest(self):
        return (self._h0, self._h1, self._h2, self._h3, self._h4)

    def hexdigest(self):
        return ''.join(hex(i)[2:].rjust(8, "0")
            for i in self._digest())

    def digest(self):
        hexdigest = self.hexdigest()
        return bytes(int(hexdigest[i * 2:i * 2 + 2], 16)
            for i in range(len(hexdigest) // 2))

def MAC_SHA1(key, message):
    return SHA1_fixed(key + message).digest() 

def forged_message(keylen,message,suffix):
    glue_padding = padSHA1(b"0" * keylen + message) 
    forged_message = message + glue_padding + suffix 
    return forged_message

def forged_hash(keylen,message,hash_,suffix):
    h = []
    Forged_message = forged_message(keylen,message,suffix)
    for i in range(5):
        hi = hash_[4*i:4*(i+1)]
        hi = int(hexlify(hi),16)  
        h.append(hi)
    length = len(b"0" * keylen + Forged_message) * 8 
    forged_hash = SHA1_fixed(suffix,h[0],h[1],h[2],h[3],h[4],length).digest() 
    return forged_hash 

def validate_hash(message,hash_): 
    if MAC_SHA1(key,message) == hash_ : 
        return True 
    else : 
        return False 

if __name__ == '__main__':
    key = urandom(randint(1,100))
    print("length real key = %d " % len(key))
    message = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon" 
    suffix = b";admin=true" 
    hash_ = MAC_SHA1(key,message) 
    for keylen in range(100): 
        print("[*] Try to break with key len : %d" % keylen)
        Forged_hash = forged_hash(keylen,message,hash_,suffix) 
        Forged_message = forged_message(keylen,message,suffix) 
        if validate_hash(Forged_message,Forged_hash):
            print("Log in as Admin!")   
            print("[*] [*] [*] key len recovery : %d" % keylen)
            break 
        else : 
            print("Log in as User!") 
            time.sleep(1)   #it will more fun when you wait :v 
