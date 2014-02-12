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


    def instruction_debug(self, msg):
        if self.debugLevel != 0:
            print msg

    def nextCycle(self):
        while not self.halt:
            self.execute()
            self.pc+=1

    def massMemoryCall(self, *args):
        """
        Args for Memory call are set up as set of (callType, address)

        returns a tuple of memory call results

        Example: massMemoryCall('p','rw') could return (9,0)
        """

        contents = ()
        for memCall in args:
            self.pc += 1
            if memCall == 'p':
                value = self.pMemory.read(self.pc)
                if len(args) == 1:
                    return value
                contents += (value,)
            else:
                value = self.rwMemory.read(self.pMemory.read(self.pc))
                if len(args) == 1:
                    return value
                contents += (value,)

        return contents

    def massMemoryWrite(self, *args):
        """
        Takes in sets of tuples for *args as (memType, address, value)

        Example: massMemoryWrite(('rw', 5, 3),('p', 0, 0))
        """

        for memWrite in args:
            type, address, value = memWrite
            if type == 'p':
                self.pMemory.write(address, value)
            else:
                self.rwMemory.write(address, value)

    def execute(self):
        instruction = self.pMemory.read(self.pc)

        if instruction == 0x00:
            self.instruction_debug("and [][]")
            self.pc+=1
            target = self.pMemory.read(self.pc)
            op1 = self.rwMemory.read(target)
            self.pc+=1
            op2 = self.rwMemory.read(self.pMemory.read(self.pc))

            op1, op2 = self.massMemoryCall('rw','rw')
            result = self.alu._and(op1, op2)
            self.rwMemory.write(target, result)

        elif instruction == 0x01:
            self.instruction_debug("and []_")
            self.pc+=1
            target = self.pMemory.read(self.pc)
            op1 = self.rwMemory.read(target)
            self.pc+=1
            op2 = self.pMemory.read(self.pc)
            result = self.alu._and(op1, op2)
            self.rwMemory.write(target, result)

        elif instruction == 0x02:
            self.instruction_debug("or [][]")
            self.pc+=1
            target = self.pMemory.read(self.pc)
            op1 = self.rwMemory.read(target)
            self.pc+=1
            op2 = self.rwMemory.read(self.pMemory.read(self.pc))
            result = self.alu._or(op1, op2)
            self.rwMemory.write(target, result)

        elif instruction == 0x03:
            self.instruction_debug("or []_")
            self.pc+=1
            target = self.pMemory.read(self.pc)
            op1 = self.rwMemory.read(target)
            self.pc+=1
            op2 = self.pMemory.read(self.pc)
            result = self.alu._or(op1, op2)
            self.rwMemory.write(target, result)

        elif instruction == 0x04:
            self.instruction_debug("xor [][]")
            self.pc+=1
            target = self.pMemory.read(self.pc)
            op1 = self.rwMemory.read(target)
            self.pc+=1
            op2 = self.rwMemory.read(self.pMemory.read(self.pc))
            result = self.alu._xor(op1, op2)
            self.rwMemory.write(target, result)

        elif instruction == 0x05:
            self.instruction_debug("xor []_")
            self.pc+=1
            target = self.pMemory.read(self.pc)
            op1 = self.rwMemory.read(target)
            self.pc+=1
            op2 = self.pMemory.read(self.pc)
            result = self.alu._xor(op1, op2)
            self.rwMemory.write(target, result)

        elif instruction == 0x06:
            self.instruction_debug("not []")
            self.pc+=1
            address = self.pMemory.read(self.pc)
            target = self.rwMemory.read(address)
            result = self.alu._not(target)
            self.rwMemory.write(address, result)

        elif instruction == 0x07:
            self.instruction_debug("mov [][]")
            self.pc+=1
            target = self.pMemory.read(self.pc)
            self.pc+=1
            toMove = self.rwMemory.read(self.pMemory.read(self.pc))
            self.rwMemory.write(target, toMove)

        elif instruction == 0x08:
            self.instruction_debug("mov []_")

            target, toMove = self.massMemoryCall("p", "p")
            self.massMemoryWrite(('rw', target, toMove))

        elif instruction == 0x09:
            self.instruction_debug("random []")
            self.pc+=1
            address = self.pMemory.read(self.pc)
            self.rwMemory.write(address, (int)(random()*256))

        elif instruction == 0x0a:
            self.instruction_debug("add [][]")
            self.pc+=1
            address = self.pMemory.read(self.pc)
            target = self.rwMemory.read(address)
            self.pc+=1
            second = self.rwMemory.read(self.pMemory.read(self.pc))
            answer = self.alu.add(target, second)
            self.rwMemory.write(address, answer)

        elif instruction == 0x0b:
            ##then add []_
            self.instruction_debug("add []_")
            self.pc+=1
            address = self.pMemory.read(self.pc)
            target = self.rwMemory.read(address)
            self.pc+=1
            second = self.pMemory.read(self.pc)
            answer = self.alu.add(target, second)
            self.rwMemory.write(address, answer)

        elif instruction == 0x0c:
            self.instruction_debug("sub [][]")
            self.pc+=1
            address = self.pMemory.read(self.pc)
            target = self.rwMemory.read(address)
            self.pc+=1
            second = self.rwMemory.read(self.pMemory.read(self.pc))
            answer = self.alu.sub(target, second)
            self.rwMemory.write(address, answer)

        elif instruction == 0x0d:
            self.instruction_debug("sub []_")
            self.pc+=1
            address = self.pMemory.read(self.pc)
            target = self.rwMemory.read(address)
            self.pc+=1
            second = self.pMemory.read(self.pc)
            answer = self.alu.sub(target, second)
            self.rwMemory.write(address, answer)

        elif instruction == 0x0e:
            self.instruction_debug("jmp []")
            self.pc+=1
            address = self.pMemory.read(self.pc)
            line = self.rwMemory.read(address)
            self.jump(line)

        elif instruction == 0x0f:
            self.instruction_debug("jmp _")
            self.pc+=1
            line = self.pMemory.read(self.pc)
            self.jump(line)

        elif instruction == 0x10:
            self.instruction_debug("jz [][]")
            self.pc+=1
            address = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc+=1
            value = self.rwMemory.read(self.pMemory.read(self.pc))
            print "value: %d address: %d"%(value, address)
            if self.alu.eq(value,0):
                line = address
                self.jump(line)

        elif instruction == 0x11:
            self.instruction_debug("jz []_")
            self.pc+=1
            address = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc+=1
            value = self.pMemory.read(self.pc)
            print "value: %d address: %d"%(value, address)
            if self.alu.eq(value,0):
                line = address
                self.jump(line)

        elif instruction == 0x12:
            self.instruction_debug("jz _[]")
            self.pc+=1
            address = self.pMemory.read(self.pc)
            self.pc+=1
            value = self.rwMemory.read(self.pMemory.read(self.pc))
            print "value: %d address: %d"%(value, address)
            if self.alu.eq(value,0):
                line = address
                self.jump(line)

        elif instruction == 0x13:
            self.instruction_debug("jz __")
            self.pc+=1
            address = self.pMemory.read(self.pc)
            self.pc+=1
            value = self.pMemory.read(self.pc)
            print "value: %d address: %d"%(value, address)
            if self.alu.eq(value,0):
                line = address
                self.jump(line)

        elif instruction == 0x14:
            self.instruction_debug("jeq [][][]")
            self.pc+=1
            address = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc+=1
            value1 = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc += 1
            value2 = self.rwMemory.read(self.pMemory.read(self.pc))
            if self.alu.eq(value1, value2):
                line = address
                self.jump(line)

        elif instruction == 0x15:
            self.instruction_debug("jeq _[][]")
            self.pc+=1
            address = self.pMemory.read(self.pc)
            self.pc+=1
            value1 = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc += 1
            value2 = self.rwMemory.read(self.pMemory.read(self.pc))
            if self.alu.eq(value1, value2):
                line = address
                self.jump(line)

        elif instruction == 0x16:
            self.instruction_debug("jeq [][]_")
            self.pc+=1
            address = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc+=1
            value1 = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc += 1
            value2 = self.pMemory.read(self.pc)
            if self.alu.eq(value1, value2):
                line = address
                self.jump(line)

        elif instruction == 0x17:
            self.instruction_debug("jeq []_[]")
            self.pc+=1
            address = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc+=1
            value1 = self.pMemory.read(self.pc)
            self.pc += 1
            value2 = self.rwMemory.read(self.pMemory.read(self.pc))
            if self.alu.eq(value1, value2):
                line = address
                self.jump(line)

        elif instruction == 0x18:
            self.instruction_debug("jls [][][]")
            self.pc+=1
            address = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc+=1
            value1 = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc += 1
            value2 = self.rwMemory.read(self.pMemory.read(self.pc))
            if self.alu.lt(value1, value2):
                line = address
                self.jump(line)

        elif instruction == 0x19:
            self.instruction_debug("jls _[][]")
            self.pc+=1
            address = self.pMemory.read(self.pc)
            self.pc+=1
            value1 = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc += 1
            value2 = self.rwMemory.read(self.pMemory.read(self.pc))
            if self.alu.lt(value1, value2):
                line = address
                self.jump(line)

        elif instruction == 0x1a:
            self.instruction_debug("jls [][]_")
            self.pc+=1
            address = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc+=1
            value1 = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc += 1
            value2 = self.pMemory.read(self.pc)
            if self.alu.lt(value1, value2):
                line = address
                self.jump(line)

        elif instruction == 0x1b:
            self.instruction_debug("jls []_[]")
            self.pc+=1
            address = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc+=1
            value1 = self.pMemory.read(self.pc)
            self.pc += 1
            value2 = self.rwMemory.read(self.pMemory.read(self.pc))
            if self.alu.lt(value1, value2):
                line = address
                self.jump(line)

        elif instruction == 0x1c:
            self.instruction_debug("jgt [][][]")
            self.pc+=1
            address = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc+=1
            value1 = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc += 1
            value2 = self.rwMemory.read(self.pMemory.read(self.pc))
            if self.alu.gt(value1, value2):
                line = address
                self.jump(line)

        elif instruction == 0x1d:
            self.instruction_debug("jgt _[][]")
            self.pc+=1
            address = self.pMemory.read(self.pc)
            self.pc+=1
            value1 = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc += 1
            value2 = self.rwMemory.read(self.pMemory.read(self.pc))
            if self.alu.gt(value1, value2):
                line = address
                self.jump(line)

        elif instruction == 0x1e:
            self.instruction_debug("jgt [][]_")
            self.pc+=1
            address = self.rwMemory(self.pMemory.read(self.pc))
            self.pc+=1
            value1 = self.rwMemory.read(self.pMemory.read(self.pc))
            self.pc += 1
            value2 = self.pMemory.read(self.pc)
            if self.alu.gt(value1, value2):
                line = address
                self.jump(line)

        elif instruction == 0x1f:
            self.instruction_debug("jgt []_[]")
            self.pc+=1
            address = self.rwMemory(self.pMemory.read(self.pc))
            self.pc+=1
            value1 = self.pMemory.read(self.pc)
            self.pc += 1
            value2 = self.rwMemory.read(self.pMemory.read(self.pc))
            if self.alu.gt(value1, value2):
                line = address
                self.jump(line)

        elif instruction == 0x20:
            self.instruction_debug("aprint")
            self.pc+=1
            target=self.rwMemory.read(self.pMemory.read(self.pc))
            print "%s"%str(unichr(target))

        elif instruction == 0x21:
            # then dprint [
            self.instruction_debug("dprint")
            self.pc+=1
            target=self.rwMemory.read(self.pMemory.read(self.pc))
            print "%s"%(target)

        elif instruction == 0xff:
            #halt
            self.instruction_debug("halt")
            self.halt = True

    def __init__(self, pMemory, rwMemory):
        self.pMemory = pMemory
        self.rwMemory = rwMemory
        self.alu = CheapALU()
        self.pc=0
        self.halt = False
        self.debugLevel = 0