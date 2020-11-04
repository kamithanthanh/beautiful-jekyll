from pwn import * 
from pwnlib.util import misc
import tempfile
from time import sleep 

def pwndbg(script=b"") : 
	tmp = tempfile.NamedTemporaryFile(prefix = 'pwn', suffix = '.gdb',
		                                  delete = False)
	tmp.write(b"""
	set architecture arm
	target remote localhost:1234
	""" + script + b"\n")

	misc.run_in_new_terminal('gdb-multiarch -q -x "%s"' % tmp.name)

p = process(['qemu-arm-static', '-g', '1234', './bin'])
pwndbg(b'')
p.interactive()
