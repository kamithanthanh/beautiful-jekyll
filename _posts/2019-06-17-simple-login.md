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
Nhưng sau khi debug bằng GDB thì mình phát hiện ra méo phải như vậy .Và mình phát hiện ra là EBP thay đổi thành những giá trị rất lạ lol 😳😳😳 .  Mình đặt break poit tại ```leave``` của hàm main . 

  
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

# Phân tích binary  
Hàm main cho phép chúng ta nhập 30 kí tự vào biến ```enc``` , sau đó giải mã base64 rồi lưu vào biến ```dec``` với max len cho phép là 12. Sau đó copy giá trị lên biến bss ```input``` . Nếu hash của ```input``` trùng với hash MD5 cho trước thì chúng ta sẽ được xác thực và trở thành root. 

**hàm main**  

![hinh1](/Pwnable/pwnable.kr/rookiss/simple%20login/hinh1.PNG) 

**hàm auth**  

![hinh2](/Pwnable/pwnable.kr/rookiss/simple%20login/hinh2.PNG) 

**hàm correct**  

![hinh3](/Pwnable/pwnable.kr/rookiss/simple%20login/hinh3.PNG)

Chú ý vào hàm auth . MD5 thì không thể break được nên chúng ta sẽ phải tìm cách khác. Trong bước trên chúng ta đã phát hiện ra là EBP đã bị thay đổi ở một bước nào đó, và đó chính là tại hàm auth này. Hàm **auth** thực hiện copy **input** vào biến **v4** 😆😆😆(quên chưa sửa tên mà thôi kệ :)) Cơ mà **v4** lại chỉ được cấp phát 8 bytes bộ nhớ. Mà max len của **input** mà chúng ta được phép là 12 . 4 bytes sẽ tràn vào địa chỉ EBP cũ của hàm **auth** 💥💥💥. Như vậy khi hàm auth thực hiện lệnh **leave** thì EBP sẽ trở thành 4 bytes tràn đó. EBP lúc này là EBP của hàm main do chúng ta không vào được hàm **correct** .  
Chúng ta đã controll được EBP của hàm main . Bước cuối cùng để tiến tới heaven ☝️☝️☝️ là tìm xem heaven ở đâu. Stack là cái ta không thể control .Có một cái chúng ta có thể control đó là  👉  **input** . Lưu ý cuối là nên tìm hiểu kĩ câu lệnh **leave** để khi ret nó ret đúng địa chỉ correct. 

# Kết 

🌟🌟🌟 Tu hành gian nan méo có gái suốt ngày ngồi chơi pwn thế này liệu có ổn không  😔😔😔 
