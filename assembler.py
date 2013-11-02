translation = {
    'and':
        {'[[': 0x00, '[ ': 0x01},
    'or':
        {'[[': 0x02, '[ ': 0x03},
    'xor':
        {'[[': 0x04, '[ ': 0x05},
    'not':
        {'[': 0x06},
    'mov':
        {'[[': 0x07, '[ ': 0x08},
    'random':
        {'[': 0x09},
    'add':
        {'[[': 0x0a, '[ ': 0x0b},
    'sub':
        {'[[': 0x0c, '[ ': 0x0d},
    'jmp':
        {'[': 0x0e, ' ': 0x0f},
    'jz':
        {'[[': 0x10, '[ ': 0x11, ' [': 0x12, '  ': 0x13},
    'jeq':
        {'[[[': 0x14, ' [[': 0x15, '[[ ': 0x16, ' [ ': 0x17},
    'jls':
        {'[[[': 0x18, ' [[': 0x19, '[[ ': 0x1a, ' [ ': 0x1b},
    'jgt':
        {'[[[': 0x1c, ' [[': 0x1d, '[[ ': 0x1e, ' [ ': 0x1f},
    'halt':
        {'': 0xff},
    'aprint':
        {'[': 0x20},
    'dprint':
        {'[': 0x21}
}


class Assembler:
    def assemble(self, code):
        machineCode = []

        lines = code.split('\n')
        for line in lines:
            ops = line.split(' ')

            instruction = ops[0]
            literalMatching = ''
            for op in ops[1:]:
                ## TODO deal with brackets
                if op[0] == '[':
                    literalMatching += '['
                else:
                    literalMatching += ' '

            #TODO add try/catch for KeyError for instruction not found
            opCode = translation[instruction][literalMatching]

            machineCode += [opCode]

            for op in ops[1:]:
                op = (int)(op.replace('[', '').replace(']', ''))
                machineCode += [op]

        return machineCode