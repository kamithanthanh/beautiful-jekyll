---
layout : post 
title : Calc
subtitle : Pwnable.tw
---  

# Mở đầu
Bài này là một bài kinh điển về minnig . Việc cố gắng tìm ra lỗi tràn có thể giúp bạn rất nhiều trong tương lai.Mình thì mình chỉ đọc wu thôi nhưng
vẫn thấy nó magic vãi chưởng 😂😂😂 . Sau khi phát hiện ra lỗi tràn thì bạn có thể ez thực hiện các technique ROP để thực hiện get shell. Ở
đây có thêm một kĩ thuật mới là dùng **sys_execve** , không cần phải leak địa chỉ libc.  

# Phân tích binary  
Đầu tiên từ hình này có gợi ra cho bạn ý tưởng gì không ?  

![hinh1](/Pwnable/pwnable.tw/calc_/hinh1.PNG)  

Mình sẽ không phân tích binary cụ thể cách máy tính hoạt động vì nó là một thử thách mà ai cũng phải hoàn thành.Tất cả magic của bài toán 
đều sẽ được giải quyết nếu bạn giải thích được bức ảnh trên 😋😋😋 .  
🌱 ```+360``` có nghĩa là bạn sẽ thay đổi được biến đếm count trỏ tới ô nhớ thứ 360 sau biến count . Tất cả các toán hạng theo sau biểu thức
