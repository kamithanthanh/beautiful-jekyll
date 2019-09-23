---
layout : post 
title : Teaser Dragon CTF RsaChain 
--- 

Trong kì thi có 1 bài crypto duy nhất và cũng là bài duy nhất mình làm được.  Các bạn có thể dowload challenge tại [đây](https://github.com/hacmao/hacmao.github.io/tree/master/Crypto/ctf/teaser_dragon)
Đây là một bài rsa 😬😬😬. Trước tiên nó thiết lập 4 key :  

```python
# rsa1: p - 700 bits q - 1400 bits

p = genPrime(700)
q = genPrime(1400)

n = p*q
phi = (p-1)*(q-1)
d = gmpy2.powmod(e, -1, phi)

rsa1 = (n, d)
``` 

Mấy key còn lại tương tự nhưng có thay đổi một chút. 😁
