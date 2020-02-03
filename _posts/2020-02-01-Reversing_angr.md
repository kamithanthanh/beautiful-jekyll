---
layout : post
title : Pratice Reversing with Angr Example 
--- 

# Mở đầu   
Sau khi làm quen với angr xong, mình tiếp tục hành trình làm những ví dụ được Angr liệt kê tại [đây](https://docs.angr.io/examples#whitehat-ctf-2015-crypto-400)  
Đây đều là những challenge ctf cũ nên rất bổ ích và thực tế. Nói là làm nhưng thực ra để tận dụng thời gian mình đọc wu và tối ưu code cũng như làm rõ những điều mình chưa hiểu rõ về angr. 😁😁😁

# Table of Content   
  - [**Whitehat Crypto 400**](#wu1)
  - [**Defcon 2017 Magic**](#wu2)   
  
<a name="wu1"></a>   
    
    


# Whitehat Crypto400 
Cũng khá là ngạc nhiên khi một challenge của Việt Nam được lấy ví dụ ở đây \(￣︶￣*\))\(￣︶￣*\))\(￣︶￣*\))Việt Nam chúng ta thật tuyệt 🤗🤗🤗    
Sau khi làm những bước reverse cơ bản thì chúng ta cần chú ý những hàm sau :    

![](/ctf/re/angr/whitehat/hinh1.PNG)    

![](/ctf/re/angr/whitehat/hinh2.PNG)    

Chúng ta sẽ dùng Angr để vượt qua ```check1```.```Check1``` lấy tham số truyền vào là địa chỉ của argv[1] với độ dài là 8. Sau đó được copy vào vùng nhớ ```0x6C4B20```. Tiếp tục là một loạt các check số học khác nhau 🧐🧐🧐 Đây là một trường hợp rất thích hợp để dùng angr. Chúng ta sẽ dùng angr để tìm tất cả các input đầu vào có thể để vượt qua được ```check1```.   

## Step 1 : Hook some function to speed up angr   
Do đây là static binary nên angr sẽ thực thi rất chậm. Do đó chúng ta cần thay thế một số hàm mặc định trong libc bằng hàm built-in trong angr.   

```python
libc_start_addr = 0x4018B0 

p.hook(libc_start_addr, SIM_PROCEDURES['glibc']['__libc_start_main']())
p.hook(0x422690,  SIM_PROCEDURES['libc']['memcpy']())
p.hook(0x408F10,  SIM_PROCEDURES['libc']['puts']()) 
```   

Cùng với đó, hàm ```strlen``` không phải là hàm của C mà mình đặt tên thế thôi 😂 Ta đã biết giá trị của hàm này nên cũng thực hiện hook nó với một hàm set giá trị trả về là 8 để tối ưu.   
```python
def set_length(state) : 
    state.regs.rax = 8 

p.hook(0x4016BE, set_length, length=5) 
p.hook(0x40168E, set_length, length=5) 
```    

Cuối cùng, trong binary này có một hàm anti debug là ```sub_401438```.   

![](/ctf/re/angr/whitehat/hinh3.PNG)   

Mình lưu lại nó hơi sai tí 😂😂😂 Hàm này dùng ```ptrace``` để thực hiện công việc này. Chúng ta cần bypass hàm này bằng cách thay thế nó bằng một hàm không làm gì cả :)))   

```python
def do_nothing (state) : 
    pass 
p.hook(0x401438, do_nothing, length=262)    # length of target function 
```   

## Step 2 : Create Variable and Simulation   
Chúng ta tiến hành tạo biến input có độ dài 8 kí tự.  
```python
arg1 = BVS('arg1', 8 * 8) 
state = p.factory.entry_state(args=["name", arg1]) 
``` 
Tham số ```args``` ở đây thể hiện cho tham số truyền vào của binary.  
Thêm ràng buộc của flag là phải là kí tự in được :   
```
for c in arg1.chop(bits=8) : 
    state.add_constraints(And(c > 33, c < 128))
```
## Step 3 : Get all result of check1    
Tiến hành explore như bình thường :    
```python
simgr = p.factory.simulation_manager(state)  
simgr.explore(find=0x4017CF)      
```   


Do chúng ta cần liệt kê tất cả các giá trị có được của kết quả, ta cần dùng hàm ```eval_upto```.   
```python
s = simgr.found[0] 
posible_values = [s.solver.eval_upto(arg1.get_bytes(i, 2), 256 * 256, cast_to=bytes) for i in range(0,8,2)]
```   
Vì những ràng buộc trong ```check1``` đều theo cặp, nên để giảm tải lượng tính toán cho Angr thì chúng ta tiến hành giải theo từng cặp biến 1 với số lượng đáp án lớn nhất cho từng cặp là ```256 * 256```.    
Sau đó chúng ta tiến hành nhóm từng cặp lại, thu được toàn bộ câu trả lời :   
```python
possibilities = list(itertools.product(*posible_values))
```   

