import unittest
from processor import Processor
from memory import Memory

class ProcessorInstructions(unittest.TestCase):

    def setUp(self):
        self.memorySize = 0x100
        pMem = Memory(self.memorySize)
        rwMem = Memory(self.memorySize)
        self.proc = Processor(pMem, rwMem)

    def clearMem(self):
        for addr in xrange(0, self.memorySize):
            self.proc.pMemory.write(addr, 0)
            self.proc.rwMemory.write(addr, 0)

    def rw_array_write(self, addr, *args):
            for offset, arg in enumerate(args):
                self.proc.rwMemory.write(offset+addr, arg)

    def p_array_write(self, addr, *args):
            for offset, arg in enumerate(args):
                self.proc.pMemory.write(offset+addr, arg)

    def test_and_00_false(self):
        self.clearMem()
        #bytecode for and [0][1]
        self.p_array_write(0, 0, 1)
        self.rw_array_write(0, 0, 1)
        self.proc.execute()
        self.assertEquals(self.proc.rwMemory.read(0), 0)

    def test_and_00_true(self):
        self.clearMem()
        #bytecode for and [0][1]
        self.p_array_write(0, 0, 1)
        self.rw_array_write(0, 1, 1)
        self.proc.execute()
        self.assertEquals(self.proc.rwMemory.read(0), 1)

    def test_and_01_false(self):
        self.clearMem()
        #bytecode for and [0]1
        self.p_array_write(1, 0, 1)
        self.rw_array_write(0, 0)
        self.proc.execute()
        self.assertEquals(self.proc.rwMemory.read(0), 0)

    def test_and_01_true(self):
        self.clearMem()
        #bytecode for and [0]1
        self.p_array_write(1, 0, 1)
        self.rw_array_write(0, 1)
        self.proc.execute()
        self.assertEquals(self.proc.rwMemory.read(0), 1)

    def test_or_02_false(self):
        self.clearMem()
        #bytecode for or [0][1]
        self.p_array_write(2, 0, 1)
        self.rw_array_write(0, 0, 0)
        self.proc.execute()
        self.assertEquals(self.proc.rwMemory.read(0), 0)

    def test_or_02_true(self):
        self.clearMem()
        #bytecode for and [0][1]
        self.p_array_write(2, 0, 1)
        self.rw_array_write(0, 1, 1)
        self.proc.execute()
        self.assertEquals(self.proc.rwMemory.read(0), 1)


    def test_or_03_false(self):
        self.clearMem()
        #bytecode for or [0] 0
        self.p_array_write(3, 0, 0)
        self.rw_array_write(0, 0, 0)
        self.proc.execute()
        self.assertEquals(self.proc.rwMemory.read(0), 0)


    def test_xor_04_true(self):
        self.clearMem()
        #bytecode for or [0] 0
        self.p_array_write(4, 0, 1)
        self.rw_array_write(0, 1, 0)
        self.proc.execute()
        self.assertEquals(self.proc.rwMemory.read(0), 1)

    def test_xor_04_false01(self):
        self.clearMem()
        #bytecode for or [0] 0
        self.p_array_write(4, 0, 1)
        self.rw_array_write(1, 1, 0)
        self.proc.execute()
        self.assertEquals(self.proc.rwMemory.read(0), 0)

    def test_xor_04_false02(self):
        self.clearMem()
        #bytecode for or [0] 0
        self.p_array_write(4, 0, 1)
        self.rw_array_write(0, 0, 0)
        self.proc.execute()
        self.assertEquals(self.proc.rwMemory.read(0), 0)

    def test_xor_05_true(self):
        self.clearMem()
        self.p_array_write(5, 0, 1)
        self.rw_array_write(0, 0, 0)
        self.proc.execute()
        self.assertEquals(self.proc.rwMemory.read(0), 1)

    def test_xor_05_false01(self):
        self.clearMem()
        self.p_array_write(5, 0, 1)
        self.rw_array_write(1, 0, 0)
        self.proc.execute()
        self.assertEquals(self.proc.rwMemory.read(0), 0)

    def test_xor_05_false02(self):
        self.clearMem()
        #bytecode for or [0] 0
        self.p_array_write(5, 0, 0)
        self.rw_array_write(0, 0, 0)
        self.proc.execute()
        self.assertEquals(self.proc.rwMemory.read(0), 0)


    if __name__ == "__main__":
        unittest.main()