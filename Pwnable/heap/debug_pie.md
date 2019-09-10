---
layout : post 
title : Debug Pie Binary  
--- 

Pie là một cơ chế bảo vệ của file. Khi tính năng này được bật thì chúng ta không thể biết địa chỉ của tất cả các hàm trong chương trình.Thông thường khi PIE không được bật chúng ta sẽ biết được địa chỉ các hàm như main, các hàm con, địa chỉ bss, got, ... Và do đó khi PIE được bật sẽ gây khó khăn trong việc debug cũng như đặt breakpoint .Cách giải quyết mình học được từ [đây](https://teamrocketist.github.io/2019/08/17/Pwn-RedpwnCTF-penpal-world/)  

```python  
def get_PIE(proc):
    memory_map = open("/proc/{}/maps".format(proc.pid),"rb").readlines()
    return int(memory_map[0].split("-")[0],16)

def debug(bp):
    #bp = [0xea0,0xd31,0xc52]
    #bp = [0x00000dfb,0x00000b7c,0x00000d10]
    script = ""
    PIE = get_PIE(sh)
    PAPA = PIE
    for x in bp:
        script += "b *0x%x\n"%(PIE+x)
    gdb.attach(sh,gdbscript=script) 
```  
Hàm ```get_PIE``` sẽ lấy địa chỉ PIE rồi recovery lại tất cả địa chỉ trước khi PIE, tiến hành đặt break point rồi debug như thường thôi.