## Step 4 : Brute force   
Do số lượng đáp án thu được từ bước ba rất nhỏ nên chúng ta có thể brute force arg1.   
```python 
print('[*] brute-forcing %d possibilities' % len(possibilities))
for guess in progressbar.ProgressBar(widgets=[progressbar.Counter(), ' ', progressbar.Percentage(), ' ', progressbar.Bar(), ' ', progressbar.ETA()])(possibilities):
    guess_str = b''.join(guess)
    stdout,_ = subprocess.Popen(["./whitehat_crypto400", guess_str.decode("ascii")], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    if b'FLAG' in stdout:
        print(stdout)  
        print(guess_str.decode("ascii"))
        break
```

<a name="wu2"></a>

# Defcon 2017 - Magic    
Defcon 2017 có một chuỗi bài liên quan tới tự động hóa trong reverse engineering. Đây là bài đầu tiên trong chuỗi series này. Và cũng thực hiện những kĩ thuật đơn giản nhất.   
Chúng ta có một thư mục chứa khoảng 20 files. Thử nghĩ đến chuyện sẽ ngồi reverse hết đống này bằng IDA xem ◑﹏◐ Reverse sẽ biến thành địa ngục. :)))   
Lucki là chúng ta có thể tự động hóa quá trình này. Vì các file này có kết cấu tương tự nhau.   

```main```    
![](/ctf/re/angr/defcon/magic_dist/hinh1.PNG)   

```sub_DF6```    
![](/ctf/re/angr/defcon/magic_dist/hinh2.PNG)    

Trong ```sub_DF6``` sẽ có những hàm có chức năng tương tự như sau :   

```sub_93B```   

![](/ctf/re/angr/defcon/magic_dist/hinh3.PNG)    

Bài này sẽ không khó nếu chỉ có một file. Chúng ta có thể tự động hóa quá trình này bằng một đoạn code angr đơn giản  :    
```python
  from angr import * 
from claripy import * 
import sys 


filename = sys.argv[1]
BASE = 0x400000
p = Project(filename)

target_function = ???

state = p.factory.blank_state(addr=target_function)  
simgr = p.factory.simgr(state) 

# compute flag length from number of function
len_flag = ???
print("[*] Length flag = " + str(len_flag))
flag = BVS("flag", len_flag * 8) 

# set up paramterers for functions
memory_write = 0x20200F + BASE 
state.memory.store(memory_write, flag) 
state.regs.rdi = memory_write 

# calculate from instruction counts 
good = ???  
print("Good point = " + hex(good))
simgr.explore(find=(good)) 

if simgr.found : 
    s = simgr.found[0] 
    print(s.solver.eval(flag, cast_to=bytes))
else : 
    print("No fucking that easy ....")
```

Chúng ta sẽ bắt đầu từ ```sub_DF6```, thiết lập biến flag dài 46 kí tự, ghi vào bộ nhớ và truyền địa chỉ của bộ nhớ đó vào thanh ghi rdi. Điểm kết thúc là diểm vượt qua tất cả các check. Mọi công việc diễn ra như chương trình angr đơn giản.   

Tuy nhiên có một số tham số chưa xác định, thay đổi theo từng binary. Chúng ta sẽ dùng angr để tự động xác định tham số này.   
Chúng ta dùng công cụ ```analyses``` của angr để phân tích biểu đồ của chương trình này , liệt kê các function :   

```python
cfg = p.analyses.CFG() 
list_function = p.kb.functions.items()  
```   
Lại để ý , hàm mục tiêu lại luôn nằm gần cuối, nên việc có bao nhiêu hàm check không quan trọng, ta chỉ cần lần từ cuối lên là tìm được :   
![](/ctf/re/angr/defcon/magic_dist/hinh4.PNG)     

```python
target_function = list_function[-11][0]    # last final function 
```

Tiếp đến dựa theo những tính toán thủ công dựa trên số hàm và số câu lệnh của hàm ```sub_DF6```, mình thu được thêm những mảnh ghép còn lại :  
```python
len_flag = (len(list_function) - 24) / 2   
good = target_function + len_flag * 17 + 25  
```

Ok cách này có chút thủ công nhưng cũng ra được kết quả. Mình còn định dùng unicorn để giải cơ :]] Mà phức tạp quá nên thôi. QUa bài tiếp theo của defcon ta sẽ biết cách khác để tìm được các tham số trên bằng ```capstone```.    



