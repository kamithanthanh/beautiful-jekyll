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
# p = 1234 
P.<x,y> = GF(p)[]
f = x^3 + A*x + B 
C = Curve(-y^2 + f) 
singular_point = C.singular_points()
```

# Cusp and Node  
Sau khi xác định được singular point của (E). Chúng ta cần xác định xem Curve là Cusp hay Node.  
Chúng ta thực hiện chuyển đổi singular về dạng (0, 0). Giả sử ta có singular point là (x0, 0).  
Thực hiện script chuyển đổi hệ số :  
```sage
f_ = f.subs(x=x-x0)  
f_.factor()  
```
Nếu sau khi chuyển đổi hệ số mà ```f_=x^3``` thì Curve có dạng cusp. Không thì có dạng Node.  

# Attack 0n Cusp  
Chúng ta sẽ thực hiện một phép mapping từ Curve Field về FinityField. Mình còn chả biết từ ngữ mình dùng có đúng không nhưng bằng vào việc chuyển đổi này có thể đừa từ ECDLP về dạng DLP thông thường. Đối với Cusp, thực hiện map :  
![](https://latex.codecogs.com/gif.latex?E(Fp)&space;\mapsto&space;F_{p}^{&plus;},&space;(x,y)&space;\mapsto&space;\frac{x}{y},&space;\infty&space;\mapsto&space;0)  

# Tài liệu tham khảo  
 - [**Crypto StackExchange**](https://crypto.stackexchange.com/questions/61302/how-to-solve-this-ecdlp)  
