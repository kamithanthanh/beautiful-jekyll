---
layout : post
title : simple login rookiss 
--- 

# Mở đầu 

Mình lại tiếp tục luyện series Rookiss trên [pwnable.kr](https://pwnable.kr/play.php) . Bọn này nó sắp xếp challenge hơi dỏm nên bài này là bài khá dễ mà nó xếp sau brainFuckkk.😢😢😢 Mục tiêu của bài này là control EBP để ret về một địa chỉ chỉ định :v . Các bạn cần biết cơ bản về C và sử dụng thành thạo GDB là một lợi thế , không như heap mấy bài về stack chỉ yêu cầu các kiến thức cơ bản về C thôi 😉😉😉 Mình vẫn chưa có time ngâm cứu mấy bài về heap. 

# Phân tích ban đầu

Trước khi phân tích binary thì thử chạy chương trình và ngâm cứu xem có gì hay ho không 😬😬😬 . Thử một vài giá trị thì nó ra một cái thú vị : 

![hinh5](/Pwnable/pwnable.kr/rookiss/simple%20login/hinh5.PNG) 

Chưa gì đã segmentation fault rồi. Theo kinh nghiệm ban đầu của mình thì mình nghĩ là lại tràn vào địa chỉ trở về gì đó rồi :)) 
Nhưng sau khi debug bằng GDB thì mình phát hiện ra méo phải như vậy .Và mình phát hiện ra là EBP thay đổi thành những giá trị rất lạ lol 😳😳😳 .  
![hinh6](/Pwnable/pwnable.kr/rookiss/simple%20login/hinh6.PNG)  
Lưu ý là EBP sẽ lưu giá trị của ESP cũ .  
Trước khi vào một hàm thì nó thực hiện  :  
```
push  %ebp   
mov   %esp, %ebp     # ebp = esp,  mov  ebp,esp in Intel syntax  
sub   $n, %esp       # allocate space on the stack.  Omit if n=0   
``` 
Khi kết thúc hàm :  
```
mov   %ebp, %esp     # esp = ebp,  mov  esp,ebp in Intel syntax
pop   %ebp
ret
```  
Như vậy là control được cái EBP thì chúng ta có thể control được control flow của cả chương trình . 


