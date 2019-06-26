---
layout : post 
title : Dubblesort 
subtitle : Pwnable.tw
---

# Mở đầu
Bài này là một bài khá hay . Mình đã củng cố thêm một số kiến thức mới khi làm bài này. Đúng như tên gọi bài này là một bài sắp xếp dãy số nhưng 
có lỗi khiến chúng ta có thể tràn.Điều mà mình học được là cách xác định chính xác hơn địa chỉ của libc.Đồng thời học được một trick nhỏ để vô 
hiệu hóa **scanf** . Cũng như phải làm thế nào trong lúc tuyệt vọng 😱😱😱 

# Phân tích binary  

**Hàm main**  

![hinh4](/Pwnable/pwnable.tw/dubblesort_/hinh4.PNG)  

Hàm này thực hiện các chức năng : 
 - Nhập tên  
 - In tên  
 - Nhập độ dài array  
 - Nhập từng phần tử của mảng  
 - Sắp xếp các phần tử rồi in ra dãy đã sắp xếp  

