---
layout : post 
title : Discrete Logarithm Problem (DLP)  
--- 

# Mở đầu  
Alert : Bài viết này không mang tính chất học thuật mà mang đậm tính chất của một script kiddie. Học và hiểu cách làm thông qua một số bài CTF, biết các script và cách xử lí cho từng bài. Nếu bạn nào có hứng thú thì sau có thể tìm hiểu thêm. Không gì nhanh bằng việc học qua các bài CTF. 😂😂😂  

# Table Of Content  
 - [RitSec2018 DarkpearAI](#wu1) 

<a name="wu1">
</a>

# [RitSec2018 DarkpearAI](https://github.com/aadityapurani/My-CTF-Solutions/tree/master/ritsec-2018/DarkpearAI)  

Đề bài cho một loại mã hóa là [**Diffie Hellman**](https://vi.wikipedia.org/wiki/Trao_%C4%91%E1%BB%95i_kh%C3%B3a_Diffie-Hellman) cùng với publickey và ciphertext.  

```python
n=371781196966866977144706219746579136461491261
g=3

m1 = 97112112108101112101097114098108117101
m2 = 100097114107104111114115101097105
``` 
m1, m2 là hai khóa công khai tương ứng với A, B trong bài viết. Công việc của chúng ta là đi tìm key bí mật để có thể decrypt được ciphertext. 😀😀😀 Mà việc tìm khóa bí mật chính là đi giải bài toán DLP.   
Đối với việc giải bài toán này thì phương án đầu tiên được đưa ra tất nhiên là dùng các tool online 😆😆😆. Script kiddie mà . Cứ google search và bùm 😅😅😅 Có flag thôi.  
Tool : [**alpertron**](https://www.alpertron.com.ar/DILOG.HTM)  
Thằng này có khá là nhiều tools hữu ích khác nhau, các bạn có thể nghiên cứu thêm.  
Sau khi tìm được khóa bí mật thì việc còn lại khá là dễ dàng.  

Hoặc nếu thích viết script thì có thể dùng ```Sage``` ✨✨✨. Một công cụ tích hợp của python và một số hàm thư viện viết sẵn chuyên để xử lí những vấn đề số học phức tạp. Chẳng hạn như bài này, ta có thể dùng hàm ```discrete_log``` để giải DLP. Mình cũng chả biết nó có thể solve cho những trường hợp nào nhưng cũng là một phương án đáng để thử.  

Thiết lập script như sau :  

```python 
F = IntegerModRing(n)             
a = discrete_log(F(m1), F(g))
```





