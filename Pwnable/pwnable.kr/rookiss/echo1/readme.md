---
layout : post 
title : Echooooo1 
subtitle : Rookiss Pwnable.kr  
image : /Pwnable/pwnable.kr/rookiss/echo1/echo1.png  
--- 

# Mở đầu
Tiếp tục series Pwnable.kr rookiss đây. Bài echo1 này là về shellcode và cách chạy nó trong chương trình. Mình vẫn chưa quen dùng shellcode lắm nên toàn đi copy trên mạng về rồi chạy thôi . Up lên có con shellcode chạy được có con lại không cũng méo hiểu lí do tại sao  😞😞😞 Đồng thời dùng tới kỹ thuật control EBP đã học ở các bài trước :v 

# Phân tích Binary  
**Hàm main**
```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  unsigned int *v3; // rsi
  _QWORD *O; // rax
  unsigned int choice; // [rsp+Ch] [rbp-24h]
  __int64 name_0; // [rsp+10h] [rbp-20h]
  __int64 name_1; // [rsp+18h] [rbp-18h]
  __int64 name_2; // [rsp+20h] [rbp-10h]

  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 1, 0LL);
  o = malloc(0x28uLL);
  *((_QWORD *)o + 3) = greetings;
  *((_QWORD *)o + 4) = byebye;
  printf("hey, what's your name? : ", 0LL);
  v3 = (unsigned int *)&name_0;
  __isoc99_scanf("%24s", &name_0);
  O = o;
  *(_QWORD *)o = name_0;
  O[1] = name_1;
  O[2] = name_2;
  id = name_0;
  getchar();
  func[0] = (__int64)echo1;
  func_1 = (__int64)echo2;
  func_2 = (__int64)echo3;
  choice = 0;
  do
  {
    while ( 1 )
    {
      while ( 1 )
      {
        puts("\n- select echo type -");
        puts("- 1. : BOF echo");
        puts("- 2. : FSB echo");
        puts("- 3. : UAF echo");
        puts("- 4. : exit");
        printf("> ", v3);
        v3 = &choice;
        __isoc99_scanf("%d", &choice);
        getchar();
        if ( choice > 3 )
          break;
        ((void (__fastcall *)(const char *, unsigned int *))func[choice - 1])("%d", &choice);
      }
      if ( choice == 4 )
        break;
      puts("invalid menu");
    }
    cleanup();
    printf("Are you sure you want to exit? (y/n)", &choice);
    choice = getchar();
  }
  while ( choice != 'y' );
  puts("bye");
  return 0;
}
```   
Hàm main khá là dài và đoạn đầu khá là khó hiểu . Nhưng nếu biết kết hợp với GDB thì mọi chuyện ez hơn nhiều. Ta có các biến toàn cục là **o**, **func**,**id** .   
![hinh2](/Pwnable/pwnable.kr/rookiss/echo1/hinh2.PNG)  

Đầu tiên hàm main xin cấp phát 0x28 bytes và lưu địa chỉ của vùng nhớ đó vào 8 bytes đầu của **o** . Sau đó thì tiếp tục ghi 24 bytes tên mà mình nhập vào lên vùng heap đó. Liền ngay sau đó là địa chỉ hàm **greatings** và hàm **byebye** . Không có lỗi overflow ở đây. 😁😁😁  
Mình đặt break point ở đâu đó trong hàm main để xem sau khi thực hiện các thao tác trên thì bộ nhớ trở thành thế nào :v   

![hinh3](/Pwnable/pwnable.kr/rookiss/echo1/hinh3.PNG)   

Làm như này thì sẽ dễ dàng hơn trong việc phán đoán hoạt động của code .  
  
**Hàm echo1**   
![hinh1](/Pwnable/pwnable.kr/rookiss/echo1/hinh1.PNG)  
Chúng ta có thể gọi hàm echo1 bằng tùy chọn 1 . Hàm này có lỗi tràn rõ ràng ở biến **s** . Chúng ta có thể control flow chương trình từ đây , do binary không có canary nên chúng ta có thể thoải mái tràn mà không sợ gì . 
😥😥😥 Đến đây lúc đầu không nghĩ shellcode mình vẫn thử theo cách thường làm là leak địa chỉ libc rồi gọi hàm system như bình thường thôi . Cơ mà khổ nỗi là các gadget nghèo nàn nên không thể đủ nguyên liệu để thực hiệp ROP . Bế tắc trong tuyệt vọng .   
✨✨✨ Sau đó mình mới nghĩ đến shellcode .Có hai điều cơ bản để chạy shellcode : 
 - Đặt ở đâu ? 
 - Chạy như nào ? 
Chúng ta có thể đặt shellcode ở biến s , nhưng chúng ta không biết địa chỉ của shellcode thì không thể chạy được. Vì vậy còn 1 chỗ là nhập shellcode vào tên. Tên có độ dài là 24 bytes nên ta cần tìm shellcode < 24 bytes.  👉 [đây](https://www.exploit-db.com/exploits/42179)  
Shellcode hiện đang đặt trong heap . Muốn chạy được shellcode thì phải control dòng chảy chương trình tới heap. Địa chỉ của vùng heap được lưu tại **o** . Kỹ thuật ROP vẫn không sử dụng được ở đây. Ta sẽ dùng technique Control EBP để đưa stack đến đúng địa chỉ rồi ret tới shellcode là ok 👌👌👌 Mình nói hơi khó hiểu tí :v  😄😄😄 Cơ mà thế cũng hay vì đỡ spoil quá nhiều :v  

# Kết  
Có một fun fact là mình nhập nhầm địa chỉ netcat của bài echo2 nên ngồi chửi đề lởm các kiểu 💢💢💢 :v  
Kết bài anh em ngắm ảnh mèo cho thư giãn  :v   
![hinh](https://i.ytimg.com/vi/x_9LcmVl3uU/hqdefault.jpg)  
