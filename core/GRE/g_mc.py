from g_bo import BinaryObject

class InvalidWriteDataException(BaseException): ...

class IsProtectedCellException(BaseException): ...

class MemoryCell:
    '''Memory cell class. Represents a shell for BinaryObject with size 8.
    Can be protected from rewriting. 
    '''
    def __init__(self):
        self.__cell = BinaryObject(8)
        self.__isProtected = False
    
    def write(self, data: BinaryObject):
        '''In: other BinaryObject
        Out: void
        Desc: writes BinaryObject to the internal MemoryCell data if it isn't protected, else raises IsProtectedCellException
        '''
        if not self.__isProtected:
            self.__cell = data
        else:
            raise IsProtectedCellException('Memory cell is write-protected.')
    
    def read(self):
        '''In: void
        Out: list
        Desc: Returns internal object data as list
        '''
        return self.__cell.readNative()
    
    def readAsBinaryObject(self):
        '''In: void
        Out: BinaryObject
        Desc: Returns internal object data as BinaryObject
        '''
        return self.__cell
    
    def protect(self):
        '''In: void
        Out: void
        Desc: Protects MemomryCell from rewriting
        '''
        self.__isProtected = True
    
    def unprotect(self):
        '''In: void
        Out: void
        Desc: Unprotects MemoryCell from rewriting
        '''
        self.__isProtected = False
    
    def isProtected(self):
        '''In: void
        Out: bool
        Desc: Returns current state of the rewriting protection of MemoryCell
        '''
        return self.__isProtected
    
    def clear(self):
        '''In: void
        Out: void
        Desc: Writes to the internal cell data zero (0000000)
        '''
        self.__cell.write([0,0,0,0,0,0,0,0])
        
    def logicNot(self):
        '''In: void
        Out: void
        Desc: Releases NOT for itself
        '''
        self.__cell.logicNot()

    def logicAnd(self, arg):
        '''In: MemoryCell
        Out: void
        Desc: Releases AND for current MemoryCell and the other
        '''
        self.__cell.logicAnd(arg.readAsBinaryObject())


    def logicOr(self, arg):
        '''In: MemoryCell
        Out: void
        Desc: Releases OR for current MemoryCell and the other
        '''
        self.__cell.logicOr(arg.readAsBinaryObject())

    
    def logicXor(self, arg):
        '''In: MemoryCell
        Out: void
        Desc: Releases XOR for current MemoryCell and the other
        '''
        self.__cell.logicXor(arg.readAsBinaryObject())

    
    def logicEqv(self, arg):
        '''In: MemoryCell
        Out: void
        Desc: Releases EQV (equivalence) for current MemoryCell and the other
        '''
        self.__cell.logicEqv(arg.readAsBinaryObject())

    
    def logicImp(self, arg):
        '''In: MemoryCell
        Out: void
        Desc: Releases IMP (implication) for current MemoryCell and the other
        '''
        self.__cell.logicImp(arg.readAsBinaryObject())

    
    def logicNand(self, arg):
        '''In: MemoryCell
        Out: void
        Desc: Releases NAND (AND + NOT) for current MemoryCell and the other
        '''
        #self.logicAnd(arg)
        #self.logicNot()
        self.__cell.logicNand(arg.readAsBinaryObject())
    
    def logicNor(self, arg):
        '''In: MemoryCell
        Out: void
        Desc: Releases NOR (OR + NOT) for current MemoryCell and the other
        '''
        #self.logicOr(arg)
        #self.logicNot()
        self.__cell.logicNor(arg.readAsBinaryObject())
    

    def logicShiftLeft(self, pos):
        self.__cell.logicShiftLeft(pos)

    def logicShiftRight(self, pos):
        self.__cell.logicShiftRight(pos)

    def ariphmeticShiftLeft(self, pos):
        self.__cell.ariphmeticShiftLeft(pos)

    def ariphmeticShiftRight(self, pos):
        self.__cell.ariphmeticShiftRight(pos)

    def cyclicShiftLeft(self, pos):
        self.__cell.cyclicShiftLeft(pos)

    def cyclicShiftRight(self, pos):
        self.__cell.cyclicShiftRight(pos)

    def add(self, arg):
        '''In: MemoryCell
        Out: void
        Desc: adds value of the argument to the internal data
        '''
        self.__cell.add(arg.readAsBinaryObject())
    
    def sub(self, arg):
        '''In: MemoryCell
        Out: void
        Desc: substacts value of the argument from the internal data
        '''
        self.__cell.sub(arg.readAsBinaryObject())



