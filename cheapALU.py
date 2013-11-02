class CheapALU():

    #ALU is 'cheap' because it is not bitwise. we need bitwise. this is just an object placeholder

    def _and(self, x,y):
        return 1 if x and y else 0

    def _or(self, x,y):
        return 1 if x or y else 0

    def _xor(self, x,y):
        return 1 if (x and not y) or (not x and y) else 0

    def _not(self, x):
        return not x

    def add(self, x,y):
        return x+y

    def sub(self, x,y):
        return x-y

    def eq(self, x, y):
        return x == y

    def __init__(self):
        return None
