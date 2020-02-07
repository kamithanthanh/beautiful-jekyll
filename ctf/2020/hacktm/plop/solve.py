from pwn import * 

# def get_PIE(proc):
#     memory_map = open("/proc/{}/maps".format(proc.pid),"rb").readlines()
#     return int(memory_map[0].split("-")[0],16)

# def debug(bp):
#     #bp = [0xea0,0xd31,0xc52]
#     #bp = [0x00000dfb,0x00000b7c,0x00000d10]
#     script = ""
#     PIE = get_PIE(sh)
#     PAPA = PIE
#     for x in bp:
#         script += "b *0x%x\n"%(PIE+x)
#     script += "handle SIGSEGV noprint noignore\n" 
#     script += "handler SIGALARM noprint noignore\n"
#     gdb.attach(sh,gdbscript=script) 

# context.terminal = ['tmux', 'splitw', '-h']
# sh = process("./plop") 

# debug([0x15b2])
# sh.interactive()
def rol(num, s) : 
    num = bin(num)[2:].rjust(64, "0") 
    num = int(num[s:] + num[:s], 2) 
    return num

def ror(num, s) : 
    num = bin(num)[2:].rjust(64, "0")  
    num = int(num[-s:] + num[:-s], 2) 
    return num

from z3 import * 
for c in range(256) : 
    print(c)
    s = Solver()
    flag = [BitVec("flag%i" % i, 64) for i in range(8)] 

    t1 = RotateLeft(flag[0], 0xe) ^ 0xdc3126bd558bb7a5 
    s.add(RotateRight(flag[1] ^ 0x76085304e4b4ccd5, 0x28) == t1) 

    s.add(RotateLeft(flag[2], 0x3e) ^ 0x1cb8213f560270a0 == t1) 
    s.add(RotateLeft(flag[3], 2) ^ 0x4ef5a9b4344c0672 == t1) 
    s.add(RotateRight(flag[4] ^ 0xe28a714820758df7, 0x2d) == t1) 
    s.add(RotateLeft(flag[5], 0x27) ^ 0xa0d78b57bae31402 == t1) 
    s.add(RotateRight(rol(0x4474f2ed7223940, 0x35) ^ flag[6], 0x35) == t1) 
    s.add(RotateRight(t1 ^ 0xb18ceeb56b236b4b, 0x19) == flag[7]) 

    s.add(Extract(7,0,flag[0]) == ord('H'))
    s.add(Extract(15,8,flag[0]) == ord('a'))
    s.add(Extract(23,16,flag[0]) == ord('c'))
    s.add(Extract(31,24,flag[0]) == ord('k'))
    s.add(Extract(39,32,flag[0]) == ord('T'))
    s.add(Extract(47,40,flag[0]) == ord('M'))
    s.add(Extract(55,48,flag[0]) == ord('{'))
    s.add(Extract(63,56,flag[0]) == c)

    def pp(t):
        return binascii.unhexlify(hex(t)[2:].zfill(16))[::-1]

    s.check()
    m = s.model()

    print(''.join([pp(m[x].as_long()) for x in flag]))

