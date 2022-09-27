#from g_mc import MemoryCell
from audioop import add
from g_bo_deprecated import BinaryObject
import copy

class IsProtectedCellException(BaseException): ...

class PrimaryMemory:
    def __init__(self, size):
        self.__mem = [0 for _ in range(size)]
        self.__size = size
        self.__protected = set()
    
    def write(self, addr, data):
        if not (addr in self.__protected):
            self.__mem[addr] = data
        else:
            raise IsProtectedCellException('Memory cell is write-protected.')
    
    def read(self, addr):
        binVal = bin(self.__mem[addr])[2:]
        return '0' * (8 - len(binVal)) + binVal
    #def read(self, addr):
    #    return self.__mem[addr].read()
    
    def protect(self, addr):
        self.__protected.add(addr)
    
    def unprotect(self, addr):
        if addr in self.__protected:
            self.__protected.pop(addr)
    
    def erase(self, addr):
        self.__mem[addr] = 0

    def clear(self):
        self.__mem = [0 for _ in range(self.__size)]
    
    '''def getLastNonEmptyCellIndex(self):
        for i in range(len(self.__mem)-1, -1, -1):
            if self.__mem[i] != MemoryCell:
                return i
        return 0'''

    def logicNot(self, addr):
        #self.__cell.logicNot()
        self.__mem[addr] = 255 - self.__mem[addr]

    def logicAnd(self, addr, argAddr):
        self.__mem[addr] = self.__mem[addr] & self.__mem[argAddr]

    def logicOr(self, addr, argAddr):
        self.__mem[addr] = self.__mem[addr] | self.__mem[argAddr]

    
    def logicXor(self, addr, argAddr):
        self.__mem[addr] = self.__mem[addr] ^ self.__mem[argAddr]

    
    def logicEqv(self, addr, argAddr):
        self.logicXor(addr, argAddr)
        self.logicNot(addr)

    
    def logicImp(self, addr, argAddr):
        self.logicNot(addr)
        self.logicOr(addr, argAddr)

    
    def logicNand(self, addr, argAddr):
        #self.logicAnd(addr, argAddr)
        #self.logicNot(addr)
        self.logicAnd(addr, argAddr)
        self.logicNot(addr)
    
    def logicNor(self, addr, argAddr):
        #self.logicOr(addr, argAddr)
        #self.logicNot(addr)
        self.logicOr(addr, argAddr)
        self.logicNot(addr)

    def logicShiftLeft(self, addr, pos):
        self.__mem[addr]= (self.__mem[addr] << pos) % 256

    def logicShiftRight(self, addr, pos):
        self.__mem[addr]= (self.__mem[addr] >> pos) % 256


    def __asr_1(self, addr):
        if self.__mem[addr] % 2 != 0:
            self.__mem[addr] -= 1
        self.__mem[addr] = self.__mem[addr] // 2 + 128 if self.__mem[addr] > 127 else 0

    def __csl_1(self, addr):
        if self.__mem[addr] > 127:
            self.logicShiftLeft(addr, 1)
            self.__mem[addr] += 1
        else:
            self.logicShiftLeft(addr, 1)

    def __csr_1(self, addr):
        if self.__mem[addr] % 2 != 0:
            self.logicShiftRight(addr, 1)
            self.__mem[addr] += 128
        else:
            self.logicShiftRight(addr, 1)

    def ariphmeticShiftLeft(self, addr, pos):
        self.logicShiftLeft(addr, pos)

    def ariphmeticShiftRight(self, addr, pos):
        for i in range(pos):
            self.__asr_1(addr)

    def cyclicShiftLeft(self, addr, pos):
        for i in range(pos):
            self.__csl_1(addr)

    def cyclicShiftRight(self, addr, pos):
        for i in range(pos):
            self.__csr_1(addr)

    def add(self, addr, argAddr):
        self.__mem[addr] = (self.__mem[addr] + self.__mem[argAddr]) % 256

    def sub(self, addr, argAddr):
        self.__mem[addr] = (self.__mem[addr] - self.__mem[argAddr]) % 256

    
    
    def copy(self, source, destination):
        self.__mem[destination] = self.__mem[source]
    
    def move(self, source, destination):
        self.copy(source, destination)
        #self.__mem[destination] = copy.deepcopy(self.__mem[source])
        #dest = MemoryCell()
        #dest.write(self.__mem[source].read())
        #self.__mem[destination] = dest
        self.__mem[source].clear()

    def __len__(self):
        return self.__size