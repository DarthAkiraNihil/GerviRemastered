import sys, pickle
sys.path.append('core/GRE')
from g_vm import VirtualMachine
if len(sys.argv) == 1:
    print('Usage: vmFile mode [filename]\nmode can be:\n-t - terminal mode, not require filename\n-f - file run mode, require filename')
else:
    vm_file = open(sys.argv[1], 'rb')
    vm = pickle.load(vm_file)
    vm_file.close()
    if sys.argv[2] == '-t':
        vm.bootUpTerminal()
    elif sys.argv[2] == '-f':
        vm.runFile(sys.argv[3])