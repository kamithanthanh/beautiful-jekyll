---
layout : post 
title : Trick on Heap
--- 

# Turn off aslr  
Turn off :  
  ```echo 0 | sudo tee /proc/sys/kernel/randomize_va_space```  

Turn on : 
  ```echo 2 | sudo tee /proc/sys/kernel/randomize_va_space```  

