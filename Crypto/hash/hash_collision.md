---
layout : post 
title : Hash Collision 
--- 

Giả sử chúng ta có một prefix message nào đó. Mà chúng ta muốn tạo ra 2 đoạn messages khác nhau có cùng mã hash MD5. Điều đó hoàn toàn có thể .   
Một thanh niên nào đó đã viết ra [**fastcoll**](https://github.com/upbit/clone-fastcoll).   

Hướng dẫn sử dụng :   
 - Clone cái trang kia 
 - make 
 - ./fastcoll prefix.txt 

Sau đó nó sẽ gen ra cho mình hai file ```md5_data1``` và ```md5_data2``` có cùng mã hash.  

