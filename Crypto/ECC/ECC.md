---
layout :  post 
title : Attack on ECC 
---  
Giả định ta có đường cong Elliptic (E) trên trường số nguyên tố p :  

![](https://latex.codecogs.com/gif.latex?y^{2}&space;=&space;x^{3}&space;&plus;&space;Ax&plus;b) 

Đối với các bài toán về ECC thì thông thường chúng ta cần đi giải bài toán ECDLP :   

![](https://latex.codecogs.com/gif.latex?Q=nP)  

# Table Of Contents  
 - [**Attack on Curve singular**](#type1) 
 - [**Smart ASS Attack**](#type2)
 - [**Pohlig-Hellman attack**](#type3)  
 - [**No Correctness Check for Input Points**](#type4)   

<a name="type1"></a>  
# 1. Attack on Curve singular  
Có một cách thú vị để phát hiện curve có là singular hay không ? 😀😀😀 Đó là khai báo trong sage bằng funtion ```EllipticCurve```. Quy ước là curve thì sẽ không được có singular point (P/s : vì nó không secure).  
Đối với những loại curve singular này thì có một cách tiếp cận để giải được bài toán ECDLP mình đã trình bày ở [**đây**](https://hacmao.pw/Crypto/ECC/ECDLP_singular/)   

<a name="type2"></a>  
# 2. Smart ASS Attack   

Kiểu attack này thực hiện được khi có điều kiện : ```P.order() == p``` . Khi đó chúng ta có thể giải bài toán ECDLP trong thời gian tuyến tính.    
[**Script**](https://github.com/hacmao/hacmao.github.io/blob/master/Crypto/ECC/ECDLP_script/smart_ASS_attack.py) này mình đã lưu lại dùng đễ attack kiểu tấn công này.   
Nếu bạn muốn tìm hiểu sâu hơn thì có thể đọc [**document**](https://hpl.hp.com/techreports/97/HPL-97-128.pdf) này để biết thêm chi tiết.  
**Practice** : [**Sharift 2016**](https://hxp.io/blog/25/SharifCTF%202016:%20crypto350%20%22British%20Elevator%22%20writeup/)  

<a name="type3"></a>  
# 3. Pohlig-Hellman attack     

Kiểu tấn công này được well-defined trong [**tài liệu**](https://koclab.cs.ucsb.edu/teaching/ecc/project/2015Projects/Sommerseth+Hoeiland.pdf) này.  
Kiểu tấn công này thực hiện được khi ```P.order()``` có thể phân tích thành các số nguyên tố nhỏ hoặc là ta có bound của n.  

Giả sử chúng ta có thể phân tích được ```P.order()``` thành các số nguyên tố :  

![](https://latex.codecogs.com/gif.latex?P.order()&space;=&space;p_{1}^{e_{1}}.p_{2}^{e_{2}}...p_{r}^{e_{r}})   

Ý tưởng của Pollig-Hellman là làm việc với các số nguyên tố bé, sau đó dùng CRT để tìm được n.   
Ok trước hết tìm ```x = n (mod p1^e1)```. Ta thực hiện theo các biến đổi sau :   

```python
k = P.order() 
P0 = P * (k // (p1^e1)) 
Q0 = Q * (k // (p1^e1)) 
x = discrete_log_lamda(Q0, P0, (0, p1^e1), '+')    
```   

Trong sage, hàm ```discrete_log_lamda``` được dùng để giải bài toán DLP trong một khoảng giới hạn nào đó. Qua các phép biến đổi kia, ta đã giới hạn được x trong module p1^e1. Vì vậy sử dụng hàm này trong trường hợp này là vô cùng thích hợp, giúp giảm thời gian tìm kiếm đi rất nhiều.    

🐣🐣🐣 Một điểm đặc biệt nữa là khi ta có vùng bound của n (n < N) thì sau khi tìm được số dư của n cho một số số nguyên tố nào đó, ta có thể tiến hành bruteforce theo module đó để tìm ra được n.  

Toàn bộ ý tưởng này là mình học được từ bài CTF dưới đây. Hãy thử làm và kiểm nghiệm độ hiệu quả 😀😀😀   

**Pratice** : [**UCTF**](https://aadityapurani.com/2019/03/11/utctf-2019-writeups/#alice)   

<a name="type4"></a>   
# 4. No Correctness Check for Input Points   
🎏🎏🎏 Situation : Trong trường hợp chúng ta có một oracle cho ta nhập một điểm P' và trả về Q' = nP' mà không check xem điểm P' có thuộc đường cong (E) hay không.  

🎇🎇🎇 Solutions : Input các điểm thuộc các đường cong khác. Rồi dùng phương pháp Pollig-Hellman để tìm đồng dư của n theo một module nào đó. Làm nhiều lần như vậy rồi dùng CRT để tìm ra n.  

Kiểu tấn công này được document trong [**tài liệu**](https://www.iacr.org/archive/crypto2000/18800131/18800131.pdf) này. Và được minh họa trong kì thi CTF bên dưới.  

**Practice** :  [**Spam the flags**](https://github.com/p4-team/ctf/tree/master/2019-04-07-spam-and-flags-teaser/crypto_ecc)   


