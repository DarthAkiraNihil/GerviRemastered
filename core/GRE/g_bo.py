class InvalidWriteDataException(BaseException): ...

class NotEqualArgumentsLengthException(BaseException): ...

class BinaryObject:
    """BinaryObject constructor
    In: size (int)
    Out: BinaryObject
    Desc: Creates a binary object with fixed <size>


    """
    def __init__(self, size):
        self.__size = size
        self.__obj = [0 for _i in range(size)]

    
    def write(self, data):
        """In: data (list), it should contains only 0-1 values and equals to the <size>
        Out: void
        Desc: Writes <data> to the BinaryObjects
        """
        if data.count(0) + data.count(1) != len(data) or len(data) != self.__size:
            raise InvalidWriteDataException(f'Write data contains non-0-1 values or length of it not equal with object size({self.__size})')
        else:
            self.__obj = data
    
    def readNative(self):
        """In: void
        Out: list
        Desc: Returns internal BinaryObject data
        """
        return self.__obj
    
    def readString(self):
        """In: void
        Out: string
        Desc: Returns internal BinaryObject data as string


        """
        return ''.join(map(str, self.__obj))
    
    def getSize(self):
        """In: void
        Out: int
        Desc: Returns BinaryObject internal data size


        """
        return self.__size

    def __checkLength(self, arg):
        if self.__size != arg.getSize():
            raise NotEqualArgumentsLengthException('write some info later') #TODO exception message
    
    def logicNot(self):
        """In: void
        Out: void
        Desc: Applies logical NOT operation to the internal object data


        """
        for i in range(len(self.__obj)):
            self.__obj[i] = 0 if self.__obj[i] == 1 else 1
       
    def logicAnd(self, arg):
        """In: other BinaryObject
        Out: void
        Desc: Applies logical AND operation to the internal object data and other's object data and writes the result to itself

        :param arg: 

        """
        argObj = arg.readNative()
        self.__checkLength(arg)
        for i in range(len(self.__obj)):
            self.__obj[i] = 1 if self.__obj[i] == argObj[i] == 1 else 0
    
    def logicOr(self, arg):
        """In: other BinaryObject
        Out: void
        Desc: Applies logical OR operation to the internal object data and other's object data and writes the result to itself

        :param arg: 

        """
        argObj = arg.readNative()
        self.__checkLength(arg)
        for i in range(len(self.__obj)):
            self.__obj[i] = 0 if self.__obj[i] == argObj[i] == 0 else 1
    
    def logicXor(self, arg):
        """In: other BinaryObject
        Out: void
        Desc: Applies logical XOR operation to the internal object data and other's object data and writes the result to itself

        :param arg: 

        """
        argObj = arg.readNative()
        self.__checkLength(arg)
        for i in range(len(self.__obj)):
            self.__obj[i] = 1 if self.__obj[i] != argObj[i] else 0
    
    def logicEqv(self, arg):
        """In: other BinaryObject
        Out: void
        Desc: Applies logical EQV (equivalence) operation to the internal object data and other's object data and writes the result to itself

        :param arg: 

        """
        argObj = arg.readNative()
        self.__checkLength(arg)
        for i in range(len(self.__obj)):
            self.__obj[i] = 1 if self.__obj[i] == argObj[i] else 0

    def logicImp(self, arg):
        """In: other BinaryObject
        Out: void
        Desc: Applies logical IMP (implication) operation to the internal object data and other's object data and writes the result to itself

        :param arg: 

        """
        argObj = arg.readNative()
        self.__checkLength(arg)
        for i in range(len(self.__obj)):
            self.__obj[i] = 0 if (self.__obj[i] == 1 and argObj[i] == 0) else 1
    
    def logicNand(self, arg):
        """In: other BinaryObject
        Out: void
        Desc: Applies logical NAND (AND + NOT) operation to the internal object data and other's object data and writes the result to itself

        :param arg: 

        """
        self.logicAnd(arg)
        self.logicNot()
    
    def logicNor(self, arg):
        """In: other BinaryObject
        Out: void
        Desc: Applies logical NOR (OR + NOT) operation to the internal object data and other's object data and writes the result to itself

        :param arg: 

        """
        self.logicOr(arg)
        self.logicNot()

    #shifts

    def __lsl_1(self):
        temp = self.__obj[1:]
        temp.append(0)
        self.__obj = temp
    
    def __lsr_1(self):
        temp = [0]
        for elem in self.__obj[:-1]:
            temp.append(elem)
        self.__obj = temp

    def logicShiftLeft(self, pos):
        for i in range(pos):
            self.__lsl_1()

    def logicShiftRight(self, pos):
        for i in range(pos):
            self.__lsr_1()
    
    def __asl_1(self):
        #sign = self.__obj[0]
        self.__lsl_1()
        #self.__obj[0] = sign
    
    def __asr_1(self):
        sign = self.__obj[0]
        self.__lsr_1()
        self.__obj[0] = sign

    def ariphmeticShiftLeft(self, pos):
        for i in range(pos):
            self.__asl_1()

    def ariphmeticShiftRight(self, pos):
        for i in range(pos):
            self.__asr_1()
    
    def __csl_1(self):
        first = self.__obj[0]
        self.__lsl_1()
        self.__obj[-1] = first
    
    def __csr_1(self):
        last = self.__obj[-1]
        self.__lsr_1()
        self.__obj[0] = last

    def cyclicShiftLeft(self, pos):
        for i in range(pos):
            self.__csl_1()

    def cyclicShiftRight(self, pos):
        for i in range(pos):
            self.__csr_1()
    #def ariphmeticShiftLeft(self, pos):
    #    sign = self.__obj[0]
        
    
    #def ariphmeticShiftRight(self, pos):
    #    pass

    

    
    def add(self,arg):
        """In: other BinaryObject
        Out: void
        Desc: Adds value of the argument to the internal

        :param arg: 

        """
        argObj = arg.readNative()
        for i in range(len(self.__obj)):
            self.__obj[i] += argObj[i]
        for i in range(len(self.__obj) - 1, 0, -1):
            if self.__obj[i] > 1:
                self.__obj[i] -= 2
                self.__obj[i-1] += 1
        if self.__obj[0] > 1:
            self.__obj[0] -= 2
    
    def advancedCode(self):
        """In: void
        Out: void
        Desc: Writes to the internal object data advanced code of the current object value


        """
        self.logicNot()
        temp = BinaryObject(self.__size)
        one = [0 for _i in range(self.__size-1)]
        one.append(1)
        temp.write(one)
        self.add(temp)
    
    def sub(self, arg):
        """In: other BinaryObject
        Out: void
        Desc: Substractss value of the argument from the internal

        :param arg: 

        """
        arg.advancedCode()
        self.add(arg)
        #arg.advancedCode()
