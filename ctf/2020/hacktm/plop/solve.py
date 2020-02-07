from pwn import * 

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
    script += "handle SIGSEGV noprint noignore pass\n" 
    script += "handle SIGALRM noprint noignore pass\n"
    gdb.attach(sh,gdbscript=script) 

# context.terminal = ['tmux', 'splitw', '-h']
# with context.verbose : 
#     sh = process("./plop") 

#     debug([0x15b2])
#     sh.interactive()
def rol(num, s) : 
    num = bin(num)[2:].rjust(64, "0") 
    num = int(num[s:] + num[:s], 2) 
    return num

def ror(num, s) : 
    num = bin(num)[2:].rjust(64, "0")  
    num = int(num[-s:] + num[:-s], 2) 
    return num

# handle SIGSEGV noignore noprint pass 
# handle SIGALRM noignore noprint pass 
# handle SIGTRAP noignore noprint nopass 
#  b * 0x80015b2
from z3 import * 
import binascii
from string import printable 
def is_printable(s) : 
    for _ in s : 
        if _ not in printable : 
            return False 
    return True 

for c in printable : 
    print(c)
    s = Solver()
    flag = [BitVec("flag%i" % i, 64) for i in range(8)] 

    t1 = RotateLeft(flag[0], 0xe) ^ 0xdc3126bd558bb7a5 

    s.add(RotateRight(t1 ^ 0x76085304e4b4ccd5, 0x28) == flag[1])
    t2 = RotateLeft(flag[1], 0x28) ^ 0x76085304e4b4ccd5 

    s.add(RotateLeft(flag[2], 0x3e) ^ 0x1cb8213f560270a0 == t2) 
    s.add(RotateLeft(flag[3], 2) ^ 0x4ef5a9b4344c0672 == t2) 

    s.add(RotateRight(t2 ^ 0xe28a714820758df7, 0x2d) == flag[4]) 
    t3 = RotateLeft(flag[4], 0x2d) ^ 0xe28a714820758df7 

    
    s.add(RotateLeft(flag[5], 0x27) ^ 0xa0d78b57bae31402 == t3) 
    s.add(RotateRight(rol(0x4474f2ed7223940, 0x35) ^ flag[6], 0x35) == t3) 
    s.add(RotateRight(t1 ^ 0xb18ceeb56b236b4b, 0x19) == flag[7]) 

    s.add(Extract(7,0,flag[0]) == ord('H'))
    s.add(Extract(15,8,flag[0]) == ord('a'))
    s.add(Extract(23,16,flag[0]) == ord('c'))
    s.add(Extract(31,24,flag[0]) == ord('k'))
    s.add(Extract(39,32,flag[0]) == ord('T'))
    s.add(Extract(47,40,flag[0]) == ord('M'))
    s.add(Extract(55,48,flag[0]) == ord('{'))
    s.add(Extract(63,56,flag[0]) == ord(c))

    def pp(t):
        return binascii.unhexlify(hex(t)[2:].zfill(16))[::-1]

    s.check()
    m = s.model()

    if is_printable(''.join([pp(m[x].as_long()) for x in flag])) : 
        print (''.join([pp(m[x].as_long()) for x in flag]))

