from angr import * 
from claripy import * 
import sys 

def solve(s) : 
    p = Project(s, auto_load_libs = False)   

    BASE = 0x400000 
    target = BASE + 0x30FC 
    state = p.factory.blank_state(addr=target) 
    simgr = p.factory.simulation_manager(state) 

    cfg = p.analyses.CFG(show_progressbar=True) 
    func = cfg.functions[0x4030fc]      # get graph code of functions 0x4030fc 

    flag = "" 
    for block in func.blocks: 
        # get instruction start with al, cl 
        ins = [insn for insn in block.capstone.insns if insn.mnemonic == "cmp" and insn.operands[0].type == 1 and insn.operands[0].reg in (2, 10) ] 
        if not ins : 
            continue 
        else : 
            c = ins[0].operands[1].imm 
            flag += chr(c) 
    return flag 

if __name__ == "__main__" : 
    print(solve(sys.argv[1]))