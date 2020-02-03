from unicorn import * 
from unicorn.x86_const import * 
from pwn import * 
from Crypto.Util.number import long_to_bytes , bytes_to_long 
import itertools 
from os import urandom 
BASE = 0x400000
STACK_ADDR = 0x600000
STACK_SIZE = 1024 * 1024 
start = BASE + 0x528
stop = BASE + 0x53F 
str1 = 0x600832 

buff = 0x600770 

# convert from 'a' -> '\x01\x00\x00\x00\x00\x01\x01\x00'
def convert(payload) :      
    string = "" 
    for c in payload : 
        string += bin2str(bin(ord(c))[2:][::-1].ljust(8, '0')) 
    return string 


# convert from '\x01\x00\x00\x00\x00\x01\x01\x00' -> 'a'
def re_convert(payload) :     
    string = "" 
    payload += "\x00" * (8 - len(payload) % 8) 
    for i in range(0, len(payload), 8) : 
        string += chr(int(str2bin(payload[i:i+8][::-1]),2))
    return string 

def bindiff(str1, str2) :
    count = 0  
    for i in range(46) : 
        if str1[i] != str2[i] : 
            return count  
        count += 1 
    return count 

def bin2str(bin) : 
    return "".join(map(chr, map(int , list(bin)))) 

def str2bin(string) : 
    return "".join(map(str, map(ord, list(string)))) 

def byte2bin(byte) : 
    return "".join(map(str, list(byte))) 

def emulate(payload) :  
    mu = Uc(UC_ARCH_X86, UC_MODE_64) 

    # map memory 
    mu.mem_map(BASE, 1024 * 1024) 
    mu.mem_map(STACK_ADDR, STACK_SIZE) 

    def hook_code(mu, address, size, user_data):  
        global old_rsi 
        global found 
        global target_bits 
        global raw_input
        machine_code = mu.mem_read(address, size) 
        if bytes_to_long(machine_code[1:][::-1]) + address - 0x4000B0 == 0xfffffffb :  # if call sub_4000B0
            rsi = mu.reg_read(UC_X86_REG_RSI)
            if rsi > old_rsi  :  # if we just pass old position 
                if return_value[address] == int(target_bits) :    # come to function set true value 
                    # print("[***] RSI = " + hex(rsi)) 
                    raw_input = payload[:rsi - 0x600780]    # rsi - 0x600780 is the number byte effect to this state
                    old_rsi = rsi  
                    found = True 
                    # print(repr(re_convert(raw_input)))
                    # test(re_convert(raw_input))     # some test
                mu.reg_write(UC_X86_REG_RIP, stop) # quit 
                # mu.reg_write(UC_X86_REG_RIP)

    mu.hook_add(UC_HOOK_CODE, hook_code)
    mu.mem_write(BASE, read("./baby_bear"))      # load binary into memory 

    mu.mem_write(0x600780 ,payload) 

    mu.emu_start(start, stop)  

def test(test) : 
    mu = Uc(UC_ARCH_X86, UC_MODE_64) 

    # map memory 
    mu.mem_map(BASE, 1024 * 1024) 
    mu.mem_map(STACK_ADDR, STACK_SIZE) 
    # mu.hook_add(UC_HOOK_CODE, hook_code) 
    mu.mem_write(BASE, read("./baby_bear"))      # load binary into memory 
    mu.mem_write(buff, test)      # write String into stack to use later on 

    mu.reg_write(UC_X86_REG_RSI, buff)

    mu.emu_start(BASE + 0x4E1 , stop) 
    res = mu.mem_read(str1, 46) 
    # print(byte2bin(res))
    return byte2bin(res)

if __name__ == "__main__" : 
    sh = remote("138.68.67.161", 20005) 
    sh.recvuntil("Baby bear says:") 
    target = sh.recvuntil("\n").strip()
    print(sh.recv())
    print("[*] Target : " + target)

    return_value = {0x40010B: 1, 
                    0x400348: 1, 
                    0x400374: 0,
                    0x4003A5: 0,
                    0x4003B6: 0, 
                    0x4003CF: 0, 
                    0x400417: 1,
                    0x400463: 0, 
                    0x40047D: 1 
    } 
    print("Brute force.........") 
    old_rsi = 0x600780 
    # target = "1111001100101011100110001101000101001100011011"
    test_input = "" 
    raw_input = "" 
    bruteForce = map(lambda x: "".join(x) ,list(itertools.product('\x00\x01', repeat=4)))
    for target_bits in target : 
        # print("---------------------------------------")
        found = False   
        for b in bruteForce : 
            emulate(test_input + b) 
            if found : 
                break 
        assert len(raw_input) > len(test_input)
        test_input = raw_input
    # print(sh.recv())
    sh.sendline(re_convert(test_input))
    assert test(re_convert(test_input)) == target 
    #print(sh.recv())
    sh.interactive()
        




        


