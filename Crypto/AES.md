---
layout : post 
title : Block cipher 
--- 

# Mở đầu  
Block cipher là kiểu mã hóa khối. Hiện nay AES là loại mã khối tiêu chuẩn và hay được dùng nhất. AES được coi là không thể bị bẻ khóa. Đây cũng là một dạng quen thuộc trong các kì thi CTF. Tùy vào từng tác giả sẽ có những tùy biến khác nhau nhưng có một số lỗi cơ bản mà chúng ta cần nắm được. Vì các kiểu tùy biến thì hầu như cũng dựa trên nền những kiểu tấn công cổ điển này.  
Về tài liệu tham khảo thì có thể tham khảo trên :  
  - [**Crypto101**](file:///D:/ctf/Crypto/pdf/Crypto101.pdf)  
  - [**Cryptopal Set2**](https://cryptopals.com/sets/2)  

😁😁😁 Ôn luyện lại đồng thời lưu lại script để dùng sau .  

# Table Of Content  
  - [**Byte-at-a-time ECB decryption**](#type1)  


<a name="type1"></a> 
# Byte-at-a-time ECB decryption (Harder)  
