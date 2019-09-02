---
layout : post 
title : Heap Exploit Technique 
subtitle : Fastbin dup into stack  
--- 

**Điều kiện sử dụng** :  
 - Double free  
 - Control size of malloc  

**Mục đích** : 
 - Malloc lên stack  

**Phương pháp**:  
 - Malloc 2 fastbin chunk : a, b  
 - Free : a -> b -> a  👉 Free linked list : a -> b -> a  
 - Malloc 2 fastbin with same size  👉 Free linked list : a  
 - Giờ ta có quyền kiểm soát dữ liệu trong user data của a, viết giá trị địa chỉ stack muốn đạt được lên user data của chunk a.  
 - Free linked list : stack -> a  
 - Malloc 2 fast bin 👉 stack  

**Note** : Địa chỉ của stack khi ghi lên user phải là : stack_target - 2 * sizeof(a) có nghĩa là trừ đi kích thước của phần size.  

Source : [here](https://github.com/shellphish/how2heap/blob/master/glibc_2.25/fastbin_dup_into_stack.c)  
