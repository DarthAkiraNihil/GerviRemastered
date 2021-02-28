class Register:
    def __init__(self):
        self.__registerData = None
    
    def setValue(self, value):
        self.__registerData = value
    
    def resetValue(self):
        self.__registerData = None