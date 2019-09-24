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
  - [**CBC Bit flipping attack**](#type2)  
  - [**CBC KEY as IV**](#type3)  
  - [**CBC Padding Oracle**](#type4)  
  
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

<a name="type2"></a> 

# CBC Bit Flipping Attack  

Giả sử Alice có một oracle encrypt và trả về ciphertext. Alice sẽ đưa ciphertext cho Bob để xác nhận xem Alice có phải admin không. Oracle lại không cho encrypt bất kì đoạn message nào có chứa chữ ```admin```. Mục tiêu của chúng ta là sửa một số byte trong cipher text để thu được plaintext có chứa ```admin```.  
Mình có viết một cái [**Oracle**](https://github.com/hacmao/hacmao.github.io/tree/master/Crypto/AES/Bit_flipping) để minh họa.  
Tất cả idea của cách tấn công này được miêu tả thông qua sơ đồ sau :  

![](https://mk0resourcesinfm536w.kinstacdn.com/wp-content/uploads/082113_1459_CBCByteFlip3.jpg)   

Trong mode CBC bước decrypt, để thu được plaintext thì ta lấy blockcipher trước xor với block được decrypt trong lần hiện tại. Do đây là phép xor nên nếu ta thay đổi một số bit trong blockcipher_prev thì ở vị trí tương ứng trong plaintext cũng thay đổi.  
Có nghĩa là giả sử ta có ciphertext của một plaintext mà chữ cái ta muốn thay đổi là "A" thành "a". Ta cần thay đổi trong blockcipher trước đó (Nếu là blockđầu tiên thì thay đổi IV) theo công thức :   

```python
c[i] = chr(ord(c[i]) ^ ord("a") ^ ord("A"))
```

Khi đó plaintext sẽ trở thành :  

```python
p[i] = p[i] ^ ord("a") ^ ord("A") 
p[i] = ord("a") ^ ord("a") ^ ord("A") 
p[i] = ord("a") 
``` 

<a name="type3"></a> 
# CBC KEY as IV  
 
Trong nhiều hệ thống thời xưa khi triển khai mã hóa bằng AES.MODE_CBC thường lấy key = IV. Vì IV luôn random nên việc lấy như vậy được coi như là secure. Vừa đỡ tốn thời gian generate key, dễ setup. 😁😁😁 Nhưng có một thanh niên nào đó không nghĩ vậy và đã tìm ra được cách attack vào những hệ thống như vậy.   

🎆🎆🎆 Tình huống giả định trong trường hợp này là : Alice và Bob trao đổi thư điện tử cho nhau sử dụng hệ thống mã hóa như trên. Khi đó Malory thực hiện cuộc tấn công MITM (Man-In-the-middle attack) và kiểm soát được những dữ liệu ciphertext mã hóa tin nhắn của Alice gửi cho Bob. Và thay bằng malicious ciphertext. Sau khi Bob giải mã giữ liệu thì từ những dữ liệu đó, Malory sẽ tiến hành tính toán và recovery lại được KEY.   

🐙🐙🐙 [**Oracle**](https://github.com/hacmao/hacmao.github.io/tree/master/Crypto/AES/key_as_IV)  

Ok chi tiết hơn. Giả sử Alice -> Bob : P1P2P3..... được mã hóa thành C1C2C3....  
Malory sau đó sẽ can thiệp và gửi lại cho Bob đoạn mã hóa : C1ZC1 , trong đó Z là một block các kí tự NULL.  
Sau khi giải mã thì plaintext mới sẽ là :  
```
 - P1` = D(k, C1) ^ IV = P1 
 - P2` = D(k, Z) ^ C1 = R    # một giá trị ngẫu nhiên nào đó
 - P3` = D(k, C1) ^ Z = D(k, C1) 
``` 
Khi đó, k = P1' ^ P3'.   🌝🌝🌝 Get key.  


<a name="type4"></a>  
# CBC Padding Oracle Attack  
Kiểu tấn công này có phức tạp hơn các kiểu tấn công trước một chút.  

🎏🎏🎏 [**Oracle**](https://github.com/hacmao/hacmao.github.io/tree/master/Crypto/AES/padding_oracle)  
 
🎆🎆🎆 Tình huống : Giả sử chúng ta đang sử dụng hệ thống mã hóa AES CBC có sử dụng kiểu padding PKCS7. Có một Oracle check padding có valid hay không, trả về True and False. Từ Oracle này chúng ta có thể thực hiện tấn công và recovery lại được plaintext.  

Padding PKCS7 có dạng sau :  

```python
def pad(s) : 
    c = 16 - len(s) % 16 
    return s + c * chr(c) 
``` 
Hàm check padding có dạng :  

```python
def padding_oracle(c) : 
    m = decrypt(c) 
    LB = ord(m[-1])   
    return m[-LB :] == chr(LB) * LB
``` 

### Step 1 : create fake valid padding  

![](Crypto/AES/padding_oracle/hinh1.PNG)  

Giả sử target của chúng ta là block Ci. Chúng ta thực hiện check valid padding của đoạn cipher ```R + Ci```. Trong đó R là một block ngẫu nhiên. Chúng ta sẽ thay đổi byte cuối cùng của R cho tới khi đạt được valid padding.Do CBC là phép xor nên khi thay đổi byte như vậy ta luôn được valid padding (vì luôn qua giá trị ```\x01```).  
Tuy nhiên đôi khi chúng ta gặp phải trường hợp valid padding lại có dạng ```\x02\x02``` hoặc ```\x03\x03\x03```. Những trường hợp như vậy rất hiếm nhưng không phải không có khả năng. Ta có thể loại bỏ nó bằng cách thay đổi byte thứ hai từ cuối lên của R. Nếu nó vần là valid padding thì valid padding sẽ là ```\x01```.  
Nếu không là valid padding, trong trường hợp này mình tiếp tục lựa chọn bruteforce tiếp byte cuối của R cho tới khi tìm được valid padding là ```\x01```. Để code nó gọn hơn đỡ lằng nhằng. 👌👌👌 Đương nhiên hoàn toàn có thể xác định được padding là gì nhưng do lười nên mình thường làm những việc đơn giản hơn.  

### Step 2 : Recovery last bytes   

Sau khi có được valid padding là ```\x01```. Ta có thể recovery lại last bytes của plaintext tại block tương ứng.   
Thật vậy, ta có :  
```
D(k, Ci[-1]) ^ R[-1] = 1 
-> D(k, C[-1]) = 1 ^ R[-1] 
``` 
Khi tìm được D(k, C[-1]) theo công thức trên thì ta hoàn toàn có thể tìm được m[-1].  

### Step 3 : Recovery remaining block   
Tiếp theo, ta thay đổi R : ```R[-1] = R[-1] ^ 1 ^ 2```. Như vậy, hiện tại padding sẽ là ```\x02```.   
Ta lại tiếp tục bruteforce R[-2] cho tới khi đạt được valid padding là : ```\x02\x02```.Khi đó :   
```
D(k, Ci[-2]) ^ R[-2] = 2 
-> D(k, Ci[-2] = R[-2] ^ 2 
```  
Tiếp tục ta lại recovery được m[-2].  
Tương tự ta recovery được hết block.  





