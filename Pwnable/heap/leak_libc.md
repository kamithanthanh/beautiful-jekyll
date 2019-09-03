---
layout : post 
title : Heap exploition 
subtitle : Leak Libc Address 
---

Do các bài về heap thì nó thường bật full cơ chế bảo vệ nên sẽ rất khó để leak heap theo cách stack thông thường. Do vậy phải có một cách đặc biệt để leak heap trong các libc . Một trong số đó được trình bày ở [đây](https://sploitfun.wordpress.com/2015/02/10/understanding-glibc-malloc/).  
Để leak được libc , chúng ta quan tâm tới FD, BK của các chunk head, tail trong chuỗi bins. Nó sẽ bao gồm địa chỉ của main_arena trong libc. Từ đó sử dụng một số lỗi nào đó để in ra giá trị của FD, BK. Như lỗi UAF(Use After Free).  

![](https://docs.google.com/drawings/d/1Kf_eg7uB2mRjSOasTc4dIu5fuBpTAK0GxbnKVTkZd0Y/pub?w=1217&h=865)  
