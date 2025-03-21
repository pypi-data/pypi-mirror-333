# riscvlib  
  
Resources for working with RiscV assembly in Python.   
  
# Installation  
The package can be installed using pip:  
  
	 $ pip install riscvlib  
 
# Examples  
  
## Instruction, Static creation from a string
``` python
>> from riscvlib.instruction import Instruction  

>> i = Instruction.from_line("add x1, x2, x3")  
>> print(i) 
add x1, x2, x3  
>> i.to_bytes() 
b'\xb3\x001\x00'  
>> i  
<riscvlib.instruction.RInstruction object at 0x....>
```

## Specific Instruction Type
``` python
>> from riscvlib.instruction import RInstruction, IInstruction

>> r_instr = RInstruction("add", "x1", "x2", "a2")
>> print(r_instr)
add x1, x2, a2

>> i_instr = IInstruction("andi", "a0", "a1", -13)
>> print(i_instr)
andi a0, a1, -13
>> i_instr.to_bytes()  # note: bytes are 'little endian' ordered
b'\x13\xf55\xff'
```

## Pseudo Instruction Translation
``` python
>> from riscvlib.instruction import translate_pseudo_instruction

>> out_list = translate_pseudo_instruction("mv", "a0", "x30")
>> print(out_list)
['add a0, x30, x0']

>> out_list = translate_pseudo_instruction("la", "a0", "400")
>> print(out_list)
['lui a0, %hi(400)', 'addi a0, a0, %lo(400)']
```

## Instruction Data
``` python
>> from riscvlib.risvdata import INSTRUCTION_MAP

>> INSTRUCTION_MAP['mul']
('MUL', '0110011', '000', '0000001', 'R', 'm')
# (name, opcode, func3, func7, itype, extension)
```

# Limitations
 - Currently only supports 32bit instructions 
 - I and M extensions supported  (will add F in the future)



