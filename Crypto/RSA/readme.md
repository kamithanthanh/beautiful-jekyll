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





