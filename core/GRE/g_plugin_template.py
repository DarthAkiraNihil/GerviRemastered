import pickle

class IsInitializedPluginException(BaseException): ...

class PluginTemplate:
    def __init__(self):
        self.__name = 'your_plugin_name'
        self.__attachedMemory = None
        self.__inited = False
    def compile(self):
        if not self.__inited:
            with open(f'{self.__name}.gcp', 'wb+') as fin:
                pickle.dump(self, fin)
        else:
            raise IsInitializedPluginException('Compiling plugin after initialization is forbidden')

    def initialize(self, memory):
        self.__attachedMemory = memory
    
    def execute(self, command):
        pass
    #your plugin code here