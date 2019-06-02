---
layout : post
title : Một vài điều cơ bản về format strings
--- 

# Mở đầu  
Đây là lỗi ít gặp hơn stack overflow nhưng cũng vô cùng quan trọng. Tại tính hay quên nên note lại, khi cần mở ra xem cho nhanh . Kiến thức lấy
từ cuốn _**The art of exploitaion**_ - một cuốn khá hay dành cho người bắt đầu. 
# Hàm printf   
Hàm **printf** trong C có cấu trúc như sau :
```C
int printf ( const char * format, ... );
``` 
Một hàm hay dùng như này sao có thể bị lỗi được 😳😳😳 Lúc đầu mình cũng rất ngạc nhiên.Nhưng nếu dùng đúng cách thì đương nhiên nó sẽ rất an toàn.
Chỉ khi trong format có % mà lại không có biến kèm vào sẽ gây ra những vấn đề phức tạp : 
```C
printf("%x") ;
```
Hàm trên sẽ in ra những giá trị tại một địa chỉ trong stack dưới dạng hexadecimal.

# đọc và ghi một địa chỉ bất kì  
Nếu chúng ta có một câu lệnh như sau : 
```C
printf(input) ; 
```
Thì chúng ta hoàn toàn có thể đọc và ghi lên một địa chỉ bất kì trong chương trình để làm những việc theo ý mình. 😎😎😎 Vào một ngày đẹp trờin ào đó mà thằng lập trình viên gõ lỗi lệnh như vậy , chương trình vẫn sẽ chạy bình thường nhưng hacker chúng ta thì sẽ có việc để làm thôi . Cơ màcó vẻ hiếm lắm vì trước kia mình còn chả biết là in ra được **inpu** luôn mà không cần format thì chạy được cơ mà.  
Thôi lan man đủ rồi , cách tấn công là làm như sau : 
```C
printf("\xff\xff\xff\xff %08x.%08x.%08x.....) 
```
Trong đó ```\xff\xff\xff\xff``` thay bằng địa chỉ mà bạn muốn đọc. Phần ```...``` là  
