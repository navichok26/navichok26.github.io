#!/usr/bin/env python3
import sys
from enum import Enum

class COMMAND(Enum):
	INPUT = 0x81
	OUTPUT = 0x80
	NOP = 0x90
	MOV = 0x30
	NOTAND = 0x31
	CMP = 0x32
	LSHIFT = 0x40
	RSHIFT = 0x41
	JNE = 0x50


if __name__ == '__main__':
	filename = sys.argv[1]
	file = open(filename, 'rb')
	code = file.read()
	file.close()

	FLAG = 0

	f = open(f"{filename}.dis", 'w')

	pc = 0
	count = 0
	while (pc < len(code)):
		print(pc, "/", len(code))
		print(hex(code[pc]))
		if (code[pc] == COMMAND.INPUT.value):
			print("INPUT")
			count += 1
			pc += 3
			f.write(f"input {hex(code[pc+1])}{hex(code[pc+2])[2:]}\n")
		elif (code[pc] == COMMAND.OUTPUT.value):
			print("OUTPUT")
			count += 1
			pc += 3
			f.write(f"output {hex(code[pc+1])}{hex(code[pc+2])[2:]}\n")
		elif (code[pc] == COMMAND.NOP.value):
			print("NOP")
			count += 1
			pc += 1
			f.write(f"nop\n")
		elif (code[pc] == COMMAND.MOV.value):
			print("MOV")
			count += 1
			pc += 2
			f.write(f"mov [r]{hex(code[pc+1] >> 4)}, [r]{hex(code[pc+1] & 0xf)}\n")
		elif (code[pc] == COMMAND.NOTAND.value):
			print("NOTAND")
			count += 1
			pc += 2
			f.write(f"notand [r]{hex(code[pc+1] >> 4)}, [r]{hex(code[pc+1] & 0xf)}\n")
		elif (code[pc] == COMMAND.CMP.value):
			print("CMP")
			count += 1
			pc += 2
			f.write(f"cmp [r]{hex(code[pc+1] >> 4)}, [r]{hex(code[pc+1] & 0xf)}\n")
		elif (code[pc] == COMMAND.LSHIFT.value):
			print("LSHIFT")
			count += 1
			pc += 2
			f.write(f"lsh [r]{hex(code[pc+1] >> 4)}, [r]{hex(code[pc+1] & 0xf)}\n")
		elif (code[pc] == COMMAND.RSHIFT.value):
			print("RSHIFT")
			count += 1
			pc += 2
			f.write(f"rsh [r]{hex(code[pc+1] >> 4)}, [r]{hex(code[pc+1] & 0xf)}\n")
		elif (code[pc] == COMMAND.JNE.value):
			print("JNE")
			count += 1
			pc += 3
			f.write(f"jne {hex(code[pc+1])}{hex(code[pc+2])[2:]}\n")
			# if (FLAG == 1) {
			# 	FLAG = 0
			# 	pc += 3
			# } else {
			# 	pc = ((code[pc+1]<<8) + code[pc+2])
			# }
		elif (code[pc] in range(0x18, 0x1f+1)):
			print("MOVRMEM2") # ops: command(first 8 bit), 2 byte
			count += 1
			pc += 3
			f.write(f"mov [r]{hex(code[pc+1])}, [m]{hex(code[pc+2])}\n")
		elif (code[pc] in range(0x10, 0x17+1)):
			print("MOVRMEM1") # ops: command(first 8 bit), 1 byte
			count += 1
			pc += 2
			f.write(f"mov [r]{hex(code[pc] & 0xf)}, [m]{hex(code[pc+1])}\n")
		elif (code[pc] in range(0x20, 0x27+1)):
			print("MOVMEMR2") # ops: 2 byte, command(first 8 bit)
			count += 1
			pc += 3
			f.write(f"mov [m]{hex(code[pc+1])}{hex(code[pc+2])[2:]}, [r]{hex(code[pc] & 0xf)}\n")
		elif (code[pc] == 0xc0):
			pc += 2
			f.write("db 0xc0 0x00\n")
			#import IPython; IPython.embed()
			continue
		else:
			print(count)
			print("[Error] invalid opcode:", hex(code[pc]))
			exit(0)