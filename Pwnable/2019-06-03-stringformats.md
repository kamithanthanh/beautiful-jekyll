---
layout : post
title : Một vài điều cơ bản về format strings
--- 

# Mở đầu  
Đây là lỗi ít gặp hơn stack overflow nhưng cũng vô cùng quan trọng. Tại tính hay quên nên note lại, khi cần mở ra xem cho nhanh . Kiến thức lấy từ cuốn _**The art of exploitaion**_ - một cuốn khá hay dành cho người bắt đầu và cuốn _**Nghệ thuật tận dụng lỗi phần mềm**_ của Nguyễn Thành Nam. 
# Hàm printf   
Hàm **printf** trong C có cấu trúc như sau :
```c
int printf ( const char * format, ... );
``` 
Một hàm hay dùng như này sao có thể bị lỗi được 😳😳😳 Lúc đầu mình cũng rất ngạc nhiên.Nhưng nếu dùng đúng cách thì đương nhiên nó sẽ rất an toàn.
Chỉ khi trong format có % mà lại không có biến kèm vào sẽ gây ra những vấn đề phức tạp : 
```c
printf("%x") ;
```
Hàm trên sẽ in ra những giá trị tại một địa chỉ trong stack dưới dạng hexadecimal.

# I - Đọc một địa chỉ bất kì  
Nếu chúng ta có một câu lệnh như sau : 
```c
printf(input) ; 
```
Thì chúng ta hoàn toàn có thể đọc và ghi lên một địa chỉ bất kì trong chương trình để làm những việc theo ý mình. 😎😎😎 Vào một ngày đẹp trời nào đó mà thằng lập trình viên gõ lỗi lệnh như vậy , chương trình vẫn sẽ chạy bình thường nhưng hacker chúng ta thì sẽ có việc để làm thôi . Cơ mà có vẻ hiếm lắm vì trước kia mình còn chả biết là in ra được **input** luôn mà không cần format thì chạy được cơ mà.  
Thôi lan man đủ rồi , cách tấn công là làm như sau : 
```c
printf("\xff\xff\xff\xff %08x.%08x.%08x.....) 
```
Trong đó ```\xff\xff\xff\xff``` thay bằng địa chỉ mà bạn muốn đọc. Phần ```...``` là điền đủ số lượng cho tới khi in ra được địa chỉ ```\xff\xff\xff\xff``` . Sau đó chọn lựa format ```%08x``` đã in ra địa chỉ kia thay bằng ```%s``` . Thế là đọc được nội dung đã được lưu thôi. Một mẹo nhỏ là đầu tiên nên thay địa chỉ cần đọc bằng string ```AAAA``` để trong bước đầu tiên phân biệt cho nó dễ.  

# II - Ghi lên một địa chỉ bất kì 
Bước đầu tiên chúng ta cũng làm như khi đọc giá trị của một địa chỉ bất kì. Bước cuối thay ```%s``` bằng ```%n``` . Khi đó thay vì đọc thì nó sẽ ghi số bytes đã được in bởi hàm prinf lên địa chỉ đích. Cơ mà ta thấy có một khó khăn rõ ràng là thông thường thì cần giá trị rất lớn , vd : ```0x08041337``` nếu thế thì hàm printf phải in rất nhiều mới đủ cho giá trị đó sao ? 😱😱😱 Điều đó không khả thi chút nào .  
Dưới đây trình bày lại một số thủ thuật ứng dụng cho từng trường hợp cụ thể để ghi giá trị lên địa chỉ ```0x08041337```
## II.1 - Ghi giá trị 0x300 
```c
printf("\x37\x13\x04\x08%768x%10$n")
```
```%10$n``` là cách truy cập trực tiếp một địa chỉ trên stack . Thay vì bạn dùng 10 kí tự ```%x``` thì ở đây chúng ta thay bằng 1 kí tự duy nhất thôi . Khá là tiện lợi và hữu ích trong trường hợp bị giới hạn kí tự input.  

## II.2 - Ghi giá trị 0x87654321 
Chúng ta sẽ thực hiện ghi từng bytes một lên lần lượt các địa chỉ ```0x08041337```,```0x08041338```,```0x08041339```,```0x08041340``` lần lượt các giá trị ```0x21```,```0x43```,```0x65```,```0x87```. Mình minh họa bằng python cho dễ nhìn. Giả sử ta có một chương trình C cho phép nhập input đầu vào có lỗi format như trên.
```python
python -c 'print"\x37\x13\x04\x08\x37\x13\x04\x08\x37\x13\x04\x08\x37\x13\x04\x08" + "%" + str(0x11) + "x%10$n%" + str(0x22) + "x%11$n%" 
+ str(0x22) + "x%12$n%" + str(0x22) + "x%13$n"' | ./test 
```
## II.3 - Ghi giá trị là 0x12345678
Chúng ta sẽ thực hiện ghi từng bytes một lên lần lượt các địa chỉ ```0x08041337```,```0x08041338```,```0x08041339```,```0x08041340``` lần lượt các giá trị ```0x321```,```0x243```,```0x165```,```0x87```. Mình minh họa bằng python cho dễ nhìn. Giả sử ta có một chương trình C cho phép nhập input đầu vào có lỗi format như trên. Tại sao phải làm vậy vì %n ghi độ dài chuỗi string đã được printf in ra nên ta không thể ghi 0x65 sau 0x87 được. 
## II.4 - Short write
Nếu dùng %n thì chúng ta ghi 4 bytes 1 lúc. Nếu chỉ muốn ghi 2 bytes thì dùng ```%hn``` thay thế. 

## Kết
Như vậy là ta đã có thể đọc và ghi bất kì giá trị nào lên một địa chỉ tùy ý trong chương trình rồi. Đây chỉ là những điều basis thôi :v 
Học xong cái này mình tưởng mấy bài string chỉ là muỗi cơ 😰😰😰 Cơ mà nhìn qua bài format string trong ISITDTU 2018 Quals sao mà nó khủng khiếp thế . Đúng là pwn thì sâu không lường được. Hi hi tích lũy dùng dần , lo đéo gì. 
Note lại có hơi vớ vẩn , cũng chỉ là copy lại để sau này dùng thôi :v Hope là sau này phát hiện ra cái mới để viết. 
![meo](https://tsukasakiyshu.files.wordpress.com/2012/06/3.png) 
