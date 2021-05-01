from g_mc import MemoryCell
from g_bo import BinaryObject
import copy
class PrimaryMemory:
    def __init__(self, length):
        self.__pm = [MemoryCell() for _i in range(length)]
    
    def write(self, addr, data: BinaryObject):
        if not self.__pm[addr].isProtected():
            self.__pm[addr].write(data)
        else:
            raise IsProtectedCellException('Memory cell is write-protected.')
    
    def read(self, addr):
        return self.__pm[addr].read()
    
    def protect(self, addr):
        self.__pm[addr].protect()
    
    def unprotect(self, addr):
        self.__pm[addr].unprotect()
    
    def erase(self, addr):
        self.__pm[addr].clear()

    def clear(self):
        self.__pm = [MemoryCell() for _i in range(length)]
    
    def logicNot(self, addr):
        #self.__cell.logicNot()
        self.__pm[addr].logicNot()

    def logicAnd(self, addr, argAddr):
        self.__pm[addr].logicAnd(self.__pm[argAddr])

    def logicOr(self, addr, argAddr):
        self.__pm[addr].logicOr(self.__pm[argAddr])

    
    def logicXor(self, addr, argAddr):
        self.__pm[addr].logicXor(self.__pm[argAddr])

    
    def logicEqv(self, addr, argAddr):
        self.__pm[addr].logicEqv(self.__pm[argAddr])

    
    def logicImp(self, addr, argAddr):
        self.__pm[addr].logicImp(self.__pm[argAddr])

    
    def logicNand(self, addr, argAddr):
        self.logicAnd(addr, argAddr)
        self.logicNot(addr)
    
    def logicNor(self, addr, argAddr):
        self.logicOr(addr, argAddr)
        self.logicNot(addr)

    def sub(self, addr, argAddr):
        self.__pm[addr].sub(self.__pm[argAddr])

    def add(self, addr, argAddr):
        self.__pm[addr].add(self.__pm[argAddr])
    
    def move(self, source, destination):
        self.__pm[destination] = copy.deepcopy(self.__pm[source])
        #dest = MemoryCell()
        #dest.write(self.__pm[source].read())
        #self.__pm[destination] = dest
        self.__pm[source].clear()
    
    def copy(self, source, destination):
        self.__pm[destination] = copy.deepcopy(self.__pm[source])
    
    def __len__(self):
        return len(self.__pm)