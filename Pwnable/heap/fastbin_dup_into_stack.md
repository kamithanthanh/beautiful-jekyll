---
layout : post 
title : Heap Exploit Technique 
subtitle : Fastbin dup into stack  
--- 

# Basic knowledge    

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
 - Set Stack_target-8 = fake size, fake size = fastbin size , P = 0  để pass security check.  
 - Free linked list : stack -> a  
 - Malloc 2 fast bin 👉 stack  

**Note** : Địa chỉ của stack khi ghi lên user phải là : stack_target - 2 * sizeof(a) có nghĩa là trừ đi kích thước của phần size.  

Source : [here](https://github.com/shellphish/how2heap/blob/master/glibc_2.25/fastbin_dup_into_stack.c)  

# Practice  
 - [**Secret Garden**](https://pwnable.tw/)  
 Bài này sử dụng kĩ thuật fastbin dup into stack để có thể malloc về địa chỉ của hàm ```malloc_hook```. Lưu ý để pass cái security check như trên mà chúng ta không thể trực tiếp control được cái size như ở bước trên . Vì vậy người ta đã tìm được vị trí ```malloc_hook-0x13``` là vị trí phù hợp để pass được security check. Như vậy chúng ta có thể dup đến địa chỉ kia rồi ghi đè địa chỉ mong muốn lên ```malloc_hook```.   
