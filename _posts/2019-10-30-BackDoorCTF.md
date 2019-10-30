---
layout : post
title : BackDoor CTF 2019 
---   

# Table of Content 
 - [**[PWN] Baby Heap**](#wu1)  
 - [**[PWN] MiscPwn**](#wu2)   
 


<a name="wu1">  
</a>   

# Baby Heap

Bài này trong lúc thi mình không làm được. 😝😝😝 Hôm đó cũng bất ngờ vì cái action của chương trình này rất lạ lol.  Rõ ràng là mình đã free fastbin mà nó lại vào hết unsortedbins. 😱😱😱 Nay đọc wu thì mới hiểu được vấn đề. Đồng thời, vận dụng tốt hơn việc ghi đè lên GOT.  
Chương trình có ba chức năng cơ bản :   

**add**  
![](/Pwnable/ctf/BackDoor/babyheap/hinh1.PNG)   


**remove**   
![](/Pwnable/ctf/BackDoor/babyheap/hinh2.PNG)    

**edit**   
![](/Pwnable/ctf/BackDoor/babyheap/hinh3.PNG)   

Có những lỗi cơ bản như **double free** và **UAF** thì chương trình này đều có cả :vv Như mình đã note trên hình.    

## Step 1 : By pass mallopt   
Trở lại vấn đề mình nêu đầu tiên : Tại sao free fastbin nó lại vào hết unsorted bin. 😬😬😬   

```c
    mallopt(1, 0);  
```  
Hàm này sẽ điểu chỉnh quá trình malloc behavior. Cụ thể là nó sẽ sửa ```global_max_fast=0x10```. Như vậy thì mọi chunk size > 0x10 đều rơi vào unsorted bin hết :v  
Như vậy ban đầu chúng ta chỉ có thể sử dụng các kĩ thuật tấn công trên unsorted bin.   
Một trong những kĩ thuật tấn công trên unsorted bin được dùng trong bài này được trình bày ở [đây](https://github.com/shellphish/how2heap/blob/master/glibc_2.26/unsorted_bin_attack.c)   

👉 Các bước thực hiện : 
  - malloc 1 unsorted bin 
  - free chunk 
  - change bd -> target - 2 * size 

👉 Đạt được : thay đổi giá trị của target thành heap address.   

Chúng ta có thể dùng lỗi trên để ghi đè lên ```global_max_fast``` thành 1 giá trị cực lớn. Như vậy thì mọi chunk khi free sẽ thành fastbin và ta có thể tiến hành những kiểu tấn công quen thuộc.   

Sau khi tạo 1 chunk rồi free thì FD, BK sẽ có dạng :    

![](/Pwnable/ctf/BackDoor/babyheap/hinh5.PNG)    

Như vậy , ta chỉ cần thay đổi 4 byte cuối của ```BK``` thành ```global_max_fast``` là được. Mà 3 bytes cuối của ```global_max_fast``` không thay đổi nên chúng ta chỉ cần brute force 1 byte để có thể tiến hành ghi đè lên ```global_max_fast```.  

## Step 2 : Fastbin dup into bss   
Sau khi giải quyết vấn đề **mallopt** thì việc còn lại nhẹ nhàng hơn.  Chúng ta không hề có hàm in ra để leak được giá trị của libc. Đến đây là mình nghĩ ngay đến kĩ thuật của ```angel boy``` nhưng như vậy là quá phức tạp. Đồng thời size của ```global_max_fast``` cũng khá là lớn nên việc tạo ra một unsorted bin là điều không tưởng.   

😎😎😎 Và đến đây mình học thêm kĩ thuật vừa cũ lại mới với mình : ghi đè lên GOT. Trong những bài heap thì thường người ta bật full cơ chế bảo vệ nên mình không nghĩ đến cách tấn công này. Nhưng trong bài này thì người ta chỉ bật ```partial RELRO``` đồng thời ```PIE``` cũng tắt luôn.    

Để ghi đè lên GOT thì mình sẽ dup lên vùng bss ```0x602100```.   
Để thực hiện được fastbin thì mình cần tạo một fake size cho chunk mới nên mình tạo fake bằng cách :  

```python
add(8, 0x50, "lol") 
```  

![](/Pwnable/ctf/BackDoor/babyheap/hinh4.PNG)  

Sau đó chúng ta có thể tùy ý thay đổi giá trị con trỏ của node[0], node[1] thành GOT của các hàm khác.  
Đồng thời tận dụng hàm edit để chỉnh sửa giá trị của GOT.  
Các bước tấn công được thực hiện theo các bước sau :  
   - node[0] = free_got 
   - node[1] = atoi_got 
   - edit(node[0]) = printf_plt 
   - free(1)  - in ra got của atoi -> leak 
   - edit(node[1]) = system 
   - sh.sendline("/bin/sh") 

Khá là đơn giản và dễ hiểu 😀😀😀    

<a name="wu2">  
</a>   
# MiscPwn   

Đây tiếp tục là một bài heap lạ lol 🌝🌝🌝.   
Chương trình hết sức đơn giản :   

![](/Pwnable/ctf/BackDoor/miscpwn/hinh1.PNG)    

Mà càng thứ gì đơn giản lại càng khó sml. 😁😁😁   
Bài này dùng một kĩ thuật như sau :   

```
Khi malloc một chunk size đủ lớn, malloc sẽ gọi mmap. Khi malloc(10000000) sẽ return một địa chỉ đủ gần libc.   
```

Nhờ kĩ thuật trên chúng ta leak được địa chỉ của libc.   

![](/Pwnable/ctf/BackDoor/miscpwn/hinh2.PNG)    


Sau đó , chúng ta có lỗi out of bound có thể ghi đè lên vùng nhớ. Lại có heap của chúng ta khá gần với libc nên có thể ghi đè lên ```malloc_hook``` hoặc ```free_hook```. Tuy nhiên bài này các one_gadget đều không hoạt động.  

Tác giả của wu thực hiện như sau :   
```
  - ghi đè lên __realloc_hook : one_gadget
  - ghi đè lên __malloc_hook : realloc + 14  
```  
Đoạn ```relloc + 14``` có lẽ là một hằng số mà mình cũng không rõ lắm tại sao 😂😂😂    


# END   
Haha Sắp đến SVATTT rồi hóng quá. Không biết là sẽ nát như nào đây 😂😂😂



