---
layout : post 
title : CBC Messages Authenticate Code 
--- 

# How it works  

Một hệ thống xác thực người dùng bằng CBC-MAC hoạt động theo nguyên tắc sau :  
 - Mã hóa messages của người dùng bằng AES CBC.  
 - Chữ kí là block cuối cùng của đoạn mã hóa. 
 - Trả về message + iv + sign  

# Type 0f Attack  
 - [**CBC-MAC Forgery**](#type1)  

<a name="type1"></a>  
# CBC-MAC Forgery  
hello
















a
