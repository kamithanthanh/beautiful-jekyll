---
layout : post 
title : Heap exploition 
subtitle : Leak Libc Address 
---

# Knowledge  
Do các bài về heap thì nó thường bật full cơ chế bảo vệ nên sẽ rất khó để leak heap theo cách stack thông thường. Do vậy phải có một cách đặc biệt để leak heap trong các libc . Một trong số đó được trình bày ở [đây](https://sploitfun.wordpress.com/2015/02/10/understanding-glibc-malloc/).  
Để leak được libc , chúng ta quan tâm tới FD, BK của các chunk head, tail trong chuỗi bins. Nó sẽ bao gồm địa chỉ của main_arena trong libc. Từ đó sử dụng một số lỗi nào đó để in ra giá trị của FD, BK. Như lỗi UAF(Use After Free).  

![](https://docs.google.com/drawings/d/1Kf_eg7uB2mRjSOasTc4dIu5fuBpTAK0GxbnKVTkZd0Y/pub?w=1217&h=865)  

Hình trên rất dễ hình dung khi chúng ta free một chunk ko phải là fast bin. Nó sẽ có dạng là double linked list. Có head và tail có con trỏ trỏ vào main_arena như đã nói trên. Nếu chỉ có một chunk trong double linked list thì cả FD, BK đều trỏ vào main_arena.  

# Practice  

- [Secret garden](https://pwnable.tw/)  
Trong bài này chúng ta có thể tùy ý malloc, free chunk với size tùy ý. Để leak được libc chúng ta cần malloc 1 chunk có kích thước đủ lớn để không phải là fastbin. Để hình thành double linked list có FD, BK trỏ vào main arena. Tiếp theo chúng ta cần malloc lại 1 chunk có kích thước bé hơn, ghi đè 8 bytes của BK. Rồi dùng hàm ```visit``` để in ra giá trị của FD. Lưu ý là cần có 1 hàm malloc 1 fast bin ở giữa trước khi free. Có vẻ malloc có 1 cái check security nào đó ở đây. Tóm lại script để leak libc có dạng :  

 ```python 
 a = malloc(0x100)
 b = malloc(0x100)
 free(a) 
 c = malloc(0xc8)   # size <  a 
 ```  


 
