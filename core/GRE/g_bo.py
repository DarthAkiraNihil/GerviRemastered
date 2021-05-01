class InvalidWriteDataException(BaseException): ...

class NotEqualArgumentsLengthException(BaseException): ...

class BinaryObject:
    def __init__(self, size):
        self.__size = size
        self.__obj = [0 for _i in range(size)]
    
    def write(self, data):
        if data.count(0) + data.count(1) != len(data) or len(data) != self.__size:
            raise InvalidWriteDataException(f'Write data contains non-0-1 values or length of it not equal with object size({self.__size})')
        else:
            self.__obj = data

    def readNative(self):
        return self.__obj

    def readString(self):
        return ''.join(map(str, self.__obj))

    def getSize(self):
        return self.__size
    
    def __checkLength(self, arg):
        if self.__size != arg.getSize():
            raise NotEqualArgumentsLengthException('write some info later') #TODO exception message

    def logicNot(self):
        for i in range(len(self.__obj)):
            self.__obj[i] = 0 if self.__obj[i] == 1 else 1

    def logicAnd(self, arg):
        argObj = arg.readNative()
        self.__checkLength(arg)
        for i in range(len(self.__obj)):
            self.__obj[i] = 1 if self.__obj[i] == argObj[i] == 1 else 0

    def logicOr(self, arg):
        argObj = arg.readNative()
        self.__checkLength(arg)
        for i in range(len(self.__obj)):
            self.__obj[i] = 0 if self.__obj[i] == argObj[i] == 0 else 1
    
    def logicXor(self, arg):
        argObj = arg.readNative()
        self.__checkLength(arg)
        for i in range(len(self.__obj)):
            self.__obj[i] = 1 if self.__obj[i] != argObj[i] else 0
    
    def logicEqv(self, arg):
        argObj = arg.readNative()
        self.__checkLength(arg)
        for i in range(len(self.__obj)):
            self.__obj[i] = 1 if self.__obj[i] == argObj[i] else 0
    
    def logicImp(self, arg):
        argObj = arg.readNative()
        self.__checkLength(arg)
        for i in range(len(self.__obj)):
            self.__obj[i] = 0 if (self.__obj[i] == 1 and argObj[i] == 0) else 1
    
    def logicNand(self, arg):
        self.logicAnd(arg)
        self.logicNot()
    
    def logicNor(self, arg):
        self.logicOr(arg)
        self.logicNot()


    def add(self,arg):
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
        self.logicNot()
        temp = BinaryObject(self.__size)
        one = [0 for _i in range(self.__size-1)]
        one.append(1)
        temp.write(one)
        self.add(temp)

    def sub(self, arg):
        arg.advancedCode()
        self.add(arg)
