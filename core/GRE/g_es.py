from g_er import GerviException

class ExceptionSystem:
    def __init__(self):
        self.__exceptionArray = []
        self.__exceptionIndexes = {}
        self.__valOfExceptions = 0

    def addException(self, exception):
        self.__exceptionArray.append(exception)
        self.__exceptionIndexes[exception.throwable.name] = self.__valOfExceptions
        self.__valOfExceptions += 1
    
    def throw(self, name, *args):
        index = self.__exceptionIndexes[name]
        return self.__exceptionArray[index].throw(args)
