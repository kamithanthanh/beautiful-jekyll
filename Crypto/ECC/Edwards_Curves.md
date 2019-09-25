---
layout : post 
title : Edwards Curves 
--- 

Có một số dạng Curve đặc biệt mà chúng ta cần lưu ý. Edwards Curves là một đường cong có phương trình :   

![](https://latex.codecogs.com/gif.latex?ax^{2}&space;&plus;&space;y^{2}&space;=&space;1&space;&plus;&space;dx^{2}y^{2})   

Ta có phép cộng của nó sẽ có dạng :   

![](https://latex.codecogs.com/gif.latex?(x_{1}&space;,y_{1})&space;&plus;&space;(x_{2},y_{2})&space;=&space;(\frac{x_{1}y_{2}&plus;x_{2}y_{1}}{1&plus;dx_{1}x_{2}y_{1}y_{2}},&space;\frac{y_{1}y_{2}-ax_{1}x_{2}}{1-dx_{1}x_{2}y_{1}y_{2}}))

Nếu cho một loại mã hoạt động có phép cộng theo công thức trên thì có thể nghĩ tới đưa về phương trình Edwards như trên để giải nghiệm.  

**Practice** : [Crypto CTF 2019](http://mslc.ctf.su/wp/1st-crypto-ctf-2019-least-solved-challenges/)   
