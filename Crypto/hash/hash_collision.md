---
layout : post 
title : Hash Collision 
--- 

Tham khảo : https://github.com/corkami/collisions  

```
H(A) = H(B) 
-> H(A || C) = H(B || C)
``` 

# Identical prefix with junk suffix  

Ví dụ có một đoạn message `M`, `fastcoll` sẽ tìm ra 2 suffix s1, s2 sao cho :  
```
MD5(M || s1) = MD5(M || s2) 
```

##  [**fastcoll**](https://github.com/upbit/clone-fastcoll)

Hướng dẫn sử dụng :   
 - Clone cái trang kia 
 - make 
 - ./fastcoll prefix.txt 

Sau đó nó sẽ gen ra cho mình hai file ```md5_data1``` và ```md5_data2``` có cùng mã hash.  

## [Unicoll]  

Cái này khi có một đoạn message `M` mà nó trong blacklist thì ta có thể sử dụng để tạo ra một đoạn message `M' || junk` có cùng hash với 1 đoạn message chứa `M`.  

Script để dùng là cái `scripts/poc_no.sh` trong repo [hashclash](https://github.com/cr-marcstevens/hashclash).  

Cách sử dụng :  
```
../scripts/poc_no.sh prefix.txt
```
Lưu ý để công cụ thực hiện nhanh hơn thì prefix nên có độ dài là 68 bytes. Còn không thì khuyên là nên dùng vps, đừng dùng máy ảo :v Mình dùng máy ảo cùng 1 script mà chạy 3 tiếng chưa xong, lên vps chạy 15p xong :) Magic gì đây :))  

Ví dụ với prefix `sp3akfr1end4nd3nt3r\x00`, ta sẽ thu được 2 hash collsion như sau :  

```
colab@a17d4fd35b46:~/hashclash/tmp$ xxd collision1.bin 
00000000: 7370 3361 6b66 7231 656e 6434 6e64 336e  sp3akfr1end4nd3n
00000010: 7433 7200 0902 7cb9 4bac e7d4 9e80 21a6  t3r...|.K.....!.
00000020: 52fa a10d 5bc0 2a95 d551 85c1 754b 8f20  R...[.*..Q..uK. 
00000030: b59e cb08 3852 8184 77f6 d514 282c d3fa  ....8R..w...(,..
00000040: 1fe1 8850 51a8 4d3e eafb 2389 008a f526  ...PQ.M>..#....&
00000050: bd1a 578d a5a6 c16d 904c fc9a b4fe 9c97  ..W....m.L......
00000060: 1ca1 c774 5354 f63a 1b0f cf9e 656a ec96  ...tST.:....ej..
00000070: 6da0 06dc ac54 4319 a3ee 4715 073b 5351  m....TC...G..;SQ
colab@a17d4fd35b46:~/hashclash/tmp$ xxd collision2.bin 
00000000: 7370 3361 6b66 7231 656f 6434 6e64 336e  sp3akfr1eod4nd3n
00000010: 7433 7200 0902 7cb9 4bac e7d4 9e80 21a6  t3r...|.K.....!.
00000020: 52fa a10d 5bc0 2a95 d551 85c1 754b 8f20  R...[.*..Q..uK. 
00000030: b59e cb08 3852 8184 77f6 d514 282c d3fa  ....8R..w...(,..
00000040: 1fe1 8850 51a8 4d3e eafa 2389 008a f526  ...PQ.M>..#....&
00000050: bd1a 578d a5a6 c16d 904c fc9a b4fe 9c97  ..W....m.L......
00000060: 1ca1 c774 5354 f63a 1b0f cf9e 656a ec96  ...tST.:....ej..
00000070: 6da0 06dc ac54 4319 a3ee 4715 073b 5351  m....TC...G..;SQ
colab@a17d4fd35b46:~/hashclash/tmp$ md5sum collision*
8b7085199865a95104524f340012c956  collision1.bin
8b7085199865a95104524f340012c956  collision2.bin
```

## Hashclash  

Choosen prefix hash attack :))  

Tức là ta có hai cái message là `yes`, `no`. Ta muốn padding nó thành `yes || s1` và `no || s2` để nó có cùng md5 :))  

Thì sẽ dùng `scripts/cpc.sh` trong `hashclash`.  


