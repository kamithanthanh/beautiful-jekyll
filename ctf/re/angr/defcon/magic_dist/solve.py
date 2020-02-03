from angr import * 
from claripy import * 
import sys 


filename = sys.argv[1]
BASE = 0x400000
p = Project(filename)
cfg = p.analyses.CFG() 
list_function = p.kb.functions.items()  
target_function = list_function[-11][0]    # last final function 

state = p.factory.blank_state(addr=target_function)  
simgr = p.factory.simgr(state) 

# compute flag length from number of function
len_flag = (len(list_function) - 24) / 2
print("[*] Length flag = " + str(len_flag))
flag = BVS("flag", len_flag * 8) 

# set up paramterers for functions
memory_write = 0x20200F + BASE 
state.memory.store(memory_write, flag) 
state.regs.rdi = memory_write 

# calculate from instruction counts 
good = target_function + len_flag * 17 + 25 
print("Good point = " + hex(good))
simgr.explore(find=(good)) 

if simgr.found : 
    s = simgr.found[0] 
    print(s.solver.eval(flag, cast_to=bytes))
else : 
    print("No fucking that easy ....")
