from g_bo import BinaryObject

class InvalidWriteDataException(BaseException): ...

class IsProtectedCellException(BaseException): ...

class MemoryCell:
    def __init__(self):
        self.__cell = BinaryObject(8)
        self.__isProtected = False
    
    def write(self, data: BinaryObject):
        if not self.__isProtected:
            self.__cell = data
        else:
            raise IsProtectedCellException('Memory cell is write-protected.')
    
    def read(self):
        return self.__cell.readNative()
    
    def readAsBinaryObject(self):
        return self.__cell
    
    def protect(self):
        self.__isProtected = True
    
    def unprotect(self):
        self.__isProtected = False
    
    def isProtected(self):
        return self.__isProtected
    
    def clear(self):
        self.__cell.write([0,0,0,0,0,0,0,0])
        
    def logicNot(self):
        self.__cell.logicNot()

    def logicAnd(self, arg):
        self.__cell.logicAnd(arg.readAsBinaryObject())


    def logicOr(self, arg):
        self.__cell.logicOr(arg.readAsBinaryObject())

    
    def logicXor(self, arg):
        self.__cell.logicXor(arg.readAsBinaryObject())

    
    def logicEqv(self, arg):
        self.__cell.logicEqv(arg.readAsBinaryObject())

    
    def logicImp(self, arg):
        self.__cell.logicImp(arg.readAsBinaryObject())

    
    def logicNand(self, arg):
        self.logicAnd(arg)
        self.logicNot()
    
    def logicNor(self, arg):
        self.logicOr(arg)
        self.logicNot()



