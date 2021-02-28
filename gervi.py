import sys, pickle
sys.path.append('core/GRE')
from g_vm import VirtualMachine
vm_file = open(sys.argv[1], 'rb')
vm = pickle.load(vm_file)
vm_file.close()
vm.bootUpTerminal()