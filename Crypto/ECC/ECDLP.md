---
layout :  post 
title : Attack on ECDLP 
---  
Giả định ta có đường cong Elliptic (E) trên trường số nguyên tố p :  

![](https://latex.codecogs.com/gif.latex?y^{2}&space;=&space;x^{3}&space;&plus;&space;Ax&plus;b) 

Chúng ta cần đi giải bài toán ECDLP :   

![](https://latex.codecogs.com/gif.latex?Q=nP)  


# 1. Attack on Curve singular  
Có một cách thú vị để phát hiện curve có là singular hay không ? 😀😀😀 Đó là khai báo trong sage bằng funtion ```EllipticCurve```. Quy ước là curve thì sẽ không được có singular point (P/s : vì nó không secure).  
Đối với những loại curve singular này thì có một cách tiếp cận để giải được bài toán ECDLP mình đã trình bày ở [**đây**](https://hacmao.pw/Crypto/ECC/ECDLP_singular/)   

# 2. Smart ASS Attack   

Kiểu attack này thực hiện được khi có điều kiện : ```P.order() == p``` . Khi đó chúng ta có thể giải bài toán ECDLP trong thời gian tuyến tính.    
[**Script**](https://github.com/hacmao/hacmao.github.io/blob/master/Crypto/ECC/ECDLP_script/smart_ASS_attack.py) này mình đã lưu lại dùng đễ attack kiểu tấn công này.   
Nếu bạn muốn tìm hiểu sâu hơn thì có thể đọc [**document**](https://hpl.hp.com/techreports/97/HPL-97-128.pdf) này để biết thêm chi tiết.  
**Practice** : [**Sharift 2016**](https://hxp.io/blog/25/SharifCTF%202016:%20crypto350%20%22British%20Elevator%22%20writeup/)  

# 3. Pollard   
[CTF](https://aadityapurani.com/2019/03/11/utctf-2019-writeups/#alice)   


