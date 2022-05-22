import sys
sys.path.append('../core/GRE')

from g_vm import VirtualMachine
import pickle

class Application:
    def run(self, args):
        if len(args) == 0:
            print('Usage: prototypeFileName')
            return None
        else:
            vmData = self.__extractData(args[0])
            vm = VirtualMachine(int(vmData['MemSize']), vmData['Name'], vmData['Short'], vmData['Author'], vmData['Email'], vmData['Ver'])
            with open('%s.gvm' % (vmData['Out']), 'wb+') as f:
                pickle.dump(vm, f)
                
    def __extractData(self, file):
        with open(file, 'r', encoding='utf8') as fin:
            lines = fin.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].split(':')
                if lines[i][1].endswith('\n'):
                    lines[i][1] = lines[i][1][:-1]
            data = {}
            print(lines)
            for line in lines:
                data[line[0]] = line[1]
            return data


app = Application()
app.run(sys.argv[1:])
