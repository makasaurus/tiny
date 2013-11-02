class Memory:

    #TODO eventually have memory use embedded system to read/write
    
    memory = []

    def write(self, address, byte):
        self.memory[address] = byte

    def read(self, address):
        return self.memory[address]

    def __init__(self, size):
        self.memory=[0x0]*size
        
