---
layout : post 
title : One way to attack ECDLP of singular  
---  

# Mở đầu  
ECC luôn là vấn đề phức tạp 😥😥😥 Cần rất nhiều kiến thức toán. Mà mình lại là một script K1dd13. 😁😁😁 Nếu bạn cũng là một scr1pt k1dd13 thì w3lc0m3. Chúng ta chung lí tưởng. Vì là script kidde nên mình sẽ không đi quá sâu vào từng chi tiết một. Chỉ là cái nhìn lướt qua đủ hiểu vấn đề này là gì, khi nào thì dùng và dùng bằng cách nào.  

# Singular Point  
Giả sử ta có được cong Elliptic (E) trên GF(p) :  
![](https://latex.codecogs.com/gif.latex?y^{2}&space;=&space;x^{3}&space;&plus;&space;A\times&space;x&space;&plus;&space;B)  

Singular là nghiệm của phương trình :  
![](https://latex.codecogs.com/gif.latex?x^{3}&space;&plus;&space;A\times&space;x&space;&plus;&space;B=0)  


