---
layout : post
title : SHA1 Messages Authentication Code 
--- 

Là một hệ thống xác thực người dùng hoạt động trên loại mã hash. Giả sử người cung cấp sản phẩm A và người sử dụng B cùng chia sẻ một khóa KEY. A phát hành văn bản A kèm theo chữ ký, B có thể dùng khóa bí mật để xác thực được văn bản có bị sửa đổi hay không. Việc kí hoạt động trên nguyên tắc :  
  - Chữ kí : SHA1(KEY + message)  

Cách tấn công khả dĩ nhất trong trường hợp này là Length extension attack.  
Chúng ta có thể dựa trên đầu vào là một đoạn văn bản đã được kí, từ đoạn văn bản cũ, ta có thể thêm vào đằng sau văn bản này một đoạn văn bản mới tùy chọn, đồng thời sinh ra chữ ký mới cho đoạn văn bản này.   

Đây chính là challenge 29 trong cryptopal. Mình đã viết code thực thi, do nó khá phức tạp, liên quan nhiều tới thuật toán mã hóa của SHA-1 nên mình cũng lười làm lại. Có script rồi thì trong tình huống cụ thể có thể dùng được script luôn thôi.   

[**Script**](/Crypto/hash/SHA1_MAC/length_extension_attack.py)  
