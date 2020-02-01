---
layout : post
title : Reversing with Angr Example 
--- 

# Mở đầu   
Sau khi làm quen với angr xong, mình tiếp tục hành trình làm những ví dụ được Angr liệt kê tại [đây](https://docs.angr.io/examples#whitehat-ctf-2015-crypto-400)  
Đây đều là những challenge ctf cũ nên rất bổ ích và thực tế. Nói là làm nhưng thực ra để tận dụng thời gian mình đọc wu và tối ưu code cũng như làm rõ những điều mình chưa hiểu rõ về angr. 😁😁😁

# Table of Content   
  - [**Whitehat Crypto 400**](#wu1)
<a name="wu1"></a>   

# Whitehat Crypto400 
Cũng khá là ngạc nhiên khi một challenge của Việt Nam được lấy ví dụ ở đây \(￣︶￣*\))\(￣︶￣*\))\(￣︶￣*\))Việt Nam chúng ta thật tuyệt 🤗🤗🤗    
Sau khi làm những bước reverse cơ bản thì chúng ta cần chú ý những hàm sau :    

![](/ctf/re/angr/hinh1.PNG)    

![](/ctf/re/angr/hinh2.PNG)    

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

![](/ctf/re/angr/hinh3.PNG)   

Nó dùng ```ptrace``` để thực hiện công việc này. Chúng ta cần bypass hàm này bằng cách thay thế nó bằng một hàm không làm gì cả :)))   

```python
def do_nothing (state) : 
    pass 
p.hook(0x401438, do_nothing, length=262)    # length of target function 
```   


 

