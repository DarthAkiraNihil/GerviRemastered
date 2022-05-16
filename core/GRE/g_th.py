class Throwable:
    def __init__(self, exceptionName, exceptionLevel, messageTemplate):
        self.__name = exceptionName
        self.__level = exceptionLevel
        self.__msgTemplate = messageTemplate
    
    def getName(self):
        return self.__name
    
    def getLevel(self):
        return self.__level
    
    def throw(self, *args):
        msg = self.__msgTemplate % (args)
        return '%s [%s]: %s' % (self.__name, self.__level, msg)