---
layout : post
title : ROCA - Return of Coppersmith Attack 
--- 

Đây là một cái kiểu tấn công factor mới mình học được trong kì thi [rooterCTF](https://medium.com/@Nicholaz99/rootersctf-2019-writeup-d500434c85fe#4f23). Nó dựa trên một lỗ hổng gì đó mà mình chưa tìm hiểu kĩ. Có thể check lỗ hông tại github này.  

  - [**ROCA detection tool**](https://github.com/crocs-muni/roca)  

Có thể build dễ dàng với pip :  
```
pip install roca-detect
```  

Cách sử dụng :  
```
roca-detect key.pem
```

Nếu có lỗi thì sẽ có dòng thông báo rằng có thể có vulnerable.  
Khi đó chúng ta tiếp tục sử dụng tool sau để phân tích module. 

# [NECA](https://gitlab.com/jix/neca)  
Mình mất khá nhiều thời gian để mò ra được cách build.  
```
install GMP 
cmake CMakeLists.txt 
make
./neca <N> 
```
