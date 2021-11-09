import string

# in GDB break at check address
# in GDB run source [this script]
# update addresses with actual values

alphabet = string.hexdigits + "}"
flag_length = 34
known = "ACI{"


while len(known) < flag_length:
	for letter in alphabet:
		guess = known + letter + ("_" * (flag_length - 1 - len(known)))
		gdb.execute("r < <(python -c \"print '" + guess + "'\")")
		# gdb.execute("r " + guess)
		enc_flag = str(gdb.parse_and_eval(hex(0x5555557576d0+len(known))).cast(gdb.lookup_type('char').pointer()).dereference())
		# enc_flag = str(gdb.parse_and_eval(hex(gdb.parse_and_eval('$rax').cast(self.long_int)+len(known))).cast(gdb.lookup_type('char').pointer()).dereference())
		data_str = str(gdb.parse_and_eval(hex(0x5555557577d0+len(known))).cast(gdb.lookup_type('char').pointer()).dereference())
		if enc_flag == data_str:
			known += letter
			print(known)
print("Flag: {}".format(known))

# can also make gdb the process
"""
from pwn import *
import sys
import string
	

program = sys.argv[1]


alphabet = string.hexdigits + "}"
known = "flag_{"

r = process("gdb")
while "}" not in known:
	r.sendlineafter("pwndbg> ", f"file {program}")
	r.sendlineafter("pwndbg> ", f"b *0x4009ed")
	found = False
	for guess in alphabet:
		r.sendlineafter("pwndbg> ", f"r {known}{guess}")
		
		r.sendlineafter("pwndbg> ", f"p $eax")
		eax = int(r.recvline().split()[-1].decode(), 10)
		r.sendlineafter("pwndbg> ", f"p $ecx")
		ecx = int(r.recvline().split()[-1].decode(), 10)
		
		r.sendlineafter("pwndbg> ", f"x/bx $rcx+{len(known)}")
		them = int(r.recvline().decode().split("0x")[-1].rstrip(), 16)
		r.sendlineafter("pwndbg> ", f"x/bx $rax+{len(known)}")
		me = int(r.recvline().decode().split("0x")[-1].rstrip(), 16)
		
		if them == me:
			known += guess
			print(known)
			found = True
			break
		
	if not found:
		r.interactive()
		exit()

r.interactive()
"""