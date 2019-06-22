---
layout : post 
title : rsa calculator 
subtitle : Rookiss Pwnable.kr 
--- 

# Mở đầu
Tiếp tục với loạt bài rookiss trên Pwnable.kr . Đây là bài rookiss netcat cuối cùng nên mình sẽ tạm dừng loạt bài này tại đây và chuyển sang
cày trên trang khác. Bài này mình ngâm cứu khá lâu vì cũng đang nghỉ hè, cơn lười ập tới 😓😓😓 . Sau vài ngày kiên trì với loạt binary khá
là dài và nhiều lỗi thì mình cũng hoàn thành xong . Bài này mình làm sử dụng lỗi ```format string``` là chính . 

# Phân tích binary  
Source code khá là dài nên mình sẽ không phân tích chi tiết.  

**Hàm encrypt*** 

![hinh3](/Pwnable/pwnable.kr/rookiss/rsa_caculator/hinh3.PNG)  

Đọc có vẻ khá phức tạp và lằng nhằng nhưng về cơ bản là hàm này đọc input của người dùng và mã hóa từng kí tự của string input theo kiểu rsa.
Lưu ý là từng string input nha 😀😀😀. Rồi lưu vào biến toàn cục ```g_ebuf``` . Đặt breakpoint rồi coi trong GDB sẽ rõ hơn  

![hinh4](//Pwnable/pwnable.kr/rookiss/rsa_caculator/hinh4.PNG)  

Hình trên mình minh họa cho việc encrypt string ```a```. Và thu được cipher là một số nguyên 32 bit . Nhưng khi in ra thành chuỗi thì nó hơi dị
một chút , nó lại là ```6ea49f20``` tức là theo kiểu little endian .  
Sau tất cả công đoạn trên, mình viết lại hàm code encrypt_rsa như sau  :  
```python 
def encrypt_rsa(string) : 
    cipher = '' 
    for char in string : 
        encode = pow(ord(char),e,n) 
        encode = unhexlify(hex(encode)[2:].zfill(8))[::-1] 
        encode = hexlify(encode) 
        cipher += encode 
    return cipher 
```

Tương tự với hàm decrypt thì mình cũng viết lại thành một hàm decrypt_rsa như sau :  
```python 
def decrypt_rsa(cipher) : 
    p = '' 
    for i in range(0,len(cipher),8) : 
        c = cipher[i : i+8]
        c = int(hexlify(unhexlify(c)[::-1]),16) 
        m = pow(c,d,n) % 256 
        p += chr(m) 
    return p
```   
Ơ trong hai hàm encrypt và decrypt đều có lỗi overflow 😨😨😨 Mình tập trung tìm ở đây khá là nhiều cơ mà nó rất khó là control vì mọi cái mà
gây ra lỗi tràn đều bị biến đổi qua hàm rsa. 😬😬😬 Đến đây sau khi vừa làm vừa chơi , mình ngồi đọc lại code thì thấy trong hàm decrypt có
một lỗi format string khá là rõ ràng 😖😖😖 Tại code khá là dài và mình đọc khá là lướt nên không nhận ra lỗi này ngay từ đầu @@ . 

![hinh2](/Pwnable/pwnable.kr/rookiss/rsa_caculator/hinh1.PNG)  

Từ lỗi format string này chúng ta có thể overwrite lên địa chỉ GOT của hàm printf bằng địa chỉ của hàm system được lưu trong bss  

![hinh2](/Pwnable/pwnable.kr/rookiss/rsa_caculator/hinh2.PNG)  

Nếu không có hàm system được lưu trong bss thì chúng ta phải leak địa chỉ libc các kiểu 😁😁 May mà bài này nó cho trước nên khỏi mất công chi.
Quay lại trước một chút,tại sao lại chon GOT của hàm printf , vì nó là hàm duy nhất cho phép chúng ta chọn tham số string đầu vào. Vì vậy 
có thể nhập chuỗi ```/bin/sh\x00``` một cách dễ dàng.  
Công đoạn còn lại cũng khá là khoai vì phải căn chỉnh format string các kiểu với RSA nên khá là mắc công . Nhưng khó khăn lớn nhất đã vượt qua thì
chả lẽ cái này lại không vượt được 👍👍👍  

# Kết thúc  
Mới đây mình đọc được một câu nói khá hay , đại ý là như này  
> Chúng ta luôn nghĩ cuộc sống của chúng ta thêm một ai đó thì mọi thứ sẽ tuyệt vời hơn. Nhưng không có họ chúng ta vẫn sống tốt mà. 
