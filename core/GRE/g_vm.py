from g_pm import PrimaryMemory
from g_pa import Parser
from g_es import ExceptionSystem
import g_sysvars
#from g_rm import RegisterMemory

class VirtualMachine:
    def __init__(self, memorySize, name = '', shortName = '', author = '', authorEmail = ''):
        self.__mem = PrimaryMemory(memorySize)
        self.__size = memorySize
        self.__parser = Parser()
        self.__commandFamilies = {
            'io' : {'wrt', 'rd', 'out'},
            'logic' : {'and', 'not', 'or', 'xor', 'imp', 'eqv', 'nand', 'nor'},
            'shifts' : {'lsl', 'lsr', 'asl', 'asr', 'csl', 'csr'},
            'math' : {'add', 'sub'},
            'data' : {'mov', 'copy'},
            'jumps' : {'jmp'},
            'vars' : {'als'}
        }
        self.__meta = {
            'name' : name,
            'shortName' : shortName,
            'author' : author,
            'authorEmail' : authorEmail,
            'gerviVersion' : g_sysvars.GERVI_VERSION
        }
        self.__outputStream = ''
        self.__ip = 0
        self.__last = 0
        self.__aliases = {}

        self.__exceptionSystem = ExceptionSystem()
        
        
    def execute(self, command):
        if command.isspace():
            return
        have_comment = command.find(';')
        if have_comment != -1:
            command = command[:have_comment]
            if command.endswith(' '):
                command = command.rstrip()
        
        p_com = self.__parser.parse(command)
        for key in p_com.keys():
            if key == 'com':
                pass
            elif p_com[key] in self.__aliases:
                p_com[key] = self.__aliases[p_com[key]]
                

        if p_com['com'] in self.__commandFamilies['jumps']:
            if p_com['com'] == 'jmp':
                self.__ip = int(p_com['arg1'])
        else:
            if p_com['com'] in self.__commandFamilies['io']:
                if p_com['com'] == 'wrt':
                    self.__mem.write(int(p_com['arg1']), int(p_com['arg2'], 2))
                    self.__last = max(self.__last, int(p_com['arg1']))
                elif p_com['com'] == 'rd':
                    return self.__mem.read(int(p_com['arg1']))
                elif p_com['com'] == 'out':
                    #out = self.__mem.read(int(p_com['arg1']))
                    out = ''.join(map(str, self.__mem.read(int(p_com['arg1']))))
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
                elif p_com['com'] == 'copy':
                    self.__mem.copy(int(p_com['arg1']), int(p_com['arg2']))
            elif p_com['com'] in self.__commandFamilies['math']:
                if p_com['com'] == 'add':
                    self.__mem.add(int(p_com['arg1']), int(p_com['arg2']))
                elif p_com['com'] == 'sub':
                    self.__mem.sub(int(p_com['arg1']), int(p_com['arg2']))
            elif p_com['com'] in self.__commandFamilies['vars']:
                if p_com['com'] == 'als':
                    self.__aliases[p_com['arg1']] = p_com['arg2']
            elif p_com['com'] in self.__commandFamilies['shifts']:
                if p_com['com'] == 'lsl':
                    self.__mem.logicShiftLeft(int(p_com['arg1']), int(p_com['arg2']))
                elif p_com['com'] == 'lsr':
                    self.__mem.logicShiftRight(int(p_com['arg1']), int(p_com['arg2']))
                elif p_com['com'] == 'asl':
                    self.__mem.ariphmeticShiftLeft(int(p_com['arg1']), int(p_com['arg2']))
                elif p_com['com'] == 'asr':
                    self.__mem.ariphmeticShiftRight(int(p_com['arg1']), int(p_com['arg2']))
                elif p_com['com'] == 'csl':
                    self.__mem.cyclicShiftLeft(int(p_com['arg1']), int(p_com['arg2']))
                elif p_com['com'] == 'csr':
                    self.__mem.cyclicShiftRight(int(p_com['arg1']), int(p_com['arg2']))
                
            self.__ip += 1
        
        
    def bootUpTerminal(self):
        print('[%s][by %s (%s)][Gervi version: %s]' % (self.__meta['name'], self.__meta['author'], self.__meta['authorEmail'], self.__meta['gerviVersion']))
        while True:
            command = input('%s>' % (self.__meta['shortName']))
            if command == 'shtd':
                break
            else:
                self.execute(command)
    
    #! DEPRECATED
    def getSelf(self):
        return VirtualMachine(len(self.__mem), self.__meta['name'], self.__meta['shortName'], self.__meta['author'], self.__meta['authorEmail'], self.__meta['version'])
    
    def runFile(self, filename):
        with open(filename, 'r', encoding='utf8') as f:
            commands = f.readlines()
            while self.__ip < len(commands):
                self.execute(commands[self.__ip])
            self.__ip = 0
            #for command in commands:
            #    self.execute(command)

    def getState(self):
        meta = self.getMetaInfoString()
        state = meta + '\nCell Number |      Bin | Dec | Hex\n'
        for i in range(self.__last+1):
            cellVal = self.__mem.read(i)
            #if cellVal == [0,0,0,0,0,0,0,0]:
            #    break
            #else:
            #formatted = ''.join(map(str, cellVal))
            decVal = int(cellVal, 2)
            hexVal = hex(decVal)[2:]
            state += '%11d | %8s | %3d |  %2s\n' % (i, cellVal, decVal, hexVal)
            #state += f'{i} = {formatted}\n'
        return state
    
    def getOutputStream(self):
        return self.__outputStream
    
    def getMetaInfoString(self):
        return 'Using %s by %s\nGervi version %s\nMemory size: %s' % (self.__meta['name'], self.__meta['author'], self.__meta['gerviVersion'], self.__transformSize(self.__size))
    
    def __transformSize(self, size):
        #bytes, KB, MB, GB
        byteSize = self.__size
        kBytes, mBytes, gBytes = byteSize / 1024, byteSize / (1024**2), byteSize / (1024**3)
        if kBytes < 0.95:
            return f'{byteSize} bytes'
        elif kBytes >= 0.95 and mBytes < 0.95:
            return f'{kBytes} KB ({byteSize} bytes)'
        elif mBytes >= 0.95 and gBytes < 0.95:
            return f'{mBytes} MB ({byteSize} bytes)'
        else:
            return f'{gBytes} GB ({byteSize} bytes)'
    def exportMemory(self):
        pass

    def importMemory(self, pmiFile):
        pass

    def mountMemoryCard(self, mcFile):
        pass

    def unmountMemoryCard(self):
        pass

    def safeUnmountMemoryCard(self):
        pass

