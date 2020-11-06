from pwn import *
from pwnlib.util import misc
import tempfile
from time import sleep

def pwndbg(script=b"") :
        tmp = tempfile.NamedTemporaryFile(prefix = 'pwn', suffix = '.gdb',
                                                  delete = False)
        tmp.write(b"""
        set architecture mips
        set endian big
        target remote localhost:12345
        """ + script + b"\n")

        misc.run_in_new_terminal('gdb-multiarch -q  -x "%s"' % tmp.name)

context.log_level = 'debug'
p = process(["qemu-mips-static", "-g", "12345", "./bin"])
pwndbg(b"")

p.interactive()
