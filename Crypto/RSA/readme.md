---
layout : post 
title : RSA - loại mã cổ xưa nhất  
---  

Nếu nhắc đến loại mã nào được nhắc tới nhiều nhất thì đó chính là RSA. Trong các loại mã này thì mình cũng thích loại mã này nhất vì nó khá là gần gũi với kiến thức số học thuần túy. Nó đẹp tự nhiên, đậm chất tư duy logic mà một kẻ gà mờ về toán như mình cũng có thể hiểu được.    

![](/img/meo28.jpg)    

Do tài liệu về RSA cũng khá là phong phú rồi nên mình cũng chỉ liệt kê lại các kiểu tấn công có thể có, tình huống sử dụng là khi nào để khi gặp còn biết mà tìm script về mà chạy. 😁😁😁   

# Factor modules  
Cách tiếp cận ban đầu khi tới một bài RSA là đi phân tích modules ra thừa số nguyên tố để tìm được private key. Từ đó dễ dàng decode được message. Thông thường cách làm này chỉ dành cho những bài cho mỗi publickey mà không cho thêm thông tin gì cả.   

Chúng ta có thể lần lượt thử các tools như :   
 - [**factordb**](http://factordb.com/)   
 - [**alpertron**](https://www.alpertron.com.ar/ECM.HTM)  
 - [**RsaCtftools**](https://github.com/Ganapati/RsaCtfTool)   

Nếu thử hết tools trên mà còn không factor được modules này thì con đường factor sẽ không thể theo script kiddie được rồi.  
Chúng ta có thể dựa vào một số giấu hiệu trong code để tìm được cách factor n. Cái này thì nó đa dạng lắm nên là cũng không thể liệt kê hết được. Nhưng có một số phương pháp tiêu biểu  :  
  - **GCD** : tìm hai số có chung ước nguyên tố.  
  - **Fecmat** : khi hai ước nguyên tố của modules khá gần nhau.  

# Blinding   

🎆🎆🎆 Chúng ta có một oracle có thể decrypt mọi thứ trừ ciphertext được cho.  

Solution : Send ```2**e * C```. Ta sẽ thu được ```2*P```. Chỉ cần chia cho 2 là ta được plaintext.   

# Low private exponent   

🎆🎆🎆 Khi e quá lớn thì d có thể rất bé.   

💰💰💰 Solution : Weiner Attack. Cũng có trong RsaCtftools.   
Khi d to hơn một tí so với giới hạn của weiner attack thì chúng ta có thể sử dụng thuật toán [**boneh_durfee**](https://github.com/Ganapati/RsaCtfTool/blob/master/boneh_durfee.sage) để attack.  


# Coopersmith Attack    

🎆🎆🎆 Situation : Khi ta có thông tin về messages và chỉ cần recovery lại một phần nhỏ của message.  

Khi đó messages sẽ có dạng : ```M + x``` trong đó M là cái đã biết, x là cái cần tìm.   
Khi đó ta xây dựng hàm f(x) :  
```
f(x) = (M + x) ^ e - C 
```  
Và giải phương trình trên module n :  ```f(x) = 0```.   
Trên mạng có rất nhiều script về cái này, mình cũng có lưu một cái. [**đây**](/Crypto/RSA/coopersmith.py)   
Hoặc đơn giản hơn là dùng script trong sage như sau :   

![](https://kamithanthanhhome.files.wordpress.com/2019/01/image-3.png)   


#  Hastad's Broadcast Attack   

🎆🎆🎆 Situation : Một messages có thể mã hóa nhiều lần bằng các public key khác nhau.  

Khi đó chúng ta có thể tiến hành mã hóa nhiều lần, thu được cipher text rồi dùng Chinese remainder theorem để tìm được :  

```
m^e = C (mod N1 * N2 * ... * Nr)  
```  
Sau đó khi m^e < N1 * N2 * ... * Nr thì ta tính iroot(m,e) là xong.   

# Franklin-Reiter Related Message Attack   

🎆🎆🎆 Situation : Khi hai message có mối liên hệ với nhau thì ta có thể dùng kiểu tấn công này.   

🌊 Kiểu tấn công đơn giản đầu tiên của Franklin-Reiter là khi biết được khoảng cách giữa hai messages.  
Khi đó ta chỉ cần tính gcd hai hàm :  
```
f = x ^ e - C1  
g = (x + r) ^ e - C2   
```
f,g đều có nghiệm là M nên là khi tìm được gcd sẽ là x - M.  

🌊 Kiểu tấn công thứ hai là khi không rõ khoảng cách giữa hai messages là bao nhiêu. Chỉ cần nó không quá xa nhau thì ta hoàn toàn có thể recovery lại khoảng cách đó rồi thực hiện tiếp theo kiểu tấn công trên.   

[**script**](/Crypto/RSA/franklinReiter.py)   

# Least Significant Bits Oracle Attack  
🎆🎆🎆 Situation : Khi ta có một oracle decrypt trả về bit cuối cùng của plaintext.  

Kiểu tấn công này được trình bày khá kĩ ở [đây](https://crypto.stackexchange.com/questions/11053/rsa-least-significant-bit-oracle-attack)   

# Partial Private Key  
🎆🎆🎆 Situation : Khi chúng ta biết được một phần của private key.  

Well Documented [here](https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf).  

# Partial p  

🎆🎆🎆 Situation : Khi biết được một phần của private key.   

Kiểu tấn công này có thể được thấy qua kì CTF [này](https://github.com/p4-team/ctf/tree/master/2017-09-02-tokyo/crypto_rsa).  
# Some repositories  

 - [**ashutosh**](https://github.com/ashutosh1206/Crypton/tree/master/RSA-encryption)   
 - [**ValarDragon**](https://github.com/ValarDragon/CTF-Crypto/tree/master/RSA)   
 - [**RsaCtfTools**](https://github.com/Ganapati/RsaCtfTool)  
