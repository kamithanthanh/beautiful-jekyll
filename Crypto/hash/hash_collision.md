---
layout : post 
title : Hash Collision 
--- 



```
H(A) = H(B) 
-> H(A || C) = H(B || C)
``` 

# Identical prefix with junk suffix  

Ví dụ có một đoạn message `M`, `fastcoll` sẽ tìm ra 2 suffix s1, s2 sao cho :  
```
MD5(M || s1) = MD5(M || s2) 
```

##  [**fastcoll**](https://github.com/upbit/clone-fastcoll).   

Hướng dẫn sử dụng :   
 - Clone cái trang kia 
 - make 
 - ./fastcoll prefix.txt 

Sau đó nó sẽ gen ra cho mình hai file ```md5_data1``` và ```md5_data2``` có cùng mã hash.  



