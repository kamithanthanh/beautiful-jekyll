from pwn import *

def debug(idx) :
    cmd = """
    """
    context.terminal = ['tmux', 'splitw', '-h']

    if int(args.GDB) == idx:
        print('lol')
        gdb.attach(p, cmd)

def conn(binary) :
    if args.LOCAL :
        p = process(binary)
        e = p.elf
        libc = p.libc

    elif args.REMOTE :
        host = ""
        port = 0x0
        e = ELF(binary)
        libc = ELF("")
        p = remote(host, port)

    else :
        v = "2.30"
        libc = f"/glibc/{v}/64/lib/libc-{v}.so"
        ld = f"/glibc/{v}/64/lib/ld-{v}.so"
        p = process([ld, binary], env={"LD_PRELOAD" : libc})
        e = p.elf
        libc = p.libc
    return (p, e, libc)

def exploit() :
    global p, e, libc 
    p, e, libc = conn("./chall")

    debug(0)

    p.interactive()

if __name__ == "__main__" :
    p, e, libc = ("", "", "")
    exploit()
