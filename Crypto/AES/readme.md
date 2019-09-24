---
layout : post 
title : Block cipher 
--- 

# Mở đầu  
Block cipher là kiểu mã hóa khối. Hiện nay AES là loại mã khối tiêu chuẩn và hay được dùng nhất. AES được coi là không thể bị bẻ khóa. Đây cũng là một dạng quen thuộc trong các kì thi CTF. Tùy vào từng tác giả sẽ có những tùy biến khác nhau nhưng có một số lỗi cơ bản mà chúng ta cần nắm được. Vì các kiểu tùy biến thì hầu như cũng dựa trên nền những kiểu tấn công cổ điển này.  
Về tài liệu tham khảo thì có thể tham khảo trên :  
  - [**Crypto101**](https://www.crypto101.io/)    
  - [**Cryptopal Set2**](https://cryptopals.com/sets/2)   

Không cần đi sâu hiểu được cách hoạt động của AES. Vì nó rất khó lại ít bị khai thác lỗi. Tập trung hiểu được cách hoạt động của các dạng mã hóa như ECB, CBC, CRT, ...  
Well documented [here](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation).  

😁😁😁 Ôn luyện lại đồng thời lưu lại script để dùng sau .  

# Table Of Content  
  - [**Byte-at-a-time ECB decryption**](#type1)  


<a name="type1"></a> 
# Byte-at-a-time ECB decryption  

Chúng ta sẽ có một oracle để encrypt bất kì đoạn message nào nhưng được thêm vào những kí tự cố định ở đầu và cuối mỗi lần mã hóa. Nôm na là nó sẽ có dạng : 
```
AES-ECB(prefix || attacker-controlled || suffix, random-key)
``` 
Mục tiêu của chúng ta là tìm được ```suffix```. Nếu trong một kì thi CTF thì người ta có thể đặt flag ở đây.  

### Step 1 : find prefix length  
Do đây là kiểu mã hóa ECB nên nếu cùng một input thì sẽ cho ra cùng một kết quả.  
Idea là so sánh block thứ hai của 2 đoạn message sau :
```
 - "0" * i + "1" + "0" * length 
 - "0" * i + "0" + "0" * length 
```   
Tăng dần i lên cho tới khi nào hai block sau khác biệt. Sự khác biệt là do ```prefix + "0"*i``` phủ đầy một block đẩy ```1``` sang block tiếp theo. Từ đây chúng ta có thể tình được prefix length.  

### Step 2 : get suffix  
Chúng ta tiến hành recovery lần lượt từng bytes của suffix.  
Đầu tiên tiến hành mã hóa message  :  
```python
"a" * (block_size - len_prefix) + "a" * (block_size - 1)
```
Tại block thứ hai, chúng ta thu được mã hóa của ```"a"*(block_size-1) + suffix[0]``` (1). Lúc này tiến hành brute force kí tự đầu tiên của suffix bằng cách mã hóa : 
```python
"a" * (block_size - len_prefix) + "a" * (block_size - 1) + chr(char_brute)
```  
Bruteforce tới khi nào thu được đoạn mã giống như (1) thì dừng.Ta thu được character đầu tiên của suffix.  
Tiếp tục làm như vậy ta thu được suffix.  
👉 [Script](/Crypto/AES/byte_at_time.py) 👈  








