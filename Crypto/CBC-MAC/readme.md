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
 - [**CBC-MAC LENGTH EXTENSION ATTACK**](#type2)  


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

<a name="type2"></a>  
# CBC-MAC Length Extension Attack   

🎆 Scenario :  Khi CBC-MAC được dùng như một loại hash.   

[**Oracle**](/Crypto/CBC-MAC/CBC_mac_length_extension/oracle.py)   

🎁 Đạt được : Chúng ta có thể tạo được hai đoạn message có cùng hash mà nội dung của nó bao gồm những cái ta có thể control được.   

Nhìn lại đoạn giải mã AES-CBC một chút. 
![](https://camo.githubusercontent.com/e2a2004bd559ede641cbe267182ac824884cf738/68747470733a2f2f692e696d6775722e636f6d2f757048616375382e706e67)   

Đầu tiên chúng ta mã hóa M2. Bây giờ tiến hành các bước cần thiết để có thể có được một đoạn message có mã hash như của M2.  
Chúng ta mã hóa một đoạn message M1 bất kì. Sau đó thêm đoạn ghép nối chuyển đổi trạng thái giữa hai đoạn message :  

```
M1 || padd || M2[16:] 
```  

Đoạn padd sẽ có dạng :  

```
padd = xor(xor(CBC-MAC(M1), IV), M2[: 16])  
```  
Tại sao lại xor với CBC-MAC(M1). Vì sau khi mã hóa M1 trong chuỗi string ```M1 || padd || M2[16:]```, chương trình sẽ tiếp tục mã hóa phần padd theo công thức :  

```
E( CBC-MAC(M1) ^ padd)  
-> E(IV ^ M2[: 16])  
```   
Chúng ta thấy bây giờ chương trình mã hóa lại đúng là trạng thái đầu tiên khi mã hóa M2. Vì vậy, kết thúc quá trình này thì chúng ta được cùng một loại mã hóa với M2.   






