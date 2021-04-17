from g_pm import PrimaryMemory
from g_bo import BinaryObject
from g_pa import Parser
#from g_rm import RegisterMemory

class VirtualMachine:
    def __init__(self, memorySize, name = '', shortName = '', author = '', authorEmail = '', version = ''):
        self.__mem = PrimaryMemory(memorySize)
        self.__size = memorySize
        self.__parser = Parser()
        self.__commandFamilies = {
            'io' : {'wrt', 'rd', 'out'},
            'logic' : {'and', 'not', 'or', 'xor', 'imp', 'eqv', 'nand', 'nor'},
            'data' : {'mov', 'copy'}
        }
        self.__meta = {
            'name' : name,
            'shortName' : shortName,
            'author' : author,
            'authorEmail' : authorEmail,
            'version' : version,
        }
        self.__outputStream = ''
        
    def execute(self, command):
        p_com = self.__parser.parse(command)
        if p_com['com'] in self.__commandFamilies['io']:
            if p_com['com'] == 'wrt':
                o_t_w = BinaryObject(8)
                o_t_w.write(list(map(int, list(p_com['arg2']))))
                self.__mem.write(int(p_com['arg1']), o_t_w)
            elif p_com['com'] == 'rd':
                return self.__mem.read(int(p_com['arg1']))
            elif p_com['com'] == 'out':
                out = self.__mem.read(int(p_com['arg1']))
                print(out)
                self.__outputStream += f'{out}\n'
        elif p_com['com'] in self.__commandFamilies['logic']:
            if p_com['com'] == 'and':
                self.__mem.logicAnd(int(p_com['arg1']), int(p_com['arg2']))
            elif p_com['com'] == 'not':
                self.__mem.logicNot(int(p_com['arg1']))
            elif p_com['com'] == 'or':
                self.__mem.logicOr(int(p_com['arg1']), int(p_com['arg2']))
            elif p_com['com'] == 'xor':
                self.__mem.logicXor(int(p_com['arg1']), int(p_com['arg2']))
            elif p_com['com'] == 'imp':
                self.__mem.logicImp(int(p_com['arg1']), int(p_com['arg2']))
            elif p_com['com'] == 'eqv':
                self.__mem.logicEqv(int(p_com['arg1']), int(p_com['arg2']))
            elif p_com['com'] == 'nand':
                self.__mem.logicNand(int(p_com['arg1']), int(p_com['arg2']))
            elif p_com['com'] == 'nor':
                self.__mem.logicNor(int(p_com['arg1']), int(p_com['arg2']))
        elif p_com['com'] in self.__commandFamilies['data']:
            if p_com['com'] == 'mov':
                self.__mem.move(int(p_com['arg1']), int(p_com['arg2']))
            if p_com['com'] == 'copy':
                self.__mem.copy(int(p_com['arg1']), int(p_com['arg2']))
        
    def bootUpTerminal(self):
        print('[%s v. %s][by %s (%s)]' % (self.__meta['name'], self.__meta['version'], self.__meta['author'], self.__meta['authorEmail']))
        while True:
            command = input('%s>' % (self.__meta['shortName']))
            if command == 'shtd':
                break
            else:
                self.execute(command)
    
    def getSelf(self):
        return VirtualMachine(len(self.__mem), self.__meta['name'], self.__meta['shortName'], self.__meta['author'], self.__meta['authorEmail'], self.__meta['version'])
    
    def runFile(self, filename):
        with open(filename, 'r', encoding='utf8') as f:
            commands = f.readlines()
            for command in commands:
                self.execute(command)

    def getState(self):
        state = 'Cell No = Cell value\n'
        for i in range(self.__size):
            cellVal = self.__mem.read(i)
            if cellVal == [0,0,0,0,0,0,0,0]:
                break
            else:
                state += f'{i} = {cellVal}\n'
        return state
    
    def getOutputStream(self):
        return self.__outputStream

