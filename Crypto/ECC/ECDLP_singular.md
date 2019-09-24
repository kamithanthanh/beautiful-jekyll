---
layout : post 
title : One way to attack ECDLP of singular  
---  

# Mở đầu  
ECC luôn là vấn đề phức tạp 😥😥😥 Cần rất nhiều kiến thức toán. Mà mình lại là một script K1dd13. 😁😁😁 Nếu bạn cũng là một scr1pt k1dd13 thì w3lc0m3. Chúng ta chung lí tưởng. Vì là script kidde nên mình sẽ không đi quá sâu vào từng chi tiết một. Chỉ là cái nhìn lướt qua đủ hiểu vấn đề này là gì, khi nào thì dùng và dùng bằng cách nào.  

# Singular Point  
Giả sử ta có được cong Elliptic (E) trên GF(p) :  

![](https://latex.codecogs.com/gif.latex?y^{2}&space;=&space;x^{3}&space;&plus;&space;A\times&space;x&space;&plus;&space;B)  

Singular là nghiệm của phương trình trên GF(p) :  

![](https://latex.codecogs.com/gif.latex?x^{3}&space;&plus;&space;A\times&space;x&space;&plus;&space;B=0)  

Đối với Curve có Singular point thì sage sẽ không thiết lập được bằng hàm ```EllipticCurve```. Chúng ta có thể thiết lập bằng cách khác để tìm singular point như sau :  
```sage
p = ... 
P.<x,y> = GF(p)[]
f = x^3 + A*x + B 
C = Curve(-y^2 + f) 
singular_point = C.singular_points()
```

# Cusp and Node  
Sau khi xác định được singular point của (E). 
# Tài liệu tham khảo  
 - [**Crypto StackExchange**](https://crypto.stackexchange.com/questions/61302/how-to-solve-this-ecdlp)  
