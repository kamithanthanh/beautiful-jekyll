---
layout : post 
title : Heap exploition 
subtitle : Leak Libc Address 
---

# Unsorted bins leak  
Do các bài về heap thì nó thường bật full cơ chế bảo vệ nên sẽ rất khó để leak heap theo cách stack thông thường. Do vậy phải có một cách đặc biệt để leak heap trong các libc . Một trong số đó được trình bày ở [đây](https://sploitfun.wordpress.com/2015/02/10/understanding-glibc-malloc/).  
Để leak được libc , chúng ta quan tâm tới FD, BK của các chunk head, tail trong chuỗi bins. Nó sẽ bao gồm địa chỉ của main_arena trong libc. Từ đó sử dụng một số lỗi nào đó để in ra giá trị của FD, BK. Như lỗi UAF(Use After Free).  

![](https://docs.google.com/drawings/d/1Kf_eg7uB2mRjSOasTc4dIu5fuBpTAK0GxbnKVTkZd0Y/pub?w=1217&h=865)  

Hình trên rất dễ hình dung khi chúng ta free một chunk ko phải là fast bin. Nó sẽ có dạng là double linked list. Có head và tail có con trỏ trỏ vào main_arena như đã nói trên. Nếu chỉ có một chunk trong double linked list thì cả FD, BK đều trỏ vào main_arena.  

# Angel Boy leak  
Overwrite ```stdout->flags = 0xfbad1800```, đồng thời ghi giá trị NULL lên ```_IO_read_ptr, _IO_read_end, _IO_read_base``` và last bytes của ```_IO_write_base```.  
Nói chúng trong hàm puts có 1 function như này :  

```c
int
_IO_new_file_overflow (_IO_FILE *f, int ch)
{
  if (f->_flags & _IO_NO_WRITES) /* SET ERROR */
    {
      f->_flags |= _IO_ERR_SEEN;
      __set_errno (EBADF);
      return EOF;
    }
  /* If currently reading or no buffer allocated. */
  if ((f->_flags & _IO_CURRENTLY_PUTTING) == 0 || f->_IO_write_base == NULL)
    {
      :
      :
    }
  if (ch == EOF)
    return _IO_do_write (f, f->_IO_write_base,  // our target
			 f->_IO_write_ptr - f->_IO_write_base);
```

Đây là target : ```_IO_do_write (f, f->_IO_write_base,  // our target
			 f->_IO_write_ptr - f->_IO_write_base); ```  
Thực hiện ghi đè lên ```stdout-> flags = 0xfbad1800``` để qua tất cả các check để đến được target.  
Sau đó chúng ta ghi đè 1 bytes "\x00" lên bytes cuối cùng của ```_IO_write_base``` để nó trỏ sang một địa chỉ trước địa chỉ cần in. Từ đó in thêm cho chúng ta một số thông tin về địa chỉ của libc.   
# Practice  

- [Secret garden](https://pwnable.tw/)  
Trong bài này chúng ta có thể tùy ý malloc, free chunk với size tùy ý. Để leak được libc chúng ta cần malloc 1 chunk có kích thước đủ lớn để không phải là fastbin. Để hình thành double linked list có FD, BK trỏ vào main arena. Tiếp theo chúng ta cần malloc lại 1 chunk có kích thước bé hơn, ghi đè 8 bytes của BK. Rồi dùng hàm ```visit``` để in ra giá trị của FD. Lưu ý là cần có 1 hàm malloc 1 fast bin ở giữa trước khi free. Có vẻ malloc có 1 cái check security nào đó ở đây. Tóm lại script để leak libc có dạng :  

 ```python 
 a = malloc(0x100)
 b = malloc(0x100)
 free(a) 
 c = malloc(0xc8)   # size <  a 
 ```  


 
