#!/usr/bin/env python3
from Crypto.PublicKey import RSA, ECC
import json
from hashlib import sha256
from Crypto.Cipher import AES, PKCS1_OAEP
from base64 import b64decode
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import socket 
from base64 import * 

from server import * 


# key = RSA.importKey(open("rsapubkey.pem", "r").read() )


# key = ECC.generate(curve='P-256') 
# f = open("fakekey.pem", 'w') 
# f.write(key.export_key(format='PEM'))  

message = json.loads('{"aeskey": "nwmHkXTN/EjnoO5IzhpNwE3nXEUMHsNWFI7dcHnpxIIiXCO+dLCjR6TfqYfbL9Z6a7SNCKbeTFBLnipXcRoN6o56urZMWwCioVTsV7PHrlCU42cKX+c/ShcVFrA5aOTTjaO9rxTMxB1PxJqYyxlpNaUpRFslzj9LKH+g8hVEuP9lVMm7q4aniyOUgPrAxyn044mbuxPu6Kh+JHSt5dkmnPZGNfUDKCwvMKeilb5ZkLaW/EaoXXsJLh/wUinMROIqmD2dkiWnk10633sJIu1lEOUsiykYXtJcd3o/B2dfTx2/85C2J6IsIp3+jJne76AYryAONPSxuh+M0h1xCzNeQg==", "message": "6VCnnSOU1DBImyhlqt7SoEjRtmBxjmABFVmXYhlKDyc+NBlnZ3Hpj4EkLwydPGpHiAvr4R0zTXSyUnMk5N6fi0/BFZE=", "nonce": "Cems9uHF6mk=", "signature": "uhLCnBvGfdC1fVkGUKQ8zNp/fOXNnFxNuDEc7CDGEYSxnuZMoGqbEqMLguJqDdvHFSHoUrq2R9/+mfk8LHndhw==", "eccpubkey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEGww+NA3xHj4kCyztekLhmJVB62Hhq/oGDWwo4fxgZCgbODqD3vrMFFTGCWfO8ZyHtstuW+Yztpq94CnSNpJoug=="}')


def fake_signature(msg) : 
    eccpubkey = ECC.import_key(msg["eccpubkey"])
    h = SHA256.new(msg["aeskey"] + msg["nonce"] + msg["message"])
    sign = DSS.new(eccpubkey, 'fips-186-3')
    msg['signature'] = sign.sign(h) 
    return msg 

HOST = 'crypto1.ctf.nullcon.net'  # The server's hostname or IP address
PORT = 5001        # The port used by the server

def sendMsg(msg) : 
    msg = fake_signature(msg) 
    msg["nonce"] = b64encode(msg["nonce"]).decode()
    msg["message"] = b64encode(msg["message"]).decode()
    msg["aeskey"] = b64encode(msg["aeskey"]).decode()
    msg["signature"] = b64encode(msg["signature"]).decode()
    msg["eccpubkey"] = b64encode(msg["eccpubkey"]).decode()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.recv(1024)
        s.sendall(json.dumps(msg).encode() + b"\n")
        recpt = s.recv(1024).split(b'\n')
        assert recpt[0] == b'Here is your read receipt:' 
    return recpt[1]

"""
Recovery xor key   
"""
def xor(a, b) : 
    return bytes([ai ^ bi for (ai, bi) in zip(a,b)])
ciphertext = b64decode(message['message']) 
print(ciphertext)
flag = b"hackim20{digital_singatures_does_not_always_imp"
fake_message = xor(flag, ciphertext[:len(flag)])  

import progressbar
from string import ascii_lowercase , digits
printable = ascii_lowercase + "{}_" + digits
for _ in range(len(flag), len(ciphertext)) : 
    print(_)
    H = SHA256.new(bytes(len(fake_message) + 1)).hexdigest().encode()
    brute = list(map(lambda x : ord(x) ^ ciphertext[_], printable))
    for i in progressbar.ProgressBar(widgets=[progressbar.Counter(), ' ', progressbar.Percentage(), ' ', progressbar.Bar(), ' ', progressbar.ETA()])(brute) :
        message["nonce"] = b64decode(message["nonce"])
        message["aeskey"] = b64decode(message["aeskey"])
        message["signature"] = b64decode(message["signature"])
        message['eccpubkey'] = open("fakekey.pem","r").read().encode() 
        new_fake_message = fake_message + bytes([i]) 
        message['message'] = new_fake_message 
        recpt = sendMsg(message) 
        if recpt == H : 
            fake_message += bytes([i]) 
            flag = xor(fake_message, ciphertext[:_+1])
            print(flag)
            break  
