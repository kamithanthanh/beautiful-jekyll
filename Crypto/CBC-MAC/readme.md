---
layout : post 
title : CBC Messages Authenticate Code 
--- 

# How it works  

Một hệ thống xác thực người dùng bằng CBC-MAC hoạt động theo nguyên tắc sau.
Giả sử A, B là hai bên cần trao đổi thông tin. A, B cùng chia sẻ một KEY bí mật chung. Để bảo đảm đoạn message trao đổi không bị sửa đổi trong quá trình vận chuyển, A tiến hành kí message theo các bước :  
 - Mã hóa messages của người dùng bằng AES CBC bằng KEY bí mật.  
 - Chữ kí là block cuối cùng của đoạn mã hóa.  
 - Trả về message + iv + sign.   


Để xác nhận là cùng một người kí, đoạn message không bị sửa đổi thì phía bên B sau khi nhận được message sẽ tiến hành kí lại rồi so sánh với chữ kí của bên A. Nếu giống thì văn bản toàn vẹn.   

   

# Type 0f Attack  
 - [**CBC-MAC Forgery**](#type1)  

<a name="type1"></a>  
# CBC-MAC Forgery  
🎆 Scenario : Chúng ta nhận được chữ kí của đoạn message nào đó.  

[**Oracle**](https://github.com/hacmao/hacmao.github.io/blob/master/Crypto/CBC-MAC/CBC_mac_forgery/oracle.py)   

🎁 Đạt được : Thay đổi được 16 kí tự đầu của message.   

Vì chúng ta có quyền kiểm soát được iv, nên chúng ta có thể tiến hành CBC bit flipping-attack ở đây.   
Cụ thể IV sẽ bị thay đổi thành :   

```python
IV_forged = xor(msg[:16], xor(forged_msg[:16], iv))   
```  

Nguyên lí hoạt động tương tự như bit flipping attack. Sau đó văn bản đã kí sẽ trở thành :   

```
forged_msg + IV_forged + mac 
```  


