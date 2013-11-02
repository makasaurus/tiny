from cheapALU import *
from random import *

class Processor:

    #NO HALT COUNT - FIGURE THIS OUT
    instructionCount = [3,3,
                        3,3,
                        3,3,
                        2,
                        3,3,
                        2,
                        3,3,
                        3,3,
                        2,2,
                        3,3,3,3,
                        4,4,4,4,
                        4,4,4,4,
                        4,4,4,4,
                        2,
                        2]

    # jump will set the pc to the specified line number. The line number must be
    # the line number specified in pMemory rather than rwMemory.
    def jump(self, line):
        target=0
        for x in range(0, line-1):
            target += self.instructionCount[self.pMemory.read(target)]

        self.pc = target - 1 #it will add 1 to pc at end of cycle, so we must offset
    
    def nextCycle(self):
        while not self.halt:
            self.execute()
            self.pc+=1

    def execute(self):
        instruction = self.pMemory.read(self.pc)

        #support just a few instructions for now...
        if instruction == 0x00:
            print "and [][]"
            self.pc+=1
            target = self.pMemory.read(self.pc)
            op1 = self.rwMemory.read(target)
            self.pc+=1
            op2 = self.rwMemory.read(self.pMemory.read(self.pc))
            result = self.alu._and(op1, op2)
            self.rwMemory.write(target, result)

        if instruction == 0x01:
            print "and []_"
            self.pc+=1
            target = self.pMemory.read(self.pc)
            op1 = self.rwMemory.read(target)
            self.pc+=1
            op2 = self.pMemory.read(self.pc)
            result = self.alu._and(op1, op2)
            self.rwMemory.write(target, result)

        if instruction == 0x02:
            print "or [][]"
            self.pc+=1
            target = self.pMemory.read(self.pc)
            op1 = self.rwMemory.read(target)
            self.pc+=1
            op2 = self.rwMemory.read(self.pMemory.read(self.pc))
            result = self.alu._or(op1, op2)
            self.rwMemory.write(target, result)

        if instruction == 0x03:
            print "or []_"
            self.pc+=1
            target = self.pMemory.read(self.pc)
            op1 = self.rwMemory.read(target)
            self.pc+=1
            op2 = self.pMemory.read(self.pc)
            result = self.alu._or(op1, op2)
            self.rwMemory.write(target, result)

        if instruction == 0x04:
            print "xor [][]"
            self.pc+=1
            target = self.pMemory.read(self.pc)
            op1 = self.rwMemory.read(target)
            self.pc+=1
            op2 = self.rwMemory.read(self.pMemory.read(self.pc))
            result = self.alu._xor(op1, op2)
            self.rwMemory.write(target, result)

        if instruction == 0x05:
            print "xor []_"
            self.pc+=1
            target = self.pMemory.read(self.pc)
            op1 = self.rwMemory.read(target)
            self.pc+=1
            op2 = self.pMemory.read(self.pc)
            result = self.alu._xor(op1, op2)
            self.rwMemory.write(target, result)

        if instruction == 0x06:
            print "not []"
            self.pc+=1
            address = self.pMemory.read(self.pc)
            target = self.rwMemory.read(address)
            result = self.alu._not(target)
            self.rwMemory.write(address, result)

        if instruction == 0x07:
            print "mov [][]"
            self.pc+=1
            target = self.pMemory.read(self.pc)
            self.pc+=1
            toMove = self.rwMemory.read(self.pMemory.read(self.pc))
            self.rwMemory.write(target, toMove)

        if instruction == 0x08:
            print "mov []_"
            self.pc+=1
            target = self.pMemory.read(self.pc)
            self.pc+=1
            toMove = self.pMemory.read(self.pc)
            self.rwMemory.write(target, toMove)

        if instruction == 0x09:
            print "random []"
            self.pc+=1
            address = self.pMemory.read(self.pc)
            self.rwMemory.write(address, (int)(random()*256))

        if instruction == 0x0a:
            print "add [][]"
            self.pc+=1
            address = self.pMemory.read(self.pc)
            target = self.rwMemory.read(address)
            self.pc+=1
            second = self.rwMemory.read(self.pMemory.read(self.pc))
            answer = self.alu.add(target, second)
            self.rwMemory.write(address, answer)

        if instruction == 0x0b:
            ##then add []_
            print "add []_"
            self.pc+=1
            address = self.pMemory.read(self.pc)
            target = self.rwMemory.read(address)
            self.pc+=1
            second = self.pMemory.read(self.pc)
            answer = self.alu.add(target, second)
            self.rwMemory.write(address, answer)

        if instruction == 0x0c:
            print "sub [][]"
            self.pc+=1
            address = self.pMemory.read(self.pc)
            target = self.rwMemory.read(address)
            self.pc+=1
            second = self.rwMemory.read(self.pMemory.read(self.pc))
            answer = self.alu.sub(target, second)
            self.rwMemory.write(address, answer)

        if instruction == 0x0d:
            print "sub []_"
            self.pc+=1
            address = self.pMemory.read(self.pc)
            target = self.rwMemory.read(address)
            self.pc+=1
            second = self.pMemory.read(self.pc)
            answer = self.alu.sub(target, second)
            self.rwMemory.write(address, answer)

        if instruction == 0x0e:
            print "jmp []"
            self.pc+=1
            address = self.pMemory.read(self.pc)
            line = self.rwMemory.read(address)
            self.jump(line)

        if instruction == 0x0f:
            print "jmp _"
            self.pc+=1
            line = self.pMemory.read(self.pc)
            self.jump(line)

        if instruction == 0x10:
            print "jz [][]"
            self.pc += 1
            address = self.pMemory.read(self.pc)

            self.pc += 1
            value = self.rwMemory.read(self.pMemory.read(self.pc))

            if self.alu.eq(value, 0):
                line = self.rwMemory.read(address)
                self.jump(line)

        if instruction == 0x11:
            print "jz []_"
            self.pc+=1
            address = self.pMemory.read(self.pc)

            value = self.pMemory.read(self.pc)
            if self.alu.eq(value,0):
                line = self.rwMemory.read(address)
                self.jump(line)

        if instruction == 0x12:
            print "jz _[]"
            self.pc+=1
            line = self.pMemory.read(self.pc)
            self.jump(line)

        if instruction == 0x13:
            print "jz __"
            self.pc+=1
            line = self.pMemory.read(self.pc)
            self.jump(line)


        if instruction == 0x20:
            print "aprint"
            self.pc+=1
            target=self.rwMemory.read(self.pMemory.read(self.pc))
            print "# %s"%str(unichr(target))

        if instruction == 0x21:
            # then dprint [
            print "dprint"
            self.pc+=1
            target=self.rwMemory.read(self.pMemory.read(self.pc))
            print "# %d"%target

        if instruction == 0xff:
            #halt
            print "halt"
            self.halt = True




    def __init__(self, pMemory, rwMemory):
        self.pMemory = pMemory
        self.rwMemory = rwMemory
        self.alu = CheapALU()
        self.pc=0
        self.halt = False
