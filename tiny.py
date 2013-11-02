from memory import *
from processor import *
from assembler import *

pMem = Memory(0x100)
rwMem = Memory(0x100)


def hexPrint(memory):
    for item in memory:
        print hex(item),
    print

source = open("test.tiny","r")
sourceCode = source.read()
source.close()

assem = Assembler()
code = assem.assemble(sourceCode)

hexPrint(code)

for address, instruction in enumerate(code):
    pMem.write(address, instruction)

proc = Processor(pMem, rwMem)
proc.nextCycle()