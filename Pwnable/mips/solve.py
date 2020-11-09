
from pwn import *
from pwnlib.util import misc
import tempfile
from time import sleep

def pwndbg(script=b"") :
    tmp = tempfile.NamedTemporaryFile(prefix = 'pwn', 
        suffix = '.gdb', delete = False)
    tmp.write(b"""
    set architecture mips
    set endian little
    target remote localhost:9999
    """ + script + b"\n")
    if args.GDB : 
        misc.run_in_new_terminal('gdb-multiarch -q  -x "%s"' % tmp.name)

context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

p = remote('localhost', 9998)
pause()
cmd = b"""
"""
pwndbg(cmd)

p.interactive()