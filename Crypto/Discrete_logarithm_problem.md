---
layout : post 
title : Discrete Logarithm Problem (DLP)  
--- 

# Mở đầu  

Discrete Logarithm Problem(DLP) là việc đi tìm x sao cho : ```a ^ x = b (mod n)```   

**Alert** : Bài viết này không mang tính chất học thuật mà mang đậm tính chất của một script kiddie. Học và hiểu cách làm thông qua một số bài CTF, biết các script và cách xử lí cho từng bài. Nếu bạn nào có hứng thú thì sau có thể tìm hiểu thêm. Không gì nhanh bằng việc học qua các bài CTF. 😂😂😂  Mình sẽ lấy ví dụ là một bài CTF đơn giản để minh họa. Sad là có khá ít bài toán liên quan tới DLP mình tìm thấy trên CTFtime. Mấy bài còn lại liên quan nhiều đến ECC nên cũng không tiện viết ở đây.  

# [RitSec2018 DarkpearAI](https://github.com/aadityapurani/My-CTF-Solutions/tree/master/ritsec-2018/DarkpearAI)  

Đề bài cho một loại mã hóa là [**Diffie Hellman**](https://vi.wikipedia.org/wiki/Trao_%C4%91%E1%BB%95i_kh%C3%B3a_Diffie-Hellman) cùng với publickey và ciphertext.  

```python
n = 371781196966866977144706219746579136461491261
g = 3

m1 = 97112112108101112101097114098108117101
m2 = 100097114107104111114115101097105
``` 
m1, m2 là hai khóa công khai tương ứng với A, B trong bài viết. Công việc của chúng ta là đi tìm key bí mật để có thể decrypt được ciphertext. 😀😀😀 Mà việc tìm khóa bí mật chính là đi giải bài toán DLP.   

## Cách 1 : Tools online  
Đối với việc giải bài toán này thì phương án đầu tiên được đưa ra tất nhiên là dùng các tool online 😆😆😆. Script kiddie mà . Cứ google search và bùm 😅😅😅 Có flag thôi.  
Tool : [**alpertron**](https://www.alpertron.com.ar/DILOG.HTM)  
Thằng này có khá là nhiều tools hữu ích khác nhau, các bạn có thể nghiên cứu thêm.  
Sau khi tìm được khóa bí mật thì việc còn lại khá là dễ dàng.  


## Cách 2 : Sage  

Hoặc nếu thích viết script thì có thể dùng ```Sage``` ✨✨✨. Một công cụ tích hợp của python và một số hàm thư viện viết sẵn chuyên để xử lí những vấn đề số học phức tạp. Chẳng hạn như bài này, ta có thể dùng hàm ```discrete_log``` để giải DLP. Mình cũng chả biết nó có thể solve cho những trường hợp nào nhưng cũng là một phương án đáng để thử.  

Thiết lập script như sau :  

```python 
F = IntegerModRing(n)             
a = discrete_log(F(m1), F(g))
```

Khi hàm này được gọi, Sage tự động thực hiện các thuật toán như ```Pohlig Hellman```, ```Baby Step - Giant Step``` để giải bài toán DLP. Có thể tham khảo thêm cách viết script ở [đây](http://sage.math.canterbury.ac.nz/home/pub/337/).  
 - BSGS thường được dùng để giải bài toán Diffie Hellman trong trường hợp modules là số nguyên tố.  
 - Trong trường hợp modules không là số nguyên tố thì Pohlig Hellman là lựa chọn tốt hơn.  

Độ phức tạp của Pohlig Hellman trong trường hợp tệ nhất là  ![](https://latex.codecogs.com/gif.latex?O(\sqrt{n})) .   
Nhưng trong trường hợp tốt nhất thì là :  
              ![](https://wikimedia.org/api/rest_v1/media/math/render/svg/1659cc7510a39c976a64afaafe64f953214e1e7a)  

Như vậy ta có thể thấy được hai phương pháp này thích hợp cho những số nhỏ. Sage còn hỗ trợ nhiều cách giải khác nhau của bài toán DLP trong các trường hợp khác nhau được miêu ta chi tiết ở [đây](http://doc.sagemath.org/html/en/reference/groups/sage/groups/generic.html)  
 - **discrete_log_lamda** : Phương pháp này dùng cho trường hợp chúng ta có một vùng giới hạn của x.  
 - **discrete_log_rho** : Dùng cho module lớn hơn nhưng chỉ được phép là số nguyên tố. Nếu module khá nhỏ thì nó trở về BSGS.  
 





