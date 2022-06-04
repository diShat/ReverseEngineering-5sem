#!/ usr / bin / env python3
from unicorn import *
from unicorn . x86_const import *
from capstone import *
from pwn import *
import sys

cs = Cs(CS_ARCH_X86, CS_MODE_32)
code = open(sys.argv[1], "rb").read()
address = 0

def hook_code(uc, address, size, user_data):
	global cs
	ins = uc.mem_read(address, size)
	print(" hook called at 0x{:x}, instruction {}".format(address, ins.hex()))

	for i in cs.disasm(ins, 0):
		print(" hook 0x{:03x} size {:2d}: {:03x}: {:20s} {} {}".format(address
			,size ,address + i.address , i.bytes.hex() , i.mnemonic , i.op_str))
	print(hexdump(uc.mem_read(0, len(code))))

def hook_syscall(mu, user_data):
	rax = mu.reg_read(UC_X86_REG_RAX)
	rdi = mu.reg_read(UC_X86_REG_RDI)
	if rax == 59:
		fn = mu.mem_read(rdi, 0x1000)
		fn = fn.split(b"\0")[0]
		fn = bytes(fn)
		print(" SYS_execve {}".format(fn))
	else:
		print(" syscall rax=0x{:x}, rdi=0x{:x}".format(rax, rdi))

mu = Uc(UC_ARCH_X86, UC_MODE_32)
mu.mem_map(address, address + 0x2000)
mu.mem_write(address, code)
mu.reg_write(UC_X86_REG_ESP, address + 0x1000)
mu.hook_add(UC_HOOK_CODE, hook_code)
mu.hook_add(UC_HOOK_INSN, hook_syscall, None, 1, 0, UC_X86_INS_SYSCALL)


try:
	mu.emu_start(address, address + len(code))
except Exception:
	print("done.")
else:
	print("done.")
