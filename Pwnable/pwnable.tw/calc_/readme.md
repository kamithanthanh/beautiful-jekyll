---
layout : post 
title : Calc
subtitle : Pwnable.tw
---  

# Mở đầu
Bài này là một bài kinh điển về minnig . Việc cố gắng tìm ra lỗi tràn có thể giúp bạn rất nhiều trong tương lai.Mình thì mình chỉ đọc wu thôi nhưng vẫn thấy nó magic vãi chưởng 😂😂😂 . Sau khi phát hiện ra lỗi tràn thì bạn có thể ez thực hiện các technique ROP để thực hiện get shell. Ở đây có thêm một kĩ thuật mới là dùng **sys_execve** , không cần phải leak địa chỉ libc.  

# Phân tích binary  
Đầu tiên từ hình này có gợi ra cho bạn ý tưởng gì không ?  

![hinh1](/Pwnable/pwnable.tw/calc_/hinh1.PNG)  

Mình sẽ không phân tích binary cụ thể cách máy tính hoạt động vì nó là một thử thách mà ai cũng phải hoàn thành.Tất cả magic của bài toán 
đều sẽ được giải quyết nếu bạn giải thích được bức ảnh trên 😋😋😋 .  
🌱 ```+361``` có nghĩa là bạn sẽ thay đổi được biến đếm count trỏ tới ô nhớ thứ 361 sau biến count . Tất cả các toán hạng theo sau biểu thức trên sẽ làm việc với ô nhớ thứ 361 . Vậy tại sao lại là con số 361 ???  

![hinh2](/Pwnable/pwnable.tw/calc_/hinh2.PNG)  
  
Nó có thể là địa chỉ trở về của hàm ```calc``` . Ta có canary nằm ở ```$esp + 0x5ac``` còn biến count nằm ở ```$esp + 0x18``` .  
```python 
>>> 0x5ac - 0x18 
1428   
>>> _ / 4  
357  
```
Còn một vài chênh lệch thì bạn có thể mở GDB lên xem cho chính xác  

![hinh3](/Pwnable/pwnable.tw/calc_/hinh3.PNG)  

Đương nhiên bằng vào mã Asm thì ta có thể tính toán chính xác địa chỉ trở về nhưng trong một số trường hợp việc tính toán là khá khó khăn và rắc rối cho nên việc xem bằng GDB là một phương án mang tính khá khả thi và dễ dàng hơn.  😎😎😎 Nhiều lúc dùng GDB sẽ lợi rất nhiều nên tập dùng cho quen là tốt nhất.  

🌾 Công đoạn cuối cùng là thực hiện ROP để get shell . Chương trình này có khá nhiều ROP cho mình dùng. Trong bài này thì mình học được cách dùng [sys_execve](https://stackoverflow.com/questions/9342410/sys-execve-system-call-from-assembly).  
Tóm lại muốn dùng sys_execve thì ta cần phải set các thanh ghi như sau :  
```
  $eax = 11  
  $ebx = binsh_addr  
  $ecx = 0  
  $edx = 0
```  
Chuỗi string ```/bin/sh\x00``` đưa vào chương trình có rất nhiều cách. Bạn có thể dùng ROP để viết lên một địa chỉ có thể ghi nào đó trong bộ nhớ. Mình thì lựa chọn cách ghi ngay sau vùng nhớ stack của địa chỉ trở về , nó ez hơn vì chúng ta có technique tràn rồi mà . Muốn làm điều đó thì chúng ta phải leak được địa chỉ của stack nhưng điều đó được thực hiện cũng khá dễ dàng . ``` +360```. 😀😀😀  
Đến đây mình gặp một cái lỗi hơi ngu người nữa đó là khi mình đưa chuỗi string ```/bin/sh\x00``` vào stack hơi ngu do mình không hiểu rõ cách nó lấy chuỗi như nào. 😑😑😑 Thực ra là mình chưa từng suy nghĩ và mình copy ý tưởng từ lúc bọn nó lấy shellcode là push cái ```/sh\x00``` trước. Cơ mà mình méo hiểu rõ nên nhẫm lẫn lung tung cả. Nhờ một ngươi anh xã hội mà mình lĩnh hội và hiểu rõ được 😛😛😛 

# Kết  
👍👍👍 Ôn lại thế này cảm giác tu vi bình ổn đồng thời nhận ra được mình còn thiếu cái gì, sai ở đâu hoàn thiện bản thân chuẩn bị đột phá lên những le vồ cao hơn. Mình đang định đánh sâu vào mấy bài pwnable.tw sau nhưng muốn tự làm , tự suy nghĩ thì sẽ thu được nhiều cái hơn là đơn giản là đọc writeup . 
