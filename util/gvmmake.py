import sys
sys.path.append('../core/GRE')

from g_vm import VirtualMachine
import g_sysvars
import pickle, lzma

class Application:
    def __init__(self):
        self.__showDebug = True
        self.__convert = {
            'Name': 'Virtual machine name',
            'Short': 'Short name',
            'MemSize': 'Memory size',
            'Author': 'Author',
            'Email': 'Author`s E-mail'
        }

    def run(self, args):
        if len(args) == 0:
            print('Usage: prototypeFileName [options...]\nThe options are:\n-q - quiet mode, disables any messages')
            return None
        else:
            if args.count('-q') > 0:
                self.__showDebug = False

            self.__debugMsg(f'Creating a virtual machine from the prototype {args[0]}')

            vmData = self.__extractData(args[0])
            outName = vmData.pop('Out')

            for elem in vmData.keys():
                self.__debugMsg('%s: %s' % (self.__convert[elem], vmData[elem]))
            self.__debugMsg(f'Gervi system version: {g_sysvars.GERVI_VERSION}')

            vm = VirtualMachine(int(vmData['MemSize']), vmData['Name'], vmData['Short'], vmData['Author'], vmData['Email'])

            self.__debugMsg('Successfully created VM object')
            self.__debugMsg('Dumping...')

            bytesVM = pickle.dumps(vm)
            #with open('%s.gvm' % (vmData['Out']), 'wb+') as f:
            #    pickle.dump(vm, f)
            self.__debugMsg('Compressing...')

            with lzma.open('%s.gvm' % (outName), 'wb', preset=1) as fin:
                fin.write(bytesVM)

            self.__debugMsg(f'Succesfully dumped VM into the file {outName}.gvm')
                
    def __extractData(self, file):
        self.__debugMsg('Extractiing data from the file...')

        with open(file, 'r', encoding='utf8') as fin:
            lines = fin.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].split(':')
                if lines[i][1].endswith('\n'):
                    lines[i][1] = lines[i][1][:-1]
            data = {}
            #print(lines)
            for line in lines:
                data[line[0]] = line[1]
                
            return data
            

    def __debugMsg(self, msg):
        if self.__showDebug:
            print(msg)

app = Application()
app.run(sys.argv[1:])
