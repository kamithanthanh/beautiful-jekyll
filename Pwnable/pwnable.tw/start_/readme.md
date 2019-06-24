---
layout : post
title : Start  
subtitle : Pwnable.tw 

--- 

# Mở đầu
Đây là bài đầu tiên trong chuỗi bài của Pwnable.tw. Bài yêu cầu những kĩ thuật cơ bản về tràn và kĩ thuật cơ bản về shellcode.  

# Phân tích binary  

Binary của challenge này chỉ là một chương trình assembly đơn giản  

![hinh1](/Pwnable/pwnable.tw/start_/hinh1.PNG)  

Ta thấy hàm này có hai chức năng chính là **write** và **read** .Hàm **write** in ra kí tự ```Let's start the CTF:``` còn hàm **read** cho phép 
chúng ta tràn 40 kí tự. 😀😀😀 Đây là một bài cơ bản về tràn. Có điều do chỉ là chương trình asm cơ bản nên không sử dụng các thư viện ngoài 
của libc vì vậy không thể sử dụng hàm ```system```.  
Dùng ```checksec``` thì ta thấy NX disabled.  

![hinh2](/Pwnable/pwnable.tw/start_/hinh2.PNG)  

Khi NX bị disabled thì ta có thể sử dụng shellcode. Nhưng khi dùng shellcode ta cần quan tâm đến hai vấn đề  : 
 - Đặt ở đâu ? 👈  
 - Chạy thế nào? 👈  

Shellcode của chúng ta sẽ đặt ở ngay sau địa chỉ trở về của chương trình này và chạy bằng cách ```ret``` về stack .  
🌼 Nhiệm vụ 1 có thể dễ dàng thực hiện được. Đối với nhiệm vụ hai chúng ta cần leak địa chỉ của stack.  

![hinh3](/Pwnable/pwnable.tw/start_/hinh3.PNG)  

Địa chỉ stack được lưu ngay sau địa chỉ trở về của hàm main. Chúng ta có thể leak địa chỉ stack bằng cách tràn vào địa chỉ trở về bằng địa chỉ 
```0x08048087``` . Đó là địa chỉ bên trong hàm main cho phép chúng ta in ra 20 giá trị tính từ đỉnh ngăn xếp, trong đó có ESP. Đồng thời chúng 
ta có quyền nhập dữ liệu một lần nữa.  
☀️ Trong lần nhập liệu thứ hai, khi đã biết địa chỉ của stack thì chúng ta có thể tính toán ra địa chỉ của shellcode mà chúng ta muốn đặt rồi 
hoàn tất các nhiệm vụ là xong.  
# Kết  
Qua mỗi bài là có một vài kĩ năng có thể rèn luyện , chơi CTF không chỉ là hoàn thành challenge mà là những gì chúng ta thu được sau khi 
hoàn thành challenge đó là gì ??? 
