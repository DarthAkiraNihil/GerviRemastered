import sys
sys.path.append('../core/GRE')

from g_vm import VirtualMachine
import pickle

class Application:
    def run(self, args):
        if args[0] == '-u':
            vmf = open(args[1], 'rb')
            vm = pickle.load(vmf)
            vmf.close()
            vm = vm.getSelf()
            with open(args[1], 'wb') as f:
                pickle.dump(vm, f)
        else:
            vm = VirtualMachine(int(args[0]), args[1], args[2], args[3], args[4], args[5])
            with open(f'{args[6]}.gvm', 'wb+') as f:
                pickle.dump(vm, f)

app = Application()
app.run(sys.argv[1:])
