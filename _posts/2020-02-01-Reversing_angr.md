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
  - [**Defcon 2017 Sorcery**](#wu3)
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

Hàm ```main```:     

![](/ctf/re/angr/defcon/magic_dist/hinh1.PNG)   

Hàm ```sub_DF6```:    

![](/ctf/re/angr/defcon/magic_dist/hinh2.PNG)    

Trong ```sub_DF6``` sẽ có những hàm có chức năng tương tự như sau :   

Hàm ```sub_93B``` :   

![](/ctf/re/angr/defcon/magic_dist/hinh3.PNG)    

Bài này sẽ không khó nếu chỉ có một file. Chúng ta có thể tự động hóa quá trình này bằng một đoạn code angr không quá phức tạp 😁😁😁 .Chúng ta sẽ bắt đầu từ ```sub_DF6```, thiết lập biến flag dài 46 kí tự, ghi vào bộ nhớ và truyền địa chỉ của bộ nhớ đó vào thanh ghi rdi. Điểm kết thúc là diểm vượt qua tất cả các check. Mọi công việc diễn ra như chương trình angr đơn giản.   

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

Last solution : [solution.py](https://github.com/hacmao/hacmao.github.io/raw/master/ctf/re/angr/defcon/magic_dist/solve.py)   

Ok cách này có chút thủ công nhưng cũng ra được kết quả. Mình còn định dùng unicorn để giải cơ :]] Mà phức tạp quá nên thôi. QUa bài tiếp theo của defcon ta sẽ biết cách khác để tìm được các tham số trên bằng ```capstone```.    




<a name="wu3"></a>




# Defcon 2017 Sorcery    
Bài này là một file khá là phức tạp. Đoạn reverse đầu tiên để tìm ra được function mà chúng ta quan tâm cũng sẽ tiêu tốn khá nhiều thời gian. Vì file này nó cấp phát một vùng nhớ, stack mới để thực thi chương trình chính thì phải. 😁😁😁 Do đang tập trung vào angr nên là mình không tập trung vào phần reverse này lắm :vv 
༼ つ ◕_◕ ༽つ »»» Kinh nghiệm sẽ là tập trung vào những cái đơn giản, hàm đơn giản trước, hàm dùng nhiều hàm lạ thì để sau .Nhưng không được bỏ qua đoạn nào, vì đoạn code quan trọng có thể nằm bất kì đâu.       

Như trong trường hợp này, trong hàm main sẽ gọi đến hàm ```sub_30fc```. Trong hàm này sẽ có một chuỗi so sánh check flag :    

![](/ctf/re/angr/defcon/sorcery_dist/hinh1.PNG)     

Chúng ta sẽ dùng angr + capstone để extract ra được những giá trị khi tiến hành so sánh.   
Chúng ta sẽ tiếp tục dùng phương thức ```analyses``` để explore graph của chương trình. Tuy nhiên lần này sẽ thêm giá trị ```auto_load_libs=False``` để chương trình thực hiện nhanh hơn và không có lỗi.   
```python
p = Project(s, auto_load_libs = False)   
cfg = p.analyses.CFG(show_progressbar=True) 
```    

Lấy graph của hàm ```sub_30fc``` về để phân tích. Ta hiểu nôm na graph sẽ như sau :    

![](/ctf/re/angr/defcon/sorcery_dist/sample-gimple-cfg.png)    

Graph trong angr được biểu thị bằng các block. Mỗi block gồm nhiều câu lệnh khác nhau. Block được chia theo phép toán thay đổi luồng thực thi. Ta tiến hành sắp xếp lại các block theo thứ tự tăng dần rồi phân tích từng block :   
```python
func = cfg.functions[0x4030fc]      # get graph code of functions 0x4030fc
for block in func.blocks:     
```
Mỗi block là một class, chuyển về các đối tượng instructments  bằng câu lệnh ```block.capstone.insns```.  
Tiếp đến, chúng ta phân tích từng câu lệnh, so sánh xem khi nào câu lệnh là phép so sánh  ```al``` hoặc ```bl``` với một sô thì tách số đó cộng vào flag 😀😀😀    
```python
flag = "" 
    for block in func.blocks: 
        # get instruction start with al, cl 
        ins = [insn for insn in block.capstone.insns if insn.mnemonic == "cmp" and    # if cmp 
                  insn.operands[0].type == 1   # if not register 
                      and insn.operands[0].reg in (2, 10)  ] # if not al or cl  
        if not ins :         
            continue 
        else : 
            c = ins[0].operands[1].imm 
            flag += chr(c) 
```
Xem thêm về capstone constant tại [đây](https://github.com/aquynh/capstone/blob/master/bindings/python/capstone/x86_const.py)     




