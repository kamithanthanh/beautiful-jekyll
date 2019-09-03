---
layout : post 
title : Heap exploition 
subtitle : Leak Libc Address 
---

Do các bài về heap thì nó thường bật full cơ chế bảo vệ nên sẽ rất khó để leak heap theo cách stack thông thường. Do vậy phải có một cách đặc biệt 
để leak heap trong các libc . Một trong số đó được trình bày ở [đây](https://sploitfun.wordpress.com/2015/02/10/understanding-glibc-malloc/).  
