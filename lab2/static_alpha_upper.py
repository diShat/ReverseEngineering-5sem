from sys import byteorder
from pwn import *

context.arch = 'i386'

for file in sys.argv[1:]:
	print("Analysing", file)
	filedata = bytearray(read(file))
	result = filedata
	# print(filedata)
	# print(hexdump(result))

	for i in range(0x0, len(filedata), 0x1):
		try: 
			result[0x41+i] = result[0x42+2*i]^(result[0x41+2*i]*0x10)%0x100
		except: 
			print('Yay =^.^=')
			break
		# print(hexdump(result))

end = result.find(b'\n')
print(result[0x42:end].decode())