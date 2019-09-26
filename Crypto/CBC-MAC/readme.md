---
layout : post 
title : CBC Messages Authenticate Code 
--- 

# How it works  

Một hệ thống xác thực người dùng bằng CBC-MAC hoạt động theo nguyên tắc sau :  
 1. Mã hóa messages của người dùng bằng AES CBC.  
 2. Chữ kí là block cuối cùng của đoạn mã hóa. 
 3. Trả về message + iv + sign 

